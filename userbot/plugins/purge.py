# Userbot module for purging unneeded messages(usually spam or ot).

from asyncio import sleep

from telethon.errors import rpcbaseerrors

from ..utils import errors_handler
from . import BOTLOG, BOTLOG_CHATID


@bot.on(admin_cmd(outgoing=True, pattern="purge(?: |$)(.*)"))
@bot.on(sudo_cmd(allow_sudo=True, pattern="purge(?: |$)(.*)"))
@errors_handler
async def fastpurger(event):
    chat = await event.get_input_chat()
    msgs = []
    count = 0
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if reply:
        if input_str and input_str.isnumeric():
            async for msg in event.client.iter_messages(
                event.chat_id,
                limit=(int(input_str) - 1),
                offset_id=reply.id,
                reverse=True,
            ):
                msgs.append(msg)
                count += 1
                msgs.append(event.reply_to_msg_id)
                if len(msgs) == 100:
                    await event.client.delete_messages(chat, msgs)
                    msgs = []
        elif input_str:
            return await edit_or_reply(
                event, f"**Error**\n`{input_str} is not an integer. Use proper syntax.`"
            )
        else:
            async for msg in event.client.iter_messages(
                chat, min_id=event.reply_to_msg_id
            ):
                msgs.append(msg)
                count += 1
                msgs.append(event.reply_to_msg_id)
                if len(msgs) == 100:
                    await event.client.delete_messages(chat, msgs)
                    msgs = []
    else:
        await edit_or_reply(
            event,
            "`No message specified.`",
        )
        return
    if msgs:
        await event.client.delete_messages(chat, msgs)
    done = await event.client.send_message(
        event.chat_id,
        "`Fast purge complete!\nPurged " + str(count) + " messages.`",
    )
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#PURGE \n`Purge of " + str(count) + " messages done successfully.`",
        )
    await sleep(2)
    await done.delete()


@bot.on(admin_cmd(outgoing=True, pattern="purgeme"))
@bot.on(sudo_cmd(allow_sudo=True, pattern="purgeme"))
@errors_handler
async def purgeme(event):
    message = event.text
    count = int(message[9:])
    i = 1

    async for message in event.client.iter_messages(event.chat_id, from_user="me"):
        if i > count + 1:
            break
        i += 1
        await message.delete()

    smsg = await event.client.send_message(
        event.chat_id,
        "`Purge complete!` Purged " + str(count) + " messages.",
    )
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#PURGEME \nPurge of " + str(count) + " messages done successfully.",
        )
    await sleep(2)
    i = 1
    await smsg.delete()


@bot.on(admin_cmd(outgoing=True, pattern="del$"))
@bot.on(sudo_cmd(allow_sudo=True, pattern="del$"))
@errors_handler
async def delete_it(event):
    msg_src = await event.get_reply_message()
    if event.reply_to_msg_id:
        try:
            await msg_src.delete()
            if BOTLOG:
                await event.client.send_message(
                    BOTLOG_CHATID, "#DEL \n`Deletion of message was successful`"
                )
        except rpcbaseerrors.BadRequestError:
            await edit_or_reply(event, "`Well, I can't delete a message`")
    else:
        await event.delete()


CMD_HELP.update(
    {
        "purge": "**Plugin : **`purge`\
        \n\n•  **Syntax : **`.purge reply to message to start purge from there`\
        \n•  **Function : **__Purges all messages starting from the reply.__\
        \n\n•  **Syntax : **`.purgeme <x>`\
        \n•  **Function : **__Deletes x amount of your latest messages.__\
        \n\n•  **Syntax : **`.del reply to message to delete`\
        \n•  **Function : **__Deletes the message you replied to.__"
    }
)
