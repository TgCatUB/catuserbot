import asyncio
import io
import userbot.plugins.sql_helper.no_log_pms_sql as no_log_pms_sql
from telethon import events, functions, types
from userbot.utils import admin_cmd

PM_WARNS = {}
PREV_REPLY_MESSAGE = {}

if Config.DUAL_LOG:
    @borg.on(admin_cmd(pattern="nccreatedch$"))
    async def create_dump_channel(event):
        if Config.PM_LOGGR_BOT_API_ID is None:
            result = await event.client(functions.channels.CreateChannelRequest(  # pylint:disable=E0602
                title=f"catuserbot-{borg.uid}-PM_LOGGR_BOT_API_ID-data",
                about=" PM_LOGGR_BOT_API_ID // Do Not Touch",
                megagroup=False
            ))
            logger.info(result)
            created_chat_id = result.chats[0].id
            result = await event.client.edit_admin(  # pylint:disable=E0602
                entity=created_chat_id,
                user=Config.TG_BOT_USER_NAME_BF_HER,
                is_admin=True,
                title="Editor"
            )
            logger.info(result)
            with io.BytesIO(str.encode(str(created_chat_id))) as out_file:
                out_file.name = "PLEASE.IGNORE.dummy.file"
                await event.client.send_file(
                    created_chat_id,
                    out_file,
                    force_document=True,
                    allow_cache=False,
                    caption=f"Please set `PM_LOGGR_BOT_API_ID` to `{created_chat_id}`",
                    reply_to=1
                )
            await event.delete()
        else:
            await event.edit(f"**is configured**. [please do not touch](https://t.me/c/{Config.PM_LOGGR_BOT_API_ID}/2)")

    @borg.on(admin_cmd(pattern="nolog(?: |$)(.*)"))
    async def set_no_log_p_m(event):
        if Config.PM_LOGGR_BOT_API_ID is not None:
            event.pattern_match.group(1)
            chat = await event.get_chat()
            if event.is_private:
                if not no_log_pms_sql.is_approved(chat.id):
                    no_log_pms_sql.approve(chat.id)
                    await event.edit("Won't Log Messages from this chat")
                    await asyncio.sleep(3)
                    await event.delete()

    @borg.on(admin_cmd(pattern="log(?: |$)(.*)"))
    async def set_no_log_p_m(event):
        if Config.PM_LOGGR_BOT_API_ID is not None:
            event.pattern_match.group(1)
            chat = await event.get_chat()
            if event.is_private:
                if no_log_pms_sql.is_approved(chat.id):
                    no_log_pms_sql.disapprove(chat.id)
                    await event.edit("Will Log Messages from this chat")
                    await asyncio.sleep(3)
                    await event.delete()

    @borg.on(events.NewMessage(incoming=True))
    async def on_new_private_message(event):
        if Config.PM_LOGGR_BOT_API_ID is None:
            return
        if not event.is_private:
            return
        if event.from_id == bot.uid:
            return
        message_text = event.message.message
        message_media = event.message.media
        event.message.id
        event.message.to_id
        chat_id = event.from_id
        # logger.info(chat_id)
        sender = await event.client.get_entity(chat_id)
        if chat_id == borg.uid:
            # don't log Saved Messages
            return
        if sender.bot:
            # don't log bots
            return
        if sender.verified:
            # don't log verified accounts
            return
        if not no_log_pms_sql.is_approved(chat_id):
            # log pms
            await do_log_pm_action(chat_id, event, message_text, message_media)

    @borg.on(events.ChatAction(blacklist_chats=Config.UB_BLACK_LIST_CHAT))
    async def on_new_chat_action_message(event):
        if Config.PM_LOGGR_BOT_API_ID is None:
            return
        # logger.info(event.stringify())
        chat_id = event.chat_id
        if event.created or event.user_added:
            added_by_users = event.action_message.action.users
            if borg.uid in added_by_users:
                message_id = event.action_message.id
                added_by_user = event.action_message.from_id
                # someone added me to chat
                the_message = ""
                the_message += "#MessageActionChatAddUser\n\n"
                the_message += f"[User](tg://user?id={added_by_user}): `{added_by_user}`\n"
                the_message += f"[Private Link](https://t.me/c/{chat_id}/{message_id})\n"
                await event.client.send_message(
                    entity=Config.PM_LOGGR_BOT_API_ID,
                    message=the_message,
                    # reply_to=,
                    # parse_mode="html",
                    link_preview=False,
                    # file=message_media,
                    silent=True
                )

    @borg.on(events.Raw())
    async def on_new_channel_message(event):
        if Config.PM_LOGGR_BOT_API_ID is None:
            return
        try:
            if tgbot is None:
                return
        except Exception as e:
            logger.info(str(e))
            return
        # logger.info(event.stringify())
        if isinstance(event, types.UpdateChannel):
            channel_id = event.channel_id
            message_id = 2
            # someone added me to channel
            # TODO: https://t.me/TelethonChat/153947
            the_message = ""
            the_message += "#MessageActionChatAddUser\n\n"
            # the_message += f"[User](tg://user?id={added_by_user}): `{added_by_user}`\n"
            the_message += f"[Private Link](https://t.me/c/{channel_id}/{message_id})\n"
            await borg.send_message(
                entity=Config.PM_LOGGR_BOT_API_ID,
                message=the_message,
                # reply_to=,
                # parse_mode="html",
                link_preview=False,
                # file=message_media,
                silent=True
            )

    async def do_log_pm_action(chat_id, event, message_text, message_media):
        the_message = ""
        the_message += "#LOG_PMs\n\n"
        the_message += f"[User](tg://user?id={chat_id}): {chat_id}\n"
        the_message += f"Message: {message_text}\n"
        #the_message += f"Media: {message_media}"
        if event.message.message:
            await event.client.send_message(
                entity=Config.PM_LOGGR_BOT_API_ID,
                message=the_message,
                # reply_to=,
                # parse_mode="html",
                link_preview=False,
                file=message_media,
                silent=True
            )
        else:
            return
