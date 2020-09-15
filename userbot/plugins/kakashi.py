# created by @Jisan7509

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import bot
from userbot.events import register
from userbot.utils import admin_cmd


@borg.on(admin_cmd(outgoing=True, pattern="note_help$"))
async def kakashi(jisan):
    await jisan.edit("All commands for note is [HERE](https://nekobin.com/xihitanafu) ")


@register(outgoing=True, pattern="^.note(?: |$)(.*)")
async def kakashi(event):
    if event.fwd_from:
        return
    link = event.pattern_match.group(1)
    if link in ("alivepic", "ap"):
        link = "Alive Picture"
    elif link in ("autoname", "an"):
        link = "Auto Name"
    elif link == "bloom":
        link = "Bloom / Colour DP"
    elif link in ("customrowcolumn", "crc"):
        link = "Custom Row & Coloum"
    elif link in ("helpemoji", "he"):
        link = "Help Menu Emoji"
    elif link in ("gdrive", "gd"):
        link = "G-Drive Setup"
    elif link in ("github", "gh"):
        link = "Github Commit"
    elif link == "lydia":
        link = "Lydia Setup"
    elif link in ("handler", "ch"):
        link = "Custom Handler"
    elif link == "ocr":
        link = "OCR Setup"
    elif link in ("pmlogger", "pl"):
        link = "PM Logger"
    elif link in ("pmpermit", "pp"):
        link = "PM Permit"
    elif link in ("pmpermitpic", "ppp"):
        link = "Pm Permit Pic"
    elif link in ("speechtotext", "stt"):
        link = "Speech To Text"
    elif link == "sudo":
        link = "Add Sudo"
    elif link in ("youtube", "yts"):
        link = "Youtube Search"
    elif link in ("updater", "ud"):
        link = "Setup Updater"
    elif link in ("weather", "ws"):
        link = "Weather Setup"
    elif link in ("forward", "frwd"):
        link = "Forward"
    elif link in ("custompmtext", "cppt"):
        link = "Custom PM Permit Text"
    elif link in ("liveusername", "lu"):
        link = "Live Username"
    elif link in ("customalivetext", "cat"):
        link = "Custom Alive Text"
    elif link in ("customaliveemoji", "cae"):
        link = "Custom Alive Emoji"
    elif link == "goodcat":
        link = "🐱 Cat UserBot 🐱"
    elif link == "badcat":
        link = "My Repo"
    await event.edit("```Sending your note....```")
    async with bot.conversation("@kakashi_robot") as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=1117359246)
            )
            await conv.send_message(f"{link}")
            response = await response
        except YouBlockedUserError:
            await event.reply("```Unblock @kakashi_robot plox```")
            return
        else:
            await event.delete()
            await bot.forward_messages(event.chat_id, response.message)
