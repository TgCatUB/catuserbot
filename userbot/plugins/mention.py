# Some are ported from uniborg By: @INF1N17Y

from telethon.tl.types import ChannelParticipantsAdmins

from ..utils import admin_cmd, edit_or_reply, sudo_cmd


@bot.on(admin_cmd(pattern="tagall$"))
@bot.on(sudo_cmd(pattern="tagall$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    mentions = "@all"
    chat = await event.get_input_chat()
    async for x in event.client.iter_participants(chat, 100):
        mentions += f"[\u2063](tg://user?id={x.id})"
    await reply_to_id.reply(mentions)
    await event.delete()


@bot.on(admin_cmd(pattern="all (.*)"))
@bot.on(sudo_cmd(pattern="all (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    input_str = event.pattern_match.group(1)

    if not input_str:
        return await edit_or_reply(event, "what should i do try `.all hello`.")

    mentions = input_str
    chat = await event.get_input_chat()
    async for x in event.client.iter_participants(chat, 100):
        mentions += f"[\u2063](tg://user?id={x.id})"
    await reply_to_id.reply(mentions)
    await event.delete()


@bot.on(admin_cmd(pattern="admins$"))
@bot.on(sudo_cmd(pattern="admins$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    mentions = "@admin: **Spam Spotted**"
    chat = await event.get_input_chat()
    async for x in event.client.iter_participants(
        chat, filter=ChannelParticipantsAdmins
    ):
        mentions += f"[\u2063](tg://user?id={x.id})"
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()


@bot.on(admin_cmd(pattern="men (.*)"))
@bot.on(sudo_cmd(pattern="men (.*)", allow_sudo=True))
async def _(event):
    input_str = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        reply_msg = await event.get_reply_message()
        u = reply_msg.sender_id
        str = input_str
    else:
        user, str = input_str.split(" ", 1)
        try:
            u = int(user)
        except ValueError:
            try:
                u = await event.client.get_entity(user)
            except ValueError:
                await event.delete()
                return
            u = int(u.id)
        except:
            await event.delete()
            return
    await event.delete()
    await event.client.send_message(
        event.chat_id, f"<a href='tg://user?id={u}'>{str}</a>", parse_mode="HTML"
    )
