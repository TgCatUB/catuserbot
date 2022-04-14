"""command: .hack & .thack """
# thx to @r4v4n4
import asyncio

from userbot import catub

from ..core.managers import edit_or_reply
from ..helpers.utils import _format
from . import ALIVE_NAME

plugin_category = "fun"


@catub.cat_cmd(
    pattern="hack$",
    command=("hack", plugin_category),
    info={
        "header": "Fun hack animation.",
        "description": "Reply to user to show hack animation",
        "note": "This is just for fun. Not real hacking.",
        "usage": "{tr}hack",
    },
)
async def _(event):
    "Fun hack animation."
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        idd = reply_message.sender_id
        if idd == 1035034432:
            await edit_or_reply(
                event, "This is My Master\nI can't hack my master's Account"
            )
        else:
            event = await edit_or_reply(event, "Hacking..")
            animation_chars = [
                "`Connecting To Hacked Private Server...`",
                "`Target Selected.`",
                "`Hacking... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
                "`Hacking... 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
                "`Hacking... 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
                "`Hacking... 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
                "`Hacking... 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
                "`Hacking... 52%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ `",
                "`Hacking... 84%\n█████████████████████▒▒▒▒ `",
                "`Hacking... 100%\n█████████HACKED███████████ `",
                f"`Targeted Account Hacked...\n\nPay 69$ To` {ALIVE_NAME} . `To Remove this hack..`",
            ]
            animation_interval = 3
            animation_ttl = range(11)
            for i in animation_ttl:
                await asyncio.sleep(animation_interval)
                await event.edit(animation_chars[i % 11])
    else:
        await edit_or_reply(
            event,
            "No User is Defined\n Can't hack account",
            parse_mode=_format.parse_pre,
        )


@catub.cat_cmd(
    pattern="thack$",
    command=("thack", plugin_category),
    info={
        "header": "Fun Telegram hack animation.",
        "description": "Reply to user to show telegram hack animation",
        "note": "This is just for fun. Not real hacking.",
        "usage": "{tr}thack",
    },
)
async def _(event):
    "Fun Telegram hack animation."
    animation_interval = 2
    animation_ttl = range(12)
    event = await edit_or_reply(event, "thack")
    animation_chars = [
        "**Connecting To Telegram Data Centre**",
        f"Target Selected By Hacker: {ALIVE_NAME}",
        "`Hacking... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `\n\n\n  TERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)",
        "`Hacking... 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `\n\n\n  TERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\nCollecting Data Package",
        "`Hacking... 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `\n\n\n  TERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\nCollecting Data Package\n  Downloading Telegram-Data-Sniffer-7.1.1-py2.py3-none-any.whl (82 kB)",
        "`Hacking... 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `\n\n\n  TERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\nCollecting Data Package\n  Downloading Telegram-Data-Sniffer-7.1.1-py2.py3-none-any.whl (82 kB)\nBuilding wheel for Tg-Bruteforcing (setup.py): finished with status 'done'",
        "`Hacking... 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `\n\n\n  TERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\nCollecting Data Package\n  Downloading Telegram-Data-Sniffer-7.1.1-py2.py3-none-any.whl (82 kB)\nBuilding wheel for Tg-Bruteforcing (setup.py): finished with status 'done'\nCreated wheel for telegram: filename=Telegram-Data-Sniffer-0.0.1-py3-none-any.whl size=1306 sha256=cb224caad7fe01a6649188c62303cd4697c1869fa12d280570bb6ac6a88e6b7e",
        "`Hacking... 52%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ `\n\n\n  TERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\nCollecting Data Package\n  Downloading Telegram-Data-Sniffer-7.1.1-py2.py3-none-any.whl (82 kB)\nBuilding wheel for Tg-Bruteforcing (setup.py): finished with status 'done'\nCreated wheel for telegram: filename=Telegram-Data-Sniffer-0.0.1-py3-none-any.whl size=1306 sha256=cb224caad7fe01a6649188c62303cd4697c1869fa12d280570bb6ac6a88e6b7e\n  Stored in directory: /app/.cache/pip/wheels/a2/9f/b5/650dd4d533f0a17ca30cc11120b176643d27e0e1f5c9876b5b",
        "`Hacking... 84%\n█████████████████████▒▒▒▒ `\n\n\n  TERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\nCollecting Data Package\n  Downloading Telegram-Data-Sniffer-7.1.1-py2.py3-none-any.whl (82 kB)\nBuilding wheel for Tg-Bruteforcing (setup.py): finished with status 'done'\nCreated wheel for telegram: filename=Telegram-Data-Sniffer-0.0.1-py3-none-any.whl size=1306 sha256=cb224caad7fe01a6649188c62303cd4697c1869fa12d280570bb6ac6a88e6b7e\n  Stored in directory: /app/.cache/pip/wheels/a2/9f/b5/650dd4d533f0a17ca30cc11120b176643d27e0e1f5c9876b5b\n\n **Successfully Hacked Telegram Server Database**",
        "`Hacking... 100%\n█████████HACKED███████████ `\n\n\n  TERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\nCollecting Data Package\n  Downloading Telegram-Data-Sniffer-7.1.1-py2.py3-none-any.whl (82 kB)\nBuilding wheel for Tg-Bruteforcing (setup.py): finished with status 'done'\nCreated wheel for telegram: filename=Telegram-Data-Sniffer-0.0.1-py3-none-any.whl size=1306 sha256=cb224caad7fe01a6649188c62303cd4697c1869fa12d280570bb6ac6a88e6b7e\n  Stored in directory: /app/.cache/pip/wheels/a2/9f/b5/650dd4d533f0a17ca30cc11120b176643d27e0e1f5c9876b5b\n\n **Successfully Hacked Telegram Server Database**\n\n\n🔹Output: Generating.....",
        f"`Targeted Account Hacked...\n\nPay 699$ To` {ALIVE_NAME} .`To Remove This Hack`\n\n\n  TERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\nCollecting Data Package\n  Downloading Telegram-Data-Sniffer-7.1.1-py2.py3-none-any.whl (82 kB)\nBuilding wheel for Tg-Bruteforcing (setup.py): finished with status 'done'\nCreated wheel for telegram: filename=Telegram-Data-Sniffer-0.0.1-py3-none-any.whl size=1306 sha256=cb224caad7fe01a6649188c62303cd4697c1869fa12d280570bb6ac6a88e6b7e\n  Stored in directory: /app/.cache/pip/wheels/a2/9f/b5/650dd4d533f0a17ca30cc11120b176643d27e0e1f5c9876b5b\n\n **Successfully Hacked Telegram Server Database**\n\n\n🔹**Output:** Successful",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 11])


@catub.cat_cmd(
    pattern="wahack$",
    command=("wahack", plugin_category),
    info={
        "header": "Fun Whatsapp hack animation.",
        "description": "Reply to user to show Whatsapp hack animation",
        "note": "This is just for fun. Not real hacking.",
        "usage": "{tr}wahack",
    },
)
async def _(event):
    "Fun Whatsapp hack animation."
    animation_interval = 2
    animation_ttl = range(15)
    event = await edit_or_reply(event, "wahack..")
    animation_chars = [
        "Looking for WhatsApp databases in targeted person...",
        " User online: True\nTelegram access: True\nRead Storage: True ",
        "Hacking... 0%\n[░░░░░░░░░░░░░░░░░░░░]\n`Looking for WhatsApp...`\nETA: 0m, 30s",
        "Hacking... 11.07%\n[██░░░░░░░░░░░░░░░░░░]\n`Looking for WhatsApp...`\nETA: 0m, 27s",
        "Hacking... 20.63%\n[███░░░░░░░░░░░░░░░░░]\n`Found folder C:/WhatsApp`\nETA: 0m, 24s",
        "Hacking... 34.42%\n[█████░░░░░░░░░░░░░░░]\n`Found folder C:/WhatsApp`\nETA: 0m, 21s",
        "Hacking... 42.17%\n[███████░░░░░░░░░░░░░]\n`Searching for databases`\nETA: 0m, 18s",
        "Hacking... 55.30%\n[█████████░░░░░░░░░░░]\n`Found msgstore.db.crypt12`\nETA: 0m, 15s",
        "Hacking... 64.86%\n[███████████░░░░░░░░░]\n`Found msgstore.db.crypt12`\nETA: 0m, 12s",
        "Hacking... 74.02%\n[█████████████░░░░░░░]\n`Trying to Decrypt...`\nETA: 0m, 09s",
        "Hacking... 86.21%\n[███████████████░░░░░]\n`Trying to Decrypt...`\nETA: 0m, 06s",
        "Hacking... 93.50%\n[█████████████████░░░]\n`Decryption successful!`\nETA: 0m, 03s",
        "Hacking... 100%\n[████████████████████]\n`Scanning file...`\nETA: 0m, 00s",
        "Hacking complete!\nUploading file...",
        "Targeted Account Hacked...!\n\n ✅ File has been successfully uploaded to my server.\nWhatsApp Database:\n`./DOWNLOADS/msgstore.db.crypt12`",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 15])
