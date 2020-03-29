import asyncio
from telethon import events
from telethon.tl.functions.channels import EditBannedRequest
from userbot.utils import admin_cmd


userbot.storage.CHAT_FLOOD = {}  # pylint:disable=E0602


@borg.on(events.NewMessage(chats=Config.CHATS_TO_MONITOR_FOR_ANTI_FLOOD))  # pylint:disable=E0602
async def _(event):
    if not event.chat_id in userbot.storage.CHAT_FLOOD:  # pylint:disable=E0602
        borg.storage.CHAT_FLOOD[event.chat_id] = {}  # pylint:disable=E0602
    if event.chat_id in userbot.storage.CHAT_FLOOD:  # pylint:disable=E0602
        try:
            # pylint:disable=E0602
            max_count = int(userbot.storage.CHAT_FLOOD[event.chat_id][2]) or \
            Config.MAX_ANTI_FLOOD_MESSAGES  # pylint:disable=E0602
        except KeyError:
            max_count = Config.MAX_ANTI_FLOOD_MESSAGES  # pylint:disable=E0602
        # pylint:disable=E0602
        if event.message.from_id in userbot.storage.CHAT_FLOOD[event.chat_id]:
            current_count = int(userbot.storage.CHAT_FLOOD[event.chat_id][1])
            current_count += 1
            if current_count > max_count:
                try:
                    await borg(EditBannedRequest(
                        event.chat_id,
                        event.message.from_id,
                        Config.ANTI_FLOOD_WARN_MODE
                    ))
                except Exception as e:  # pylint:disable=C0103,W0703
                    no_admin_privilege_message = await borg.send_message(
                        entity=event.chat_id,
                        message="""**Automatic AntiFlooder**
@admin [User](tg://user?id={}) is flooding this chat.

`{}`""".format(event.message.from_id, str(e)),
                        reply_to=event.message.id
                    )
                    await asyncio.sleep(10)
                    await no_admin_privilege_message.edit(
                        "This SPAM is useless dude .So stop SPAMMING ",
                        link_preview=False
                    )
                else:
                    await borg.send_message(
                        entity=event.chat_id,
                        message="""**Automatic AntiFlooder**
[User](tg://user?id={}) has been automatically restricted
because he reached the defined flood limit.""".format(event.message.from_id),
                        reply_to=event.message.id
                    )
                userbot.storage.CHAT_FLOOD[event.chat_id] = (
                    event.message.from_id,
                    0,
                    max_count
                )
            else:
                userbot.storage.CHAT_FLOOD[event.chat_id] = (
                    event.message.from_id,
                    current_count,
                    max_count
                )
        else:
            userbot.storage.CHAT_FLOOD[event.chat_id] = (
                event.message.from_id,
                1,
                max_count
            )


@borg.on(admin_cmd("setflood (.*)"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    # pylint:disable=E0602
    if event.chat_id not in Config.CHATS_TO_MONITOR_FOR_ANTI_FLOOD:
        Config.CHATS_TO_MONITOR_FOR_ANTI_FLOOD.append(event.chat_id)  # pylint:disable=E0602
    input_str = event.pattern_match.group(1)
    try:
        userbot.storage.CHAT_FLOOD[event.chat_id] = (None, 1, int(input_str))
        await event.edit("Antiflood updated to {} in the current chat".format(input_str))
    except Exception as e:  # pylint:disable=C0103,W0703
        await event.edit(str(e))
