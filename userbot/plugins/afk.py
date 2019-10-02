"""AFK Plugin for @UniBorg
Syntax: .afk REASON"""
import asyncio
import datetime
from telethon import events
from telethon.tl import functions, types


borg.storage.USER_AFK = {}  # pylint:disable=E0602
borg.storage.afk_time = None  # pylint:disable=E0602
borg.storage.last_afk_message = {}  # pylint:disable=E0602


@borg.on(events.NewMessage(outgoing=True))  # pylint:disable=E0602
async def set_not_afk(event):
    current_message = event.message.message
    if ".afk" not in current_message and "yes" in borg.storage.USER_AFK:  # pylint:disable=E0602
        try:
            await borg.send_message(  # pylint:disable=E0602
                Config.PRIVATE_GROUP_BOT_API_ID,  # pylint:disable=E0602
                "Set AFK mode to False"
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await borg.send_message(  # pylint:disable=E0602
                event.chat_id,
                "Please set `PRIVATE_GROUP_BOT_API_ID` " + \
                "for the proper functioning of afk functionality " + \
                "in @UniBorg\n\n `{}`".format(str(e)),
                reply_to=event.message.id,
                silent=True
            )
        borg.storage.USER_AFK = {}  # pylint:disable=E0602
        borg.storage.afk_time = None  # pylint:disable=E0602


@borg.on(events.NewMessage(pattern=r"\.afk ?(.*)", outgoing=True))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    reason = event.pattern_match.group(1)
    if not borg.storage.USER_AFK:  # pylint:disable=E0602
        last_seen_status = await borg(  # pylint:disable=E0602
            functions.account.GetPrivacyRequest(
                types.InputPrivacyKeyStatusTimestamp()
            )
        )
        if isinstance(last_seen_status.rules, types.PrivacyValueAllowAll):
            borg.storage.afk_time = datetime.datetime.now()  # pylint:disable=E0602
        borg.storage.USER_AFK.update({"yes": reason})  # pylint:disable=E0602
        if reason:
            await event.edit(f"Set AFK mode to True, and Reason is {reason}")
        else:
            await event.edit(f"Set AFK mode to True")
        await asyncio.sleep(5)
        await event.delete()
        try:
            await borg.send_message(  # pylint:disable=E0602
                Config.PRIVATE_GROUP_BOT_API_ID,  # pylint:disable=E0602
                f"Set AFK mode to True, and Reason is {reason}"
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            logger.warn(str(e))  # pylint:disable=E0602


@borg.on(events.NewMessage(  # pylint:disable=E0602
    incoming=True,
    func=lambda e: bool(e.mentioned or e.is_private)
))
async def on_afk(event):
    if event.fwd_from:
        return
    afk_since = "**a while ago**"
    current_message_text = event.message.message.lower()
    if "afk" in current_message_text:
        # userbot's should not reply to other userbot's
        # https://core.telegram.org/bots/faq#why-doesn-39t-my-bot-see-messages-from-other-bots
        return False
    if borg.storage.USER_AFK and not (await event.get_sender()).bot:  # pylint:disable=E0602
        reason = borg.storage.USER_AFK["yes"]  # pylint:disable=E0602
        if borg.storage.afk_time:  # pylint:disable=E0602
            now = datetime.datetime.now()
            datime_since_afk = now - borg.storage.afk_time  # pylint:disable=E0602
            time = float(datime_since_afk.seconds)
            days = time // (24 * 3600)
            time = time % (24 * 3600)
            hours = time // 3600
            time %= 3600
            minutes = time // 60
            time %= 60
            seconds = time
            if days == 1:
                afk_since = "**Yesterday**"
            elif days > 1:
                if days > 6:
                    date = now + \
                        datetime.timedelta(
                            days=-days, hours=-hours, minutes=-minutes)
                    afk_since = date.strftime("%A, %Y %B %m, %H:%I")
                else:
                    wday = now + datetime.timedelta(days=-days)
                    afk_since = wday.strftime('%A')
            elif hours > 1:
                afk_since = f"`{int(hours)}h{int(minutes)}m` **ago**"
            elif minutes > 0:
                afk_since = f"`{int(minutes)}m{int(seconds)}s` **ago**"
            else:
                afk_since = f"`{int(seconds)}s` **ago**"
        msg = None
        message_to_reply = f"╭━╮╭━╮╱╱╱╱╱╱╭╮\n┃┃╰╯┃┃╱╱╱╱╱╭╯╰╮\n┃╭╮╭╮┣━━┳━━╋╮╭╋━━┳━╮\n┃┃┃┃┃┃╭╮┃━━┫┃┃┃┃━┫╭╯\n┃┃┃┃┃┃╭╮┣━━┃┃╰┫┃━┫┃\n╰╯╰╯╰┻╯╰┻━━╯╰━┻━━┻╯\n╭━━╮\n╰┫┣╯\n╱┃┃╭━━╮\n╱┃┃┃━━┫\n╭┫┣╋━━┃\n╰━━┻━━╯\n╭━━━╮\n┃╭━╮┃\n┃┃╱┃┣╮╭╮╭┳━━┳╮╱╭╮\n┃╰━╯┃╰╯╰╯┃╭╮┃┃╱┃┃\n┃╭━╮┣╮╭╮╭┫╭╮┃╰━╯┃\n╰╯╱╰╯╰╯╰╯╰╯╰┻━╮╭╯\n╱╱╱╱╱╱╱╱╱╱╱╱╭━╯┃\n╱╱╱╱╱╱╱╱╱╱╱╱╰━━╯\n╭━━━╮\n┃╭━━╯\n┃╰━━┳━┳━━┳╮╭╮\n┃╭━━┫╭┫╭╮┃╰╯┃\n┃┃╱╱┃┃┃╰╯┃┃┃┃\n╰╯╱╱╰╯╰━━┻┻┻╯\n╭╮╭━╮╱╱╱╱╱╱╭╮╱╱╱╱╱╱╱╱╱╱╱╭╮\n┃┃┃╭╯╱╱╱╱╱╱┃┃╱╱╱╱╱╱╱╱╱╱╱┃┃\n┃╰╯╯╭━━┳╮╱╭┫╰━┳━━┳━━┳━┳━╯┃\n┃╭╮┃┃┃━┫┃╱┃┃╭╮┃╭╮┃╭╮┃╭┫╭╮┃\n┃┃┃╰┫┃━┫╰━╯┃╰╯┃╰╯┃╭╮┃┃┃╰╯┃\n╰╯╰━┻━━┻━╮╭┻━━┻━━┻╯╰┻╯╰━━╯\n╱╱╱╱╱╱╱╭━╯┃\n╱╱╱╱╱╱╱╰━━╯  \n\n**Last Seen: Only God Knows.** " + \
            f"\n\n__Reason:__ {reason}" \
            if reason \
            else f"Hello! This is an automated message. I am offline currently. Will reply soon. "
        msg = await event.reply(message_to_reply)
        await asyncio.sleep(5)
        if event.chat_id in borg.storage.last_afk_message:  # pylint:disable=E0602
            await borg.storage.last_afk_message[event.chat_id].delete()  # pylint:disable=E0602
        borg.storage.last_afk_message[event.chat_id] = msg  # pylint:disable=E0602
