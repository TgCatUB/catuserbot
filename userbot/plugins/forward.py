import string

from telethon.tl.types import Channel

from ..utils import admin_cmd, edit_or_reply, sudo_cmd
from . import CMD_HELP

global msg_cache
msg_cache = {}


global groupsid
groupsid = []


async def all_groups_id(cat):
    catgroups = []
    async for dialog in cat.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel) and entity.megagroup:
            catgroups.append(entity.id)
    return catgroups


@bot.on(admin_cmd(pattern="frwd$"))
@bot.on(sudo_cmd(pattern="frwd$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if Config.PRIVATE_CHANNEL_BOT_API_ID is None:
        await edit_or_reply(
            event,
            "Please set the required environment variable `PRIVATE_CHANNEL_BOT_API_ID` for this plugin to work",
        )
        return
    try:
        e = await event.client.get_entity(Config.PRIVATE_CHANNEL_BOT_API_ID)
    except Exception as e:
        await edit_or_reply(event, str(e))
    else:
        re_message = await event.get_reply_message()
        # https://t.me/telethonofftopic/78166
        fwd_message = await event.client.forward_messages(e, re_message, silent=True)
        await event.client.forward_messages(event.chat_id, fwd_message)
        await event.delete()


@bot.on(admin_cmd(pattern="resend$"))
@bot.on(sudo_cmd(pattern="resend$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    try:
        await event.delete()
    except:
        pass
    m = await event.get_reply_message()
    if not m:
        return
    await event.respond(m)


@bot.on(admin_cmd(pattern=r"fpost (.*)"))
@bot.on(sudo_cmd(pattern=r"fpost (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    global groupsid
    global msg_cache
    await event.delete()
    text = event.pattern_match.group(1)
    destination = await event.get_input_chat()
    if len(groupsid) == 0:
        groupsid = await all_groups_id(event)
    for c in text.lower():
        if c not in string.ascii_lowercase:
            continue
        if c not in msg_cache:
            async for msg in event.client.iter_messages(event.chat_id, search=c):
                if msg.raw_text.lower() == c and msg.media is None:
                    msg_cache[c] = msg
                    break
        if c not in msg_cache:
            for i in groupsid:
                async for msg in event.client.iter_messages(event.chat_id, search=c):
                    if msg.raw_text.lower() == c and msg.media is None:
                        msg_cache[c] = msg
                        break
        await event.client.forward_messages(destination, msg_cache[c])


CMD_HELP.update(
    {
        "forward": "__**PLUGIN NAME :** Forward__\
    \n\n📌** CMD ➥** `.frwd` <reply to any message>\
    \n**USAGE   ➥  **Enable Seen Counter in any message, to know how many users have seen your message\
    \n\n📌** CMD ➥** `.resend` reply to message\
    \n**USAGE   ➥  **Just resend the replied message again in that chat__\
    \n\n📌** CMD ➥** `.fpost text`\
    \n**USAGE   ➥  **Split the word and forwards each letter from the messages cache if exists "
    }
)
