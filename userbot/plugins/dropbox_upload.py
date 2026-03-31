# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# credits= @medusaXD(https://t.me/medusaXD) #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Dropbox File Uploader Plugin
# Upload, rename, extract, batch sync, and manage files on Dropbox
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import asyncio
import math
import os
import shutil
import tarfile
import tempfile
import time
import zipfile
from urllib.parse import unquote, urlparse

import aiohttp
import dropbox
from dropbox.exceptions import ApiError, AuthError
from dropbox.files import WriteMode
from telethon.errors import FloodWaitError

from userbot import catub

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply

plugin_category = "misc"

CHUNK_SIZE = 16 * 1024 * 1024
DEFAULT_FOLDER = "/CatUserBot"
STATUS_UPDATE_INTERVAL = 15
STATUS_EDIT_THROTTLE = 3
SUPPORTED_ARCHIVES = (
    ".zip",
    ".tar",
    ".tar.gz",
    ".tgz",
    ".tar.bz2",
    ".tar.xz",
    ".7z",
    ".rar",
)

status_dict = {}
cancel_dict = {}
task_trackers = {}
task_intervals = {}


class TaskCancelledError(Exception):
    """Raised when the active task is cancelled."""


class SetInterval:
    """Simple async interval wrapper."""

    def __init__(self, interval, action):
        self.interval = interval
        self.action = action
        self._task = asyncio.create_task(self._runner())

    async def _runner(self):
        try:
            while True:
                await asyncio.sleep(self.interval)
                try:
                    await self.action()
                except Exception:
                    pass
        except asyncio.CancelledError:
            pass

    def cancel(self):
        self._task.cancel()


class DownloadProgress:
    """Tracks download progress using running-average speed."""

    def __init__(self, sid, task_name, status_label, total_bytes=0):
        self.sid = sid
        self.task_name = task_name
        self.status_label = status_label
        self.total_bytes = int(total_bytes or 0)
        self.processed_bytes = 0
        self.start_time = time.time()
        self.batch_info = None
        self.seeders = None
        self.leechers = None

    @property
    def speed(self):
        elapsed = time.time() - self.start_time
        return self.processed_bytes / elapsed if elapsed > 0 else 0

    def progress_callback(self, current, total):
        check_cancelled(self.sid)
        self.processed_bytes = max(0, int(current or 0))
        self.total_bytes = max(0, int(total or 0))


class UploadProgress:
    """Tracks upload progress using uploaded deltas per callback."""

    def __init__(self, sid, task_name, status_label, total_bytes=0, batch_info=None):
        self.sid = sid
        self.task_name = task_name
        self.status_label = status_label
        self.total_bytes = int(total_bytes or 0)
        self.processed_bytes = 0
        self.last_uploaded = 0
        self.start_time = time.time()
        self.batch_info = batch_info
        self.seeders = None
        self.leechers = None

    @property
    def speed(self):
        elapsed = time.time() - self.start_time
        return self.processed_bytes / elapsed if elapsed > 0 else 0

    def progress_callback(self, current, total):
        check_cancelled(self.sid)
        current = max(0, int(current or 0))
        total = max(0, int(total or 0))
        chunk_size = max(0, current - self.last_uploaded)
        self.processed_bytes += chunk_size
        self.last_uploaded = current
        self.total_bytes = max(self.total_bytes, total)


def get_readable_file_size(size_in_bytes):
    """Convert bytes to B/KB/MB/GB/TB."""
    if size_in_bytes is None:
        return "0B"
    try:
        size = float(size_in_bytes)
    except (TypeError, ValueError):
        return "0B"
    if size <= 0:
        return "0B"
    units = ["B", "KB", "MB", "GB", "TB"]
    unit_index = 0
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    if unit_index == 0:
        return f"{int(size)}B"
    return f"{size:.2f}{units[unit_index]}"


def get_readable_time(seconds):
    """Convert seconds to a compact readable string."""
    try:
        seconds = int(max(0, seconds or 0))
    except (TypeError, ValueError):
        return "0s"
    if seconds == 0:
        return "0s"
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    parts = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    if seconds or not parts:
        parts.append(f"{seconds}s")
    return "".join(parts)


def render_progress_bar(percentage):
    """Render a 12-char bar using ⬢ and ⬡."""
    try:
        percentage = float(percentage)
    except (TypeError, ValueError):
        percentage = 0
    percentage = max(0, min(100, percentage))
    filled = math.floor(percentage / 8)
    if percentage >= 100:
        filled = 12
    filled = max(0, min(12, filled))
    return f"[{'⬢' * filled}{'⬡' * (12 - filled)}]"


def get_flood_wait_seconds(error):
    value = getattr(error, "value", None)
    if value is None:
        value = getattr(error, "seconds", 0)
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0


def get_message_text(message):
    return getattr(message, "text", None) or getattr(message, "message", None) or ""


async def safe_message_edit(message, text):
    """Edit a Telegram message safely and return the message object plus edit status."""
    if get_message_text(message) == text:
        return message, False
    try:
        edited_message = await message.edit(text)
    except FloodWaitError as flood_wait:
        await asyncio.sleep(get_flood_wait_seconds(flood_wait) * 1.2)
        try:
            edited_message = await message.edit(text)
        except Exception:
            return message, False
    except Exception:
        return message, False
    if edited_message is not None:
        message = edited_message
    try:
        message.message = text
    except Exception:
        pass
    return message, True


def check_cancelled(sid):
    if cancel_dict.get(sid):
        raise TaskCancelledError("Task cancelled by user.")


def is_url(text):
    """Check if text looks like a URL."""
    try:
        result = urlparse(text.strip())
        return result.scheme in ("http", "https")
    except Exception:
        return False


def normalize_dropbox_folder(folder):
    if folder is None:
        return DEFAULT_FOLDER
    folder = folder.strip()
    if not folder:
        return DEFAULT_FOLDER
    if folder == "/":
        return ""
    return folder if folder.startswith("/") else f"/{folder}"


def build_dropbox_path(folder, name):
    folder = normalize_dropbox_folder(folder)
    if folder in ("", "/"):
        return f"/{name}"
    return f"{folder.rstrip('/')}/{name}"


def get_reply_file_name(reply):
    reply_file = getattr(reply, "file", None)
    if reply_file and getattr(reply_file, "name", None):
        return reply_file.name
    document = getattr(reply, "document", None)
    if document:
        for attribute in getattr(document, "attributes", []):
            file_name = getattr(attribute, "file_name", None)
            if file_name:
                return file_name
    return f"telegram_{reply.id}"


def get_reply_file_size(reply):
    reply_file = getattr(reply, "file", None)
    if reply_file and getattr(reply_file, "size", None):
        return reply_file.size
    document = getattr(reply, "document", None)
    return getattr(document, "size", 0) or 0


def render_task_text(tracker):
    elapsed = max(time.time() - tracker.start_time, 0)
    processed = max(0, tracker.processed_bytes)
    total = max(0, tracker.total_bytes)
    speed = tracker.speed
    if total > 0:
        percentage = min(100, (processed / total) * 100)
        eta = round((total - processed) / speed) if speed > 0 else 0
        estimated_total = elapsed + eta
        total_text = get_readable_file_size(total)
    else:
        percentage = 0
        eta = 0
        estimated_total = elapsed
        total_text = "Unknown"
    lines = [
        f"**{tracker.task_name}**",
        f"`{render_progress_bar(percentage)} {percentage:.2f}%`",
        f"`{get_readable_file_size(processed)} / {total_text}` | `{tracker.status_label}`",
        f"**Speed:** `{get_readable_file_size(speed)}/s`",
        f"**ETA:** `{get_readable_time(eta)}` | **Elapsed:** `{get_readable_time(elapsed)}` | **Est:** `{get_readable_time(estimated_total)}`",
    ]
    if tracker.batch_info:
        lines.append(f"**Batch:** `({tracker.batch_info[0]}/{tracker.batch_info[1]})`")
    if tracker.seeders is not None and tracker.leechers is not None:
        lines.append(
            f"**Seeders:** `{tracker.seeders}` | **Leechers:** `{tracker.leechers}`"
        )
    return "\n".join(lines)


async def update_status_message(sid, force=False):
    entry = status_dict.get(sid)
    tracker = task_trackers.get(sid)
    if not entry or not tracker:
        return
    if not force and (time.time() - entry["last_update"]) < STATUS_EDIT_THROTTLE:
        return
    new_text = render_task_text(tracker)
    message, edited = await safe_message_edit(entry["message"], new_text)
    entry["message"] = message
    if edited:
        entry["last_update"] = time.time()


def schedule_status_update(sid, force=False):
    entry = status_dict.get(sid)
    if not entry or sid not in task_trackers:
        return
    if not force and (time.time() - entry["last_update"]) < STATUS_EDIT_THROTTLE:
        return
    try:
        asyncio.get_event_loop().create_task(update_status_message(sid, force=force))
    except RuntimeError:
        pass


def start_status_session(sid, message, is_user=False):
    if sid in status_dict:
        return False
    status_dict[sid] = {
        "message": message,
        "last_update": 0,
        "page_no": 1,
        "page_step": 1,
        "status_filter": None,
        "is_user": is_user,
    }
    cancel_dict[sid] = False
    task_intervals[sid] = SetInterval(
        STATUS_UPDATE_INTERVAL,
        lambda sid=sid: update_status_message(sid),
    )
    return True


def end_status_session(sid):
    interval = task_intervals.pop(sid, None)
    if interval:
        interval.cancel()
    task_trackers.pop(sid, None)
    status_dict.pop(sid, None)
    cancel_dict.pop(sid, None)


async def set_active_tracker(sid, tracker):
    task_trackers[sid] = tracker
    await update_status_message(sid, force=True)


def clear_active_tracker(sid, tracker=None):
    if tracker is None or task_trackers.get(sid) is tracker:
        task_trackers.pop(sid, None)


def get_dbx():
    """Initialize and return Dropbox client, or None if credentials are missing.

    Prefers refresh-token OAuth (auto-refreshes) over a short-lived access token.
    """
    app_key = getattr(Config, "DROPBOX_APP_KEY", None)
    app_secret = getattr(Config, "DROPBOX_APP_SECRET", None)
    refresh_token = getattr(Config, "DROPBOX_REFRESH_TOKEN", None)
    if app_key and app_secret and refresh_token:
        return dropbox.Dropbox(
            app_key=app_key,
            app_secret=app_secret,
            oauth2_refresh_token=refresh_token,
        )
    token = getattr(Config, "DROPBOX_ACCESS_TOKEN", None)
    if not token:
        return None
    return dropbox.Dropbox(token)


async def validate_dbx(event):
    """Validate Dropbox client. Returns client or sends error and returns None."""
    dbx = get_dbx()
    if not dbx:
        await edit_delete(
            event,
            "**Dropbox not configured.**\n"
            "Set `DROPBOX_APP_KEY` + `DROPBOX_APP_SECRET` + `DROPBOX_REFRESH_TOKEN` (recommended)\n"
            "or set `DROPBOX_ACCESS_TOKEN` (expires ~4h).\n"
            "Get credentials from https://www.dropbox.com/developers/apps",
        )
        return None
    try:
        dbx.users_get_current_account()
    except AuthError:
        await edit_delete(
            event,
            "**Invalid Dropbox token.** Check your DROPBOX_ACCESS_TOKEN.",
        )
        return None
    return dbx


async def count_progress(event, phase, current, total, current_name):
    """Progress for count-based operations (extraction)."""
    if total <= 0:
        return
    percentage = current * 100 / total
    text = (
        f"**{phase}** `({current}/{total})`\n"
        f"`{render_progress_bar(percentage)} {percentage:.2f}%`\n"
        f"**Current:** `{current_name}`"
    )
    await safe_message_edit(event, text)


async def upload_to_dropbox(dbx, file_path, dropbox_path, sid, batch_info=None):
    """Upload a file to Dropbox with chunked upload and progress tracking."""
    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)
    tracker = UploadProgress(
        sid,
        file_name,
        "Uploading to Dropbox",
        file_size,
        batch_info=batch_info,
    )
    await set_active_tracker(sid, tracker)
    try:
        with open(file_path, "rb") as file_obj:
            if file_size <= CHUNK_SIZE:
                check_cancelled(sid)
                dbx.files_upload(
                    file_obj.read(),
                    dropbox_path,
                    mode=WriteMode("overwrite"),
                )
                tracker.progress_callback(file_size, file_size)
                await update_status_message(sid, force=True)
                return
            check_cancelled(sid)
            first_chunk = file_obj.read(CHUNK_SIZE)
            session = dbx.files_upload_session_start(first_chunk)
            current_uploaded = file_obj.tell()
            tracker.progress_callback(current_uploaded, file_size)
            await update_status_message(sid)
            cursor = dropbox.files.UploadSessionCursor(
                session_id=session.session_id,
                offset=file_obj.tell(),
            )
            commit = dropbox.files.CommitInfo(
                path=dropbox_path,
                mode=WriteMode("overwrite"),
            )
            while file_obj.tell() < file_size:
                check_cancelled(sid)
                remaining = file_size - file_obj.tell()
                if remaining <= CHUNK_SIZE:
                    dbx.files_upload_session_finish(
                        file_obj.read(remaining),
                        cursor,
                        commit,
                    )
                    current_uploaded = file_size
                else:
                    chunk = file_obj.read(CHUNK_SIZE)
                    dbx.files_upload_session_append_v2(chunk, cursor)
                    cursor.offset = file_obj.tell()
                    current_uploaded = cursor.offset
                tracker.progress_callback(current_uploaded, file_size)
                await update_status_message(sid)
                await asyncio.sleep(0)
            await update_status_message(sid, force=True)
    finally:
        clear_active_tracker(sid, tracker)


async def get_share_link(dbx, dropbox_path):
    """Create or retrieve a shareable link for a Dropbox path."""
    try:
        shared = dbx.sharing_create_shared_link_with_settings(dropbox_path)
        return shared.url
    except ApiError as error:
        if error.error.is_shared_link_already_exists():
            links = dbx.sharing_list_shared_links(path=dropbox_path, direct_only=True)
            if links.links:
                return links.links[0].url
        raise


async def download_from_telegram(reply, download_dir, sid):
    """Download a file from a Telegram message with progress tracking."""
    os.makedirs(download_dir, exist_ok=True)
    tracker = DownloadProgress(
        sid,
        get_reply_file_name(reply),
        "Downloading from Telegram",
        get_reply_file_size(reply),
    )
    await set_active_tracker(sid, tracker)
    file_path = None

    def progress_callback(current, total):
        tracker.progress_callback(current, total)
        schedule_status_update(sid)

    try:
        file_path = await reply.download_media(
            file=download_dir,
            progress_callback=progress_callback,
        )
        if file_path and os.path.exists(file_path):
            tracker.task_name = os.path.basename(file_path)
            final_size = os.path.getsize(file_path)
            tracker.progress_callback(final_size, final_size)
            await update_status_message(sid, force=True)
        return file_path
    finally:
        clear_active_tracker(sid, tracker)


async def download_from_url(url, download_dir, sid, custom_name=None):
    """Download a file from a URL with progress tracking."""
    os.makedirs(download_dir, exist_ok=True)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return None
            if custom_name:
                file_name = custom_name
            else:
                disposition = response.headers.get("Content-Disposition", "")
                if "filename=" in disposition:
                    file_name = disposition.split("filename=")[-1].strip('" ')
                else:
                    file_name = unquote(os.path.basename(urlparse(url).path)) or "download"
            try:
                total = int(response.headers.get("Content-Length", 0) or 0)
            except ValueError:
                total = 0
            file_path = os.path.join(download_dir, file_name)
            downloaded = 0
            tracker = DownloadProgress(sid, file_name, "Downloading from URL", total)
            await set_active_tracker(sid, tracker)
            try:
                with open(file_path, "wb") as file_obj:
                    async for chunk in response.content.iter_chunked(1024 * 1024):
                        check_cancelled(sid)
                        file_obj.write(chunk)
                        downloaded += len(chunk)
                        tracker.progress_callback(downloaded, total or downloaded)
                        await update_status_message(sid)
                        await asyncio.sleep(0)
                if total <= 0:
                    tracker.total_bytes = downloaded
                tracker.processed_bytes = downloaded
                await update_status_message(sid, force=True)
                return file_path
            finally:
                clear_active_tracker(sid, tracker)


async def extract_archive(file_path, extract_dir, event, sid=None):
    """Extract an archive and show extraction progress."""
    os.makedirs(extract_dir, exist_ok=True)
    ext = file_path.lower()
    file_list = []
    try:
        if ext.endswith(".zip"):
            with zipfile.ZipFile(file_path, "r") as zip_file:
                file_list = [name for name in zip_file.namelist() if not name.endswith("/")]
                total = len(file_list)
                for index, name in enumerate(file_list, 1):
                    if sid is not None:
                        check_cancelled(sid)
                    zip_file.extract(name, extract_dir)
                    await count_progress(event, "Extracting", index, total, name)
        elif ext.endswith((".tar", ".tar.gz", ".tgz", ".tar.bz2", ".tar.xz")):
            with tarfile.open(file_path, "r:*") as tar_file:
                members = [member for member in tar_file.getmembers() if member.isfile()]
                file_list = [member.name for member in members]
                total = len(members)
                for index, member in enumerate(members, 1):
                    if sid is not None:
                        check_cancelled(sid)
                    tar_file.extract(member, extract_dir)
                    await count_progress(event, "Extracting", index, total, member.name)
        elif ext.endswith(".7z"):
            import py7zr

            with py7zr.SevenZipFile(file_path, mode="r") as seven_zip:
                file_list = [name for name in seven_zip.getnames() if not name.endswith("/")]
                total = len(file_list)
                if sid is not None:
                    check_cancelled(sid)
                seven_zip.extractall(path=extract_dir)
                for index, name in enumerate(file_list, 1):
                    if sid is not None:
                        check_cancelled(sid)
                    await count_progress(event, "Extracting", index, total, name)
        elif ext.endswith(".rar"):
            import rarfile

            with rarfile.RarFile(file_path) as rar_file:
                file_list = [item.filename for item in rar_file.infolist() if not item.is_dir()]
                total = len(file_list)
                for index, name in enumerate(file_list, 1):
                    if sid is not None:
                        check_cancelled(sid)
                    rar_file.extract(name, extract_dir)
                    await count_progress(event, "Extracting", index, total, name)
        else:
            return None
    except Exception as error:
        raise Exception(f"Extraction failed: {error}")
    return file_list


def cleanup(*paths):
    """Remove files and directories."""
    for path in paths:
        if path and os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path, ignore_errors=True)
            else:
                os.remove(path)


async def finalize_task(message, sid, text=None, *paths):
    cleanup(*paths)
    end_status_session(sid)
    if text is not None:
        message, _ = await safe_message_edit(message, text)
    return message


@catub.cat_cmd(
    pattern="dropbox(?:\s|$)([\s\S]*)",
    command=("dropbox", plugin_category),
    info={
        "header": "Upload files to Dropbox and get a shareable link.",
        "description": "Reply to a file or provide a direct URL to upload to Dropbox.",
        "usage": [
            "{tr}dropbox <reply to file>",
            "{tr}dropbox <url>",
            "{tr}dropbox /custom/folder <reply to file>",
            "{tr}dropbox <url> | /custom/folder",
        ],
    },
)
async def dropbox_upload_cmd(event):
    """Upload a file to Dropbox."""
    dbx = await validate_dbx(event)
    if not dbx:
        return
    input_str = event.pattern_match.group(1).strip()
    reply = await event.get_reply_message()
    catevent = await edit_or_reply(event, "`Processing...`")
    sid = event.chat_id
    if not start_status_session(sid, catevent, event.is_private):
        return await edit_delete(
            catevent,
            "**Another Dropbox task is already running in this chat. Use `.dbcancel` first.**",
        )
    start_time = time.time()
    download_dir = Config.TMP_DOWNLOAD_DIRECTORY
    file_path = None
    dropbox_folder = DEFAULT_FOLDER
    try:
        if reply and reply.media:
            if input_str:
                dropbox_folder = normalize_dropbox_folder(input_str)
            file_path = await download_from_telegram(reply, download_dir, sid)
        elif input_str:
            parts = [part.strip() for part in input_str.split("|")]
            url_candidate = parts[0]
            if is_url(url_candidate):
                if len(parts) > 1:
                    dropbox_folder = normalize_dropbox_folder(parts[1])
                file_path = await download_from_url(url_candidate, download_dir, sid)
            elif input_str.startswith("/") and reply and reply.media:
                dropbox_folder = normalize_dropbox_folder(input_str)
                file_path = await download_from_telegram(reply, download_dir, sid)
        if not file_path:
            return await finalize_task(
                catevent,
                sid,
                "**Reply to a file or provide a URL.**",
            )
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        dropbox_path = build_dropbox_path(dropbox_folder, file_name)
        await upload_to_dropbox(dbx, file_path, dropbox_path, sid)
        link = await get_share_link(dbx, dropbox_path)
    except TaskCancelledError:
        return await finalize_task(catevent, sid, "**❌ Cancelled**", file_path)
    except Exception as error:
        return await finalize_task(
            catevent,
            sid,
            f"**Upload failed:**\n`{error}`",
            file_path,
        )
    elapsed = round(time.time() - start_time)
    await finalize_task(
        catevent,
        sid,
        (
            f"**✅ Uploaded to Dropbox**\n\n"
            f"**File:** `{file_name}`\n"
            f"**Size:** `{get_readable_file_size(file_size)}`\n"
            f"**Path:** `{dropbox_path}`\n"
            f"**Time:** `{get_readable_time(elapsed)}`\n\n"
            f"**🔗 Link:** {link}"
        ),
        file_path,
    )


@catub.cat_cmd(
    pattern="dbrename(?:\s|$)([\s\S]*)",
    command=("dbrename", plugin_category),
    info={
        "header": "Rename and upload a file to Dropbox.",
        "usage": [
            "{tr}dbrename <new_name> <reply to file>",
            "{tr}dbrename <new_name> | /folder <reply to file>",
            "{tr}dbrename <url> | <new_name>",
            "{tr}dbrename <url> | <new_name> | /folder",
        ],
    },
)
async def dbrename_cmd(event):
    """Rename a file and upload to Dropbox."""
    dbx = await validate_dbx(event)
    if not dbx:
        return
    input_str = event.pattern_match.group(1).strip()
    if not input_str:
        return await edit_delete(
            event,
            "**Provide a new name.**\nUsage: `.dbrename <name>` (reply to file)",
        )
    reply = await event.get_reply_message()
    parts = [part.strip() for part in input_str.split("|")]
    catevent = await edit_or_reply(event, "`Processing...`")
    sid = event.chat_id
    if not start_status_session(sid, catevent, event.is_private):
        return await edit_delete(
            catevent,
            "**Another Dropbox task is already running in this chat. Use `.dbcancel` first.**",
        )
    start_time = time.time()
    download_dir = Config.TMP_DOWNLOAD_DIRECTORY
    file_path = None
    new_path = None
    new_name = None
    dropbox_folder = DEFAULT_FOLDER
    try:
        if is_url(parts[0]):
            url = parts[0]
            if len(parts) < 2:
                return await finalize_task(
                    catevent,
                    sid,
                    "**Provide a new name.**\n`.dbrename <url> | <new_name>`",
                )
            new_name = parts[1]
            if len(parts) > 2:
                dropbox_folder = normalize_dropbox_folder(parts[2])
            file_path = await download_from_url(url, download_dir, sid)
        elif reply and reply.media:
            new_name = parts[0]
            if len(parts) > 1:
                dropbox_folder = normalize_dropbox_folder(parts[1])
            file_path = await download_from_telegram(reply, download_dir, sid)
        else:
            return await finalize_task(
                catevent,
                sid,
                "**Reply to a file or provide a URL.**",
            )
        if not file_path:
            return await finalize_task(catevent, sid, "**Download failed.**")
        old_dir = os.path.dirname(file_path)
        _, old_ext = os.path.splitext(file_path)
        _, new_ext = os.path.splitext(new_name)
        if not new_ext and old_ext:
            new_name = new_name + old_ext
        new_path = os.path.join(old_dir, new_name)
        os.rename(file_path, new_path)
        file_size = os.path.getsize(new_path)
        dropbox_path = build_dropbox_path(dropbox_folder, new_name)
        await upload_to_dropbox(dbx, new_path, dropbox_path, sid)
        link = await get_share_link(dbx, dropbox_path)
    except TaskCancelledError:
        return await finalize_task(
            catevent,
            sid,
            "**❌ Cancelled**",
            file_path,
            new_path,
        )
    except Exception as error:
        return await finalize_task(
            catevent,
            sid,
            f"**Upload failed:**\n`{error}`",
            file_path,
            new_path,
        )
    elapsed = round(time.time() - start_time)
    await finalize_task(
        catevent,
        sid,
        (
            f"**✅ Renamed & Uploaded to Dropbox**\n\n"
            f"**File:** `{new_name}`\n"
            f"**Size:** `{get_readable_file_size(file_size)}`\n"
            f"**Path:** `{dropbox_path}`\n"
            f"**Time:** `{get_readable_time(elapsed)}`\n\n"
            f"**🔗 Link:** {link}"
        ),
        new_path,
    )


@catub.cat_cmd(
    pattern="dbextract(?:\s|$)([\s\S]*)",
    command=("dbextract", plugin_category),
    info={
        "header": "Extract an archive and upload all files to Dropbox.",
        "description": "Supports zip, tar, tar.gz, tar.bz2, rar, 7z",
        "usage": [
            "{tr}dbextract <reply to archive>",
            "{tr}dbextract /custom/folder <reply to archive>",
            "{tr}dbextract <url>",
            "{tr}dbextract <url> | /custom/folder",
        ],
    },
)
async def dbextract_cmd(event):
    """Extract archive and upload contents to Dropbox."""
    dbx = await validate_dbx(event)
    if not dbx:
        return
    input_str = event.pattern_match.group(1).strip()
    reply = await event.get_reply_message()
    parts = [part.strip() for part in input_str.split("|")] if input_str else []
    catevent = await edit_or_reply(event, "`Processing...`")
    sid = event.chat_id
    if not start_status_session(sid, catevent, event.is_private):
        return await edit_delete(
            catevent,
            "**Another Dropbox task is already running in this chat. Use `.dbcancel` first.**",
        )
    start_time = time.time()
    download_dir = Config.TMP_DOWNLOAD_DIRECTORY
    extract_dir = tempfile.mkdtemp(prefix="dbextract_")
    file_path = None
    dropbox_folder = DEFAULT_FOLDER
    try:
        if parts and is_url(parts[0]):
            if len(parts) > 1:
                dropbox_folder = normalize_dropbox_folder(parts[1])
            file_path = await download_from_url(parts[0], download_dir, sid)
        elif reply and reply.media:
            if parts and parts[0]:
                dropbox_folder = normalize_dropbox_folder(parts[0])
            file_path = await download_from_telegram(reply, download_dir, sid)
        else:
            return await finalize_task(
                catevent,
                sid,
                "**Reply to an archive or provide a URL.**",
                extract_dir,
            )
        if not file_path:
            return await finalize_task(
                catevent,
                sid,
                "**Download failed.**",
                extract_dir,
            )
        lower_path = file_path.lower()
        if not any(lower_path.endswith(ext) for ext in SUPPORTED_ARCHIVES):
            return await finalize_task(
                catevent,
                sid,
                f"**Unsupported format.**\nSupported: `{', '.join(SUPPORTED_ARCHIVES)}`",
                file_path,
                extract_dir,
            )
        file_list = await extract_archive(file_path, extract_dir, catevent, sid=sid)
        if not file_list:
            return await finalize_task(
                catevent,
                sid,
                "**Archive is empty or format unsupported.**",
                file_path,
                extract_dir,
            )
        archive_name = os.path.splitext(os.path.basename(file_path))[0]
        if archive_name.endswith(".tar"):
            archive_name = archive_name[:-4]
        upload_folder = build_dropbox_path(dropbox_folder, archive_name)
        total_files = len(file_list)
        total_size = 0
        for index, relative_path in enumerate(file_list, 1):
            check_cancelled(sid)
            local_path = os.path.join(extract_dir, relative_path)
            if not os.path.isfile(local_path):
                continue
            dbx_relative_path = relative_path.replace("\\", "/")
            dbx_path = f"{upload_folder.rstrip('/')}/{dbx_relative_path}"
            total_size += os.path.getsize(local_path)
            await upload_to_dropbox(
                dbx,
                local_path,
                dbx_path,
                sid,
                batch_info=(index, total_files),
            )
        link = await get_share_link(dbx, upload_folder)
    except TaskCancelledError:
        return await finalize_task(
            catevent,
            sid,
            "**❌ Cancelled**",
            file_path,
            extract_dir,
        )
    except Exception as error:
        return await finalize_task(
            catevent,
            sid,
            f"**Upload failed:**\n`{error}`",
            file_path,
            extract_dir,
        )
    elapsed = round(time.time() - start_time)
    await finalize_task(
        catevent,
        sid,
        (
            f"**✅ Extracted & Uploaded to Dropbox**\n\n"
            f"**Files:** `{total_files}`\n"
            f"**Total Size:** `{get_readable_file_size(total_size)}`\n"
            f"**Folder:** `{upload_folder}`\n"
            f"**Time:** `{get_readable_time(elapsed)}`\n\n"
            f"**🔗 Link:** {link}"
        ),
        file_path,
        extract_dir,
    )


@catub.cat_cmd(
    pattern="dbsync(?:\s|$)([\s\S]*)",
    command=("dbsync", plugin_category),
    info={
        "header": "Batch upload files to Dropbox.",
        "description": "Reply to an album to upload all grouped media, or specify a count to upload multiple messages.",
        "usage": [
            "{tr}dbsync <reply to album>",
            "{tr}dbsync <count> <reply to message>",
            "{tr}dbsync <count> | /custom/folder",
        ],
    },
)
async def dbsync_cmd(event):
    """Batch upload files to Dropbox."""
    dbx = await validate_dbx(event)
    if not dbx:
        return
    input_str = event.pattern_match.group(1).strip()
    reply = await event.get_reply_message()
    if not reply:
        return await edit_delete(event, "**Reply to a message to batch upload.**")
    parts = [part.strip() for part in input_str.split("|")] if input_str else []
    dropbox_folder = DEFAULT_FOLDER
    count = 0
    if parts:
        try:
            count = int(parts[0])
        except ValueError:
            if parts[0].startswith("/"):
                dropbox_folder = normalize_dropbox_folder(parts[0])
        if len(parts) > 1:
            dropbox_folder = normalize_dropbox_folder(parts[1])
    catevent = await edit_or_reply(event, "`Collecting files...`")
    sid = event.chat_id
    if not start_status_session(sid, catevent, event.is_private):
        return await edit_delete(
            catevent,
            "**Another Dropbox task is already running in this chat. Use `.dbcancel` first.**",
        )
    messages = []
    if count > 0:
        chat = event.chat_id
        msg_id = reply.id
        collected = 0
        async for message in event.client.iter_messages(chat, min_id=msg_id - 1, limit=count + 50):
            if message.id >= msg_id and message.media:
                messages.append(message)
                collected += 1
                if collected >= count:
                    break
        if reply.media and reply not in messages:
            messages.insert(0, reply)
    elif reply.grouped_id:
        chat = event.chat_id
        async for message in event.client.iter_messages(chat, min_id=reply.id - 15, max_id=reply.id + 15):
            if message.grouped_id == reply.grouped_id and message.media:
                messages.append(message)
        messages.sort(key=lambda msg: msg.id)
    elif reply.media:
        messages = [reply]
    if not messages:
        return await finalize_task(catevent, sid, "**No media found to upload.**")
    total = len(messages)
    batch_name = f"batch_{int(time.time())}"
    batch_folder = build_dropbox_path(dropbox_folder, batch_name)
    start_time = time.time()
    download_dir = Config.TMP_DOWNLOAD_DIRECTORY
    uploaded_files = []
    total_size = 0
    current_file_path = None
    catevent, _ = await safe_message_edit(
        catevent,
        f"`Found {total} files. Starting upload...`",
    )
    try:
        for index, message in enumerate(messages, 1):
            check_cancelled(sid)
            current_file_path = await download_from_telegram(message, download_dir, sid)
            if not current_file_path:
                continue
            file_name = os.path.basename(current_file_path)
            file_size = os.path.getsize(current_file_path)
            total_size += file_size
            dropbox_path = build_dropbox_path(batch_folder, file_name)
            try:
                await upload_to_dropbox(
                    dbx,
                    current_file_path,
                    dropbox_path,
                    sid,
                    batch_info=(index, total),
                )
                uploaded_files.append(file_name)
            except TaskCancelledError:
                raise
            except Exception:
                pass
            finally:
                cleanup(current_file_path)
                current_file_path = None
        if not uploaded_files:
            return await finalize_task(catevent, sid, "**Failed to upload any files.**")
        try:
            link = await get_share_link(dbx, batch_folder)
        except Exception:
            link = "Could not generate folder link"
    except TaskCancelledError:
        return await finalize_task(
            catevent,
            sid,
            "**❌ Cancelled**",
            current_file_path,
        )
    elapsed = round(time.time() - start_time)
    await finalize_task(
        catevent,
        sid,
        (
            f"**✅ Batch Upload Complete**\n\n"
            f"**Files:** `{len(uploaded_files)}/{total}`\n"
            f"**Total Size:** `{get_readable_file_size(total_size)}`\n"
            f"**Folder:** `{batch_folder}`\n"
            f"**Time:** `{get_readable_time(elapsed)}`\n\n"
            f"**🔗 Link:** {link}"
        ),
    )


@catub.cat_cmd(
    pattern="dbcancel$",
    command=("dbcancel", plugin_category),
    info={
        "header": "Cancel the active Dropbox task in the current chat.",
        "usage": ["{tr}dbcancel"],
    },
)
async def dbcancel_cmd(event):
    """Cancel the active Dropbox task for this chat."""
    sid = event.chat_id
    if sid not in status_dict:
        return await edit_delete(event, "**No active Dropbox task to cancel.**")
    cancel_dict[sid] = True
    await edit_delete(event, "`Cancellation requested...`", 5)


@catub.cat_cmd(
    pattern="dblist(?:\s|$)([\s\S]*)",
    command=("dblist", plugin_category),
    info={
        "header": "List files and folders in a Dropbox path.",
        "usage": ["{tr}dblist", "{tr}dblist /path"],
    },
)
async def dblist_cmd(event):
    """List files in a Dropbox folder."""
    dbx = await validate_dbx(event)
    if not dbx:
        return
    path = event.pattern_match.group(1).strip() or ""
    if path == "/":
        path = ""
    catevent = await edit_or_reply(event, "`Listing files...`")
    try:
        result = dbx.files_list_folder(path)
    except ApiError as error:
        return await edit_delete(catevent, f"**Error:**\n`{error}`")
    if not result.entries:
        return await edit_delete(catevent, f"**No files found in** `{path or '/'}`")
    output = f"**📂 Dropbox: `{path or '/'}`**\n\n"
    for entry in result.entries:
        if isinstance(entry, dropbox.files.FolderMetadata):
            output += f"📁 `{entry.name}/`\n"
        else:
            output += f"📄 `{entry.name}` — `{get_readable_file_size(entry.size)}`\n"
    await catevent.edit(output)


@catub.cat_cmd(
    pattern="dbdel(?:\s|$)([\s\S]*)",
    command=("dbdel", plugin_category),
    info={
        "header": "Delete a file or folder from Dropbox.",
        "usage": ["{tr}dbdel /path/to/file"],
    },
)
async def dbdel_cmd(event):
    """Delete a file or folder from Dropbox."""
    dbx = await validate_dbx(event)
    if not dbx:
        return
    path = event.pattern_match.group(1).strip()
    if not path:
        return await edit_delete(event, "**Provide a path.**\nUsage: `.dbdel /path/to/file`")
    catevent = await edit_or_reply(event, f"`Deleting {path}...`")
    try:
        dbx.files_delete_v2(path)
    except ApiError as error:
        return await edit_delete(catevent, f"**Error:**\n`{error}`")
    await catevent.edit(f"**🗑️ Deleted:** `{path}`")


@catub.cat_cmd(
    pattern="dbfolder(?:\s|$)([\s\S]*)",
    command=("dbfolder", plugin_category),
    info={
        "header": "Create a new folder in Dropbox.",
        "usage": ["{tr}dbfolder /path/to/folder"],
    },
)
async def dbfolder_cmd(event):
    """Create a folder in Dropbox."""
    dbx = await validate_dbx(event)
    if not dbx:
        return
    path = event.pattern_match.group(1).strip()
    if not path:
        return await edit_delete(event, "**Provide a path.**\nUsage: `.dbfolder /my/folder`")
    path = normalize_dropbox_folder(path)
    if not path:
        return await edit_delete(event, "**Provide a valid folder path.**")
    catevent = await edit_or_reply(event, f"`Creating folder {path}...`")
    try:
        dbx.files_create_folder_v2(path)
    except ApiError as error:
        return await edit_delete(catevent, f"**Error:**\n`{error}`")
    await catevent.edit(f"**📁 Folder created:** `{path}`")


@catub.cat_cmd(
    pattern="dbinfo$",
    command=("dbinfo", plugin_category),
    info={
        "header": "Show Dropbox account info.",
        "usage": ["{tr}dbinfo"],
    },
)
async def dbinfo_cmd(event):
    """Show Dropbox account information."""
    dbx = await validate_dbx(event)
    if not dbx:
        return
    catevent = await edit_or_reply(event, "`Fetching info...`")
    try:
        account = dbx.users_get_current_account()
        space = dbx.users_get_space_usage()
    except Exception as error:
        return await edit_delete(catevent, f"**Error:**\n`{error}`")
    used = space.used
    allocation = space.allocation
    if allocation.is_individual():
        allocated = allocation.get_individual().allocated
    elif allocation.is_team():
        allocated = allocation.get_team().allocated
    else:
        allocated = used or 1
    percentage = round(used * 100 / allocated, 1) if allocated > 0 else 0
    await catevent.edit(
        f"**📦 Dropbox Account**\n\n"
        f"**Name:** `{account.name.display_name}`\n"
        f"**Email:** `{account.email}`\n"
        f"**Plan:** `{account.account_type._tag}`\n"
        f"**Used:** `{get_readable_file_size(used)}` / `{get_readable_file_size(allocated)}` (`{percentage}%`)\n"
    )


@catub.cat_cmd(
    pattern="dbspace$",
    command=("dbspace", plugin_category),
    info={
        "header": "Show Dropbox storage usage with visual bar.",
        "usage": ["{tr}dbspace"],
    },
)
async def dbspace_cmd(event):
    """Show Dropbox storage usage bar."""
    dbx = await validate_dbx(event)
    if not dbx:
        return
    catevent = await edit_or_reply(event, "`Checking storage...`")
    try:
        space = dbx.users_get_space_usage()
    except Exception as error:
        return await edit_delete(catevent, f"**Error:**\n`{error}`")
    used = space.used
    allocation = space.allocation
    if allocation.is_individual():
        allocated = allocation.get_individual().allocated
    elif allocation.is_team():
        allocated = allocation.get_team().allocated
    else:
        allocated = used or 1
    percentage = round(used * 100 / allocated, 1) if allocated > 0 else 0
    bar = render_progress_bar(percentage)
    await catevent.edit(
        f"**💾 Dropbox Storage**\n\n"
        f"`{bar} {percentage}%`\n"
        f"**Used:** `{get_readable_file_size(used)}` / `{get_readable_file_size(allocated)}`\n"
        f"**Free:** `{get_readable_file_size(allocated - used)}`"
    )
