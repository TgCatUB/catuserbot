# Userbot module for fetching info about any user on Telegram(including you!).

import html
import os

from requests import get
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location

from . import LOGS, get_user_from_event, spamwatch

TMP_DOWNLOAD_DIRECTORY = Config.TMP_DOWNLOAD_DIRECTORY


@bot.on(admin_cmd(pattern="userinfo(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="userinfo(?: |$)(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    replied_user, error_i_a = await get_full_user(event)
    if replied_user is None:
        return await edit_or_reply(event, f"`{str(error_i_a)}`")
    user_id = replied_user.user.id
    # some people have weird HTML in their names
    first_name = html.escape(replied_user.user.first_name)
    # https://stackoverflow.com/a/5072031/4723940
    # some Deleted Accounts do not have first_name
    if first_name is not None:
        # some weird people (like me) have more than 4096 characters in their
        # names
        first_name = first_name.replace("\u2060", "")
    # inspired by https://telegram.dog/afsaI181
    common_chats = replied_user.common_chats_count
    try:
        dc_id, location = get_input_location(replied_user.profile_photo)
    except Exception:
        dc_id = "Couldn't fetch DC ID!"
    if spamwatch:
        ban = spamwatch.get_ban(user_id)
        if ban:
            sw = f"**Spamwatch Banned :** `True` \n       **-**🤷‍♂️**Reason : **`{ban.reason}`"
        else:
            sw = f"**Spamwatch Banned :** `False`"
    else:
        sw = "**Spamwatch Banned :**`Not Connected`"
    try:
        casurl = "https://api.cas.chat/check?user_id={}".format(user_id)
        data = get(casurl).json()
    except Exception as e:
        LOGS.info(e)
        data = None
    if data:
        if data["ok"]:
            cas = "**Antispam(CAS) Banned :** `True`"
        else:
            cas = "**Antispam(CAS) Banned :** `False`"
    else:
        cas = "**Antispam(CAS) Banned :** `Couldn't Fetch`"
    caption = """**Info of [{}](tg://user?id={}):
   -🔖ID : **`{}`
   **-**👥**Groups in Common : **`{}`
   **-**🌏**Data Centre Number : **`{}`
   **-**🔏**Restricted by telegram : **`{}`
   **-**🦅{}
   **-**👮‍♂️{}
""".format(
        first_name,
        user_id,
        user_id,
        common_chats,
        dc_id,
        replied_user.user.restricted,
        sw,
        cas,
    )
    await edit_or_reply(event, caption)


async def get_full_user(event):
    input_str = event.pattern_match.group(1)
    if input_str:
        try:
            try:
                input_str = int(input_str)
            except Exception as e:
                LOGS.info(str(e))
            user_object = await event.client.get_entity(input_str)
            user_id = user_object.id
            replied_user = await event.client(GetFullUserRequest(user_id))
            return replied_user, None
        except Exception as e:
            return None, e
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.from_id is None and not event.is_private:
            return None, "Well that's an anonymous admin. I can't fetch details!"
        if previous_message.forward:
            replied_user = await event.client(
                GetFullUserRequest(
                    previous_message.forward.sender_id
                    or previous_message.forward.channel_id
                )
            )
            return replied_user, None
        replied_user = await event.client(
            GetFullUserRequest(previous_message.sender_id)
        )
        return replied_user, None
    if event.is_private:
        try:
            user_id = event.chat_id
            replied_user = await event.client(GetFullUserRequest(user_id))
            return replied_user, None
        except Exception as e:
            return None, e
    return None, "No input is found"


@bot.on(admin_cmd(pattern="whois(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="whois(?: |$)(.*)", allow_sudo=True))
async def who(event):
    cat = await edit_or_reply(event, "`Fetching userinfo wait....`")
    if not os.path.isdir(TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TMP_DOWNLOAD_DIRECTORY)
    replied_user = await get_user(event)
    if replied_user is None:
        return await edit_or_reply(
            cat, "`Well that's an anonymous admin. I can't fetch details!`"
        )
    try:
        photo, caption = await fetch_info(replied_user, event)
    except AttributeError:
        await edit_or_reply(cat, "`Could not fetch info of that user.`")
        return
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = None
    try:
        await event.client.send_file(
            event.chat_id,
            photo,
            caption=caption,
            link_preview=False,
            force_document=False,
            reply_to=message_id_to_reply,
            parse_mode="html",
        )
        if not photo.startswith("http"):
            os.remove(photo)
        await cat.delete()
    except TypeError:
        await cat.edit(caption, parse_mode="html")


async def get_user(event):
    """Get the user from argument or replied message."""
    if event.reply_to_msg_id and not event.pattern_match.group(1):
        previous_message = await event.get_reply_message()
        if previous_message.from_id is None and not event.is_private:
            return None
        replied_user = await event.client(
            GetFullUserRequest(previous_message.sender_id)
        )
    else:
        user = event.pattern_match.group(1)
        if user.isnumeric():
            user = int(user)
        if not user:
            self_user = await event.client.get_me()
            user = self_user.id
        if event.message.entities:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user
        try:
            user_object = await event.client.get_entity(user)
            replied_user = await event.client(GetFullUserRequest(user_object.id))
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None
    return replied_user


async def fetch_info(replied_user, event):
    """Get details from the User object."""
    replied_user_profile_photos = await event.client(
        GetUserPhotosRequest(
            user_id=replied_user.user.id, offset=42, max_id=0, limit=80
        )
    )
    replied_user_profile_photos_count = "User haven't set profile pic"
    try:
        replied_user_profile_photos_count = replied_user_profile_photos.count
    except AttributeError:
        pass
    user_id = replied_user.user.id
    first_name = replied_user.user.first_name
    last_name = replied_user.user.last_name
    try:
        dc_id, location = get_input_location(replied_user.profile_photo)
    except Exception:
        dc_id = "Couldn't fetch DC ID!"
    common_chat = replied_user.common_chats_count
    username = replied_user.user.username
    user_bio = replied_user.about
    is_bot = replied_user.user.bot
    restricted = replied_user.user.restricted
    verified = replied_user.user.verified
    photo = await event.client.download_profile_photo(
        user_id, TMP_DOWNLOAD_DIRECTORY + str(user_id) + ".jpg", download_big=True
    )
    first_name = (
        first_name.replace("\u2060", "")
        if first_name
        else ("This User has no First Name")
    )
    last_name = last_name.replace("\u2060", "") if last_name else (" ")
    username = "@{}".format(username) if username else ("This User has no Username")
    user_bio = "This User has no About" if not user_bio else user_bio
    caption = "<b><i>USER INFO from Durov's Database :</i></b>\n\n"
    caption += f"<b>👤 First Name:</b> {first_name} {last_name}\n"
    caption += f"<b>🤵 Username:</b> {username}\n"
    caption += f"<b>🔖 ID:</b> <code>{user_id}</code>\n"
    caption += f"<b>🌏 Data Centre ID:</b> {dc_id}\n"
    caption += f"<b>🖼 Number of Profile Pics:</b> {replied_user_profile_photos_count}\n"
    caption += f"<b>🤖 Is Bot:</b> {is_bot}\n"
    caption += f"<b>🔏 Is Restricted:</b> {restricted}\n"
    caption += f"<b>🌐 Is Verified by Telegram:</b> {verified}\n\n"
    caption += f"<b>✍️ Bio:</b> \n<code>{user_bio}</code>\n\n"
    caption += f"<b>👥 Common Chats with this user:</b> {common_chat}\n"
    caption += f"<b>🔗 Permanent Link To Profile:</b> "
    caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'
    return photo, caption


@bot.on(admin_cmd(pattern="link(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="link(?: |$)(.*)", allow_sudo=True))
async def permalink(mention):
    """For .link command, generates a link to the user's PM with a custom text."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if custom:
        await edit_or_reply(mention, f"[{custom}](tg://user?id={user.id})")
    else:
        tag = (
            user.first_name.replace("\u2060", "") if user.first_name else user.username
        )
        await edit_or_reply(mention, f"[{tag}](tg://user?id={user.id})")


async def ge(user, event):
    if isinstance(user, str):
        user = int(user)
    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None
    return user_obj


CMD_HELP.update(
    {
        "whois": "**Plugin : **`whois`\
    \n\n  •  **Syntax : **`.whois <username> or reply to someones text with .whois`\
    \n  •  **Function : **__Gets info of an user.__\
    \n\n  •  **Syntax : **`.userinfo <username> or reply to someones text with .userinfo`\
    \n  •  **Function : **__Gets information of an user such as restrictions ban by spamwatch or cas__\
    \n\n  •  **Syntax : **`.link id/username/reply`\
    \n  •  **Function : **__Generates a link to the user's PM .__"
    }
)
