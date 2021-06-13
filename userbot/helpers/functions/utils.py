import time
from datetime import datetime

from emoji import get_emoji_regexp
from telethon.tl.types import Channel, PollAnswer


async def get_message_link(channelid, msgid):
    if str(channelid).startswith("-"):
        channelid = str(channelid)[1:]
    if channelid.startswith("100"):
        channelid = channelid[3:]
    return f"https://t.me/c/{channelid}/{msgid}"


def utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(
        now_timestamp
    )
    return utc_datetime + offset


async def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    hmm = len(time_list)
    for x in range(hmm):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "
    time_list.reverse()
    up_time += ":".join(time_list)
    return up_time


# gban


async def admin_groups(catub):
    catgroups = []
    async for dialog in catub.iter_dialogs():
        entity = dialog.entity
        if (
            isinstance(entity, Channel)
            and entity.megagroup
            and (entity.creator or entity.admin_rights)
        ):
            catgroups.append(entity.id)
    return catgroups


# https://github.com/pokurt/LyndaRobot/blob/7556ca0efafd357008131fa88401a8bb8057006f/lynda/modules/helper_funcs/string_handling.py#L238


async def extract_time(cat, time_val):
    if any(time_val.endswith(unit) for unit in ("s", "m", "h", "d", "w")):
        unit = time_val[-1]
        time_num = time_val[:-1]  # type: str
        if not time_num.isdigit():
            await cat.edit("Invalid time amount specified.")
            return None
        if unit == "s":
            bantime = int(time.time() + int(time_num) * 1)
        elif unit == "m":
            bantime = int(time.time() + int(time_num) * 60)
        elif unit == "h":
            bantime = int(time.time() + int(time_num) * 60 * 60)
        elif unit == "d":
            bantime = int(time.time() + int(time_num) * 24 * 60 * 60)
        elif unit == "w":
            bantime = int(time.time() + int(time_num) * 7 * 24 * 60 * 60)
        else:
            # how even...?
            await cat.edit(
                f"__Invalid time type specified. Expected s,  m , h , d or w but got:__ {time_val[-1]}"
            )
            return None
        return bantime
    await cat.edit(
        f"__Invalid time type specified. Expected s,  m , h , d or w but got: __{time_val[-1]}"
    )
    return None


def Build_Poll(options):
    return [PollAnswer(option, bytes(i)) for i, option in enumerate(options, start=1)]


def deEmojify(inputString: str) -> str:
    """Remove emojis and other non-safe characters from string"""
    return get_emoji_regexp().sub("", inputString)
