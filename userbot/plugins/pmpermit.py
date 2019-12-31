import asyncio
import io 
import userbot.plugins.sql_helper.pmpermit_sql as pmpermit_sql
import telethon.sync
from telethon.tl.functions.users import GetFullUserRequest
from telethon import events, errors, functions, types 


PM_WARNS = {}
PREV_REPLY_MESSAGE = {}


USER_BOT_WARN_ZERO = "I am currently offline. Please do not SPAM me.Else gaand mara dunga bsdk "
USER_BOT_NO_WARN = "`[──▄█▀█▄─────────██ \n▄████████▄───▄▀█▄▄▄▄ \n██▀▼▼▼▼▼─▄▀──█▄▄ \n█████▄▲▲▲─▄▄▄▀───▀▄ \n██████▀▀▀▀─▀────────▀▀]\n\nHello, this is X-tra-Telegram Security Service. If you spam you will be reported and blocked, so make sure you **DON'T SPAM**.\n\nYour companionship is always an opportunity But Sed This line is not for you.`"


if Var.PRIVATE_GROUP_ID is not None:
    @command(pattern="^.approve ?(.*)")
    async def approve_p_m(event):
        if event.fwd_from:
           return
        replied_user = await event.client(GetFullUserRequest(event.chat_id))
        firstname = replied_user.user.first_name
        reason = event.pattern_match.group(1)
        chat = await event.get_chat()
        if event.is_private:
            if not pmpermit_sql.is_approved(chat.id):
                if chat.id in PM_WARNS:
                    del PM_WARNS[chat.id]
                if chat.id in PREV_REPLY_MESSAGE:
                    await PREV_REPLY_MESSAGE[chat.id].delete()
                    del PREV_REPLY_MESSAGE[chat.id]
                pmpermit_sql.approve(chat.id, reason)
                await event.edit("Approved User [{}](tg://user?id={})".format(firstname, chat.id))
                await asyncio.sleep(3)
                await event.delete()


    @command(pattern="^.block ?(.*)")
    async def approve_p_m(event):
        if event.fwd_from:
            return
        replied_user = await event.client(GetFullUserRequest(event.chat_id))
        firstname = replied_user.user.first_name
        reason = event.pattern_match.group(1)
        chat = await event.get_chat()
        if event.is_private:
            if pmpermit_sql.is_approved(chat.id):
                pmpermit_sql.disapprove(chat.id)
                await event.edit(" ███████▄▄███████████▄  \n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓███░░░░░░░░░░░░█\n██████▀▀▀█░░░░██████▀  \n░░░░░░░░░█░░░░█  \n░░░░░░░░░░█░░░█  \n░░░░░░░░░░░█░░█  \n░░░░░░░░░░░█░░█  \n░░░░░░░░░░░░▀▀ \n\nFuck Off Bitch, Now You Can't Message Me..[{}](tg://user?id={})".format(firstname, chat.id))
                await asyncio.sleep(3)
                await event.client(functions.contacts.BlockRequest(chat.id))


    @bot.on(events.NewMessage(incoming=True))
    async def on_new_private_message(event):
        if event.from_id == bot.uid:
            return

        if Var.PRIVATE_GROUP_ID is None:
            return

        if not event.is_private:
            return

        message_text = event.message.message
        chat_id = event.from_id

        current_message_text = message_text.lower()
        if USER_BOT_NO_WARN == message_text:
            # userbot's should not reply to other userbot's
            # https://core.telegram.org/bots/faq#why-doesn-39t-my-bot-see-messages-from-other-bots
            return

        sender = await bot.get_entity(chat_id)
        if chat_id == bot.uid:
            # don't log Saved Messages
            return
        if sender.bot:
            # don't log bots
            return
        if sender.verified:
            # don't log verified accounts
            return

        if not pmpermit_sql.is_approved(chat_id):
            # pm permit
            await do_pm_permit_action(chat_id, event)


    async def do_pm_permit_action(chat_id, event):
        chat = await event.get_chat()
        if event.is_private:
         Nudas = ("__Please state your gender.__\n"
                  "`1`. Female Homo-Sapien\n"
                  "`2`. Male Homo-Sapien\n"
                  "`3`. Other\n")
         PM = ("`Hello. You are accessing the availabe menu of my peru master, DEFAULTUSER.`\n"
               "__Let's make this smooth and let me know why you are here.__\n"
               "**Choose one of the following reasons why you are here:**\n\n"
               "`1`. To chat with my master\n"
               "`2`. To spam my master's inbox.\n"
               "`3`. To send nudes.\n"
               "`4`. To enquire something\n"
               "`5`. To request something\n")
         ONE = ("__Okay. Your request has been registered. Do not spam my master's inbox.You can expect a reply within 24 light years. He is a busy man, unlike you probably.__\n\n"
                "**⚠️ You will be blocked and reported if you spam nibba. ⚠️**\n"
                "__Use__ `/start` __to go back to the main menu.__")
         TWO = (" `███████▄▄███████████▄  \n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓███░░░░░░░░░░░░█\n██████▀▀▀█░░░░██████▀  \n░░░░░░░░░█░░░░█  \n░░░░░░░░░░█░░░█  \n░░░░░░░░░░░█░░█  \n░░░░░░░░░░░█░░█  \n░░░░░░░░░░░░▀▀ `\n\n**So uncool, this is not your home. Go bother someone else. You have been blocked and reported until further notice.**")
         FOUR = ("__Okay. My master has not seen your message yet.He usually responds to people,though idk about retarted ones.__\n __He'll respond when he comes back, if he wants to.There's already a lot of pending messages😶__\n **Please do not spam unless you wish to be blocked and reported.**")
         FIVE = ("`Okay. please have the basic manners as to not bother my master too much. If he wishes to help you, he will respond to you soon.`\n**Do not ask repeatdly else you will be blocked and reported.**")
         LWARN = ("**This is your last warning. DO NOT send another message else you will be blocked and reported. Keep patience. My master will respond you ASAP.**\n__Use__ `/start` __to go back to the main menu.__")
         
        async with borg.conversation(chat) as conv:
         chat_id = event.from_id
         response = await conv.get_response(chat)
         if response.text == "/start":
             await borg.send_message(chat, PM)
             await borg.send_message(chat, PM)
             chat_id = event.from_id
             response = await conv.get_response(chat)
             y = response.text
             if y == "1":
                 await borg.send_message(chat, ONE)
                 response = await conv.get_response(chat)
                 if not reponse.text == "/start":
                     await borg.send_messgae(chat, LWARN)
                     response = await conv.get_response(chat)
                     if not reponse.text == "/start":
                         await borg.send_message(chat, TWO)
                         await asyncio.sleep(3)
                         await event.client(functions.contacts.BlockRequest(chat_id))
             elif y == "2":
                 await borg.send_message(chat, LWARN)
                 response = await conv.get_response(chat)
                 if not reponse.text == "/start":
                     await borg.send_messgae(chat, TWO)
                     await asyncio.sleep(3)
                     await event.client(functions.contacts.BlockRequest(chat_id))
             elif y == "3":
                 await borg.send_message(chat, Nudas)
                 response = await conv.get_response(chat)
                 x = response.text
                 if x == "1":
                     await borg.send_message(chat, "__Oh my, you're very much welcome here ;). Please drop your offerings and let my master judge if you have good heart <3.\n Please don't flood my inbox, we'll have a nice convo once i come back ;D__")
                 elif x == "2":
                     await borg.send_message(chat, "**You nigga gay af to send a guy like my your male nudes. Leave immediately else you become the ultimate gayest gay the gay world has ever seen.**")
                 elif x == "3":
                     await borg.send_message(chat, "`Please decide a gender for yourself before coming here, not that i'm judging if you're a helicopter or a banana but yeah. If you are anything else than the first option, Do not send more messages and let my master see for himself if he wants to talk with you.`")
                 else:
                     await borg.send_message(chat, "__You have entered an invalid command. Please send__ `/start` __again or do not send another message if you do not wish to be blocked and reported.__")
                     response = await conv.get_response(chat)
                     if not response.text.startswith("/start"):
                         await borg.send_message(chat, TWO)
                         await asyncio.sleep(3)
                         await event.client(functions.contacts.BlockRequest(chat_id))
             elif y == "4":
                 await borg.send_message(chat, FOUR)
                 if not reponse.text == "/start":
                     await borg.send_messgae(chat, LWARN)
                     response = await conv.get_response(chat)
                     if not reponse.text == "/start":
                         await borg.send_message(chat, TWO)
                         await asyncio.sleep(3)
                         await event.client(functions.contacts.BlockRequest(chat_id))
             elif y == "5":
                 await borg.send_message(chat,FIVE)
                 if not reponse.text == "/start":
                     await borg.send_messgae(chat, LWARN)
                     response = await conv.get_response(chat)
                     if not reponse.text == "/start":
                         await borg.send_message(chat, TWO)
                         await asyncio.sleep(3)
                         await event.client(functions.contacts.BlockRequest(chat_id))
             else:
                 await borg.send_message(chat, "You have entered an invalid command. Please send /start again or do not send another message if you do not wish to be blocked and reported.")
                 response = await conv.get_response(chat)
                 z = response.text
                 if not z == "/start":
                     await borg.send_message(chat, LWARN)
                     await conv.get_response(chat)
                     if not response.text == "/start":
                         await borg.send_message(chat, TWO)
                         await asyncio.sleep(3)
                         await event.client(functions.contacts.BlockRequest(chat_id))
         else:
            r = await event.reply(USER_BOT_NO_WARN)
            if chat_id in PREV_REPLY_MESSAGE:
                await PREV_REPLY_MESSAGE[chat_id].delete()
            PREV_REPLY_MESSAGE[chat_id] = r
            chat = await event.get_chat()
    
