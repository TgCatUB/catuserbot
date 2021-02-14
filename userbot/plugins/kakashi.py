# created by @Jisan7509

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError


@bot.on(admin_cmd(outgoing=True, pattern="note_help$"))
@bot.on(sudo_cmd(outgoing=True, pattern="note_help$", allow_sudo=True))
async def kakashi(jisan):
    await edit_or_reply(
        jisan, "All commands for note is [HERE](https://nekobin.com/pizacisawi) "
    )


@bot.on(admin_cmd(pattern="note(?: |$)(.*)", outgoing=True))
@bot.on(sudo_cmd(outgoing=True, pattern="note(?: |$)(.*)", allow_sudo=True))
async def kakashi(event):
    if event.fwd_from:
        return
    reply_to_id = await reply_id(event)
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
    elif link in ("customalivetext", "cat"):
        link = "Custom Alive Text"
    elif link in ("customaliveemoji", "cae"):
        link = "Custom Alive Emoji"
    elif link == "rmbg":
        link = "Rmbg"
    elif link in ("lastfm", "lf"):
        link = "LastFm"
    elif link == "goodcat":
        link = "🐱 Cat UserBot 🐱"
    elif link == "badcat":
        link = "My Repo"
    catevent = await edit_or_reply(event, "```Sending your note....```")
    async with event.client.conversation("@kakashi_robot") as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=1117359246)
            )
            msg = await conv.send_message(f"{link}")
            response = await response
        except YouBlockedUserError:
            await catevent.edit("```Unblock @kakashi_robot plox```")
            return
        else:
            await catevent.delete()
            await event.client.send_message(
                event.chat_id,
                response.message,
                reply_to=reply_to_id,
            )
            await event.client.send_read_acknowledge(conv.chat_id)
        await event.client.delete_messages(conv.chat_id, [msg.id, response.id])


CMD_HELP.update(
    {
        "kakashi": "__**PLUGIN NAME :** Kakashi__\
    \n\n📌** CMD ➥** `.note_help` \
    \n**USAGE   ➥  **To get code name list of notes present in kakashi.\
    \n\n📌** CMD ➥** `.note <name of note or give it's code name>`\
    \n**USAGE   ➥  **Type .note_name/note_code to get the corresponding note.\
    \n\n**Example:** `.note ap` , this will send you note on how to set alive pic."
    }
)
