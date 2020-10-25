import string

from ..utils import admin_cmd, edit_or_reply, sudo_cmd
from . import CMD_HELP

msg_cache = {}


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
    try:
        await event.delete()
    except:
        pass
    m = await event.get_reply_message()
    if not m:
        return
    await event.respond(m)


@bot.on(admin_cmd(pattern=r"fpost\s+(.*)"))
@bot.on(sudo_cmd(pattern="fpost\s+(.*)", allow_sudo=True))
async def _(event):
    await event.delete()
    text = event.pattern_match.group(1)
    destination = await event.get_input_chat()
    for c in text.lower():
        if c not in string.ascii_lowercase:
            continue
        if c not in msg_cache:
            async for msg in event.client.iter_messages(None, search=c):
                if msg.raw_text.lower() == c and msg.media is None:
                    msg_cache[c] = msg
                    break
        await event.client.forward_messages(destination, msg_cache[c])


CMD_HELP.update(
    {
        "forward": "**Plugin : **`forward`\
    \n\n**Synatax : **`frwd reply to any message`\
    \n**Function :  **__Enable Seen Counter in any message, to know how many users have seen your message__\
    \n\n**Syntax : **`.resend reply to message`\
    \n**Function : **__Just resend the replied message again in that chat__\
    \n\n**Syntax : **`.fpost text`\
    \n**Function : **__Split the word and forwards each letter from the messages cache if exists__"
    }
)
