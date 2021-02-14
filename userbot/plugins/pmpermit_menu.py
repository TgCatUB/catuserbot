"""
Support chatbox for pmpermit.
Used by incoming messages with trigger as /start
Will not work for already approved people.
Credits: written by ༺αиυвιѕ༻ {@A_Dark_Princ3}
"""
import asyncio

from telethon import events, functions

import userbot.plugins.sql_helper.pmpermit_sql as pmpermit_sql

from . import ALIVE_NAME, PM_START, PMMESSAGE_CACHE, set_key

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "cat"
PREV_REPLY_MESSAGE = {}
PM = f"""Hello. You are accessing the availabe menu of my master, {DEFAULTUSER}.
__Let's make this smooth and let me know why you are here.__
**Choose one of the following reasons why you are here:**

`a`. To chat with my master
`b`. To spam my master's inbox.
`c`. To enquire something
`d`. To request something\n"""
ONE = """__Okay. Your request has been registered. Do not spam my master's inbox.You can expect a reply within next few years. He/She is a busy man, unlike you probably.__

**⚠️ You will be blocked and reported if you spam. ⚠️**\n\n"""
TWO = " `███████▄▄███████████▄  \n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓███░░░░░░░░░░░░█\n██████▀▀▀█░░░░██████▀  \n░░░░░░░░░█░░░░█  \n░░░░░░░░░░█░░░█  \n░░░░░░░░░░░█░░█  \n░░░░░░░░░░░█░░█  \n░░░░░░░░░░░░▀▀ `\n\n**So uncool, this is not your home. Go bother someone else. You have been blocked and reported until further notice.**"
THREE = "__Okay. My master has not seen your message yet.He/She usually responds to people,though idk about retarted ones.__\n __He'll respond when he/she comes back, if he/she wants to.There's already a lot of pending messages😶__\n **Please do not spam unless you wish to be blocked and reported.**"
FOUR = "`Okay. please have the basic manners as to not bother my master too much. If he/she wishes to help you, he/she will respond to you soon.`\n**Do not ask repeatdly else you will be blocked and reported.**"
LWARN = "**This is your last warning. DO NOT send another message else you will be blocked and reported. Keep patience. My master will respond you ASAP.**\n"


@bot.on(events.NewMessage(pattern=r"\/start", incoming=True))
async def _(event):
    if event.fwd_from:
        return
    chat_id = event.sender_id
    if not pmpermit_sql.is_approved(chat_id):
        chat = await event.get_chat()
        if chat_id not in PM_START:
            PM_START.append(chat_id)
        if not event.is_private:
            return
        set_key(PMMESSAGE_CACHE, event.chat_id, event.id)
        try:
            async with event.client.conversation(chat) as conv:
                if pmpermit_sql.is_approved(chat_id):
                    return
                test1 = await event.client.send_message(chat, PM)
                set_key(PMMESSAGE_CACHE, event.chat_id, test1.id)
                chat_id = event.sender_id
                response = await conv.get_response(chat)
                y = response.text
                if y == "a" or "A":
                    if pmpermit_sql.is_approved(chat_id):
                        return
                    set_key(PMMESSAGE_CACHE, event.chat_id, response.id)
                    test2 = await event.client.send_message(chat, ONE)
                    set_key(PMMESSAGE_CACHE, event.chat_id, test2.id)
                    response = await conv.get_response(chat)
                    if response.text != "/start":
                        if pmpermit_sql.is_approved(chat_id):
                            return
                        set_key(PMMESSAGE_CACHE, event.chat_id, response.id)
                        test3 = await event.client.send_message(chat, LWARN)
                        set_key(PMMESSAGE_CACHE, event.chat_id, test3.id)
                        response = await conv.get_response(chat)
                        if response.text != "/start":
                            if pmpermit_sql.is_approved(chat_id):
                                return
                            set_key(PMMESSAGE_CACHE, event.chat_id, response.id)
                            test4 = await event.client.send_message(chat, TWO)
                            set_key(PMMESSAGE_CACHE, event.chat_id, test4.id)
                            await asyncio.sleep(3)
                            await event.client(functions.contacts.BlockRequest(chat_id))
                elif y == "b" or "B":
                    if pmpermit_sql.is_approved(chat_id):
                        return
                    set_key(PMMESSAGE_CACHE, event.chat_id, response.id)
                    test5 = await event.client.send_message(chat, LWARN)
                    set_key(PMMESSAGE_CACHE, event.chat_id, test5.id)
                    response = await conv.get_response(chat)
                    if response.text != "/start":
                        if pmpermit_sql.is_approved(chat_id):
                            return
                        set_key(PMMESSAGE_CACHE, event.chat_id, response.id)
                        test6 = await event.client.send_message(chat, TWO)
                        set_key(PMMESSAGE_CACHE, event.chat_id, test6.id)
                        await asyncio.sleep(3)
                        await event.client(functions.contacts.BlockRequest(chat_id))
                elif y == "c" or "C":
                    if pmpermit_sql.is_approved(chat_id):
                        return
                    set_key(PMMESSAGE_CACHE, event.chat_id, response.id)
                    test7 = await event.client.send_message(chat, THREE)
                    set_key(PMMESSAGE_CACHE, event.chat_id, test7.id)
                    response = await conv.get_response(chat)
                    if response.text != "/start":
                        if pmpermit_sql.is_approved(chat_id):
                            return
                        set_key(PMMESSAGE_CACHE, event.chat_id, response.id)
                        test8 = await event.client.send_message(chat, LWARN)
                        set_key(PMMESSAGE_CACHE, event.chat_id, test8.id)
                        response = await conv.get_response(chat)
                        if response.text != "/start":
                            if pmpermit_sql.is_approved(chat_id):
                                return
                            set_key(PMMESSAGE_CACHE, event.chat_id, response.id)
                            test9 = await event.client.send_message(chat, TWO)
                            set_key(PMMESSAGE_CACHE, event.chat_id, test9.id)
                            await asyncio.sleep(3)
                            await event.client(functions.contacts.BlockRequest(chat_id))
                elif y == "d" or "D":
                    if pmpermit_sql.is_approved(chat_id):
                        return
                    set_key(PMMESSAGE_CACHE, event.chat_id, response.id)
                    test10 = await event.client.send_message(chat, FOUR)
                    set_key(PMMESSAGE_CACHE, event.chat_id, test10.id)
                    response = await conv.get_response(chat)
                    if response.text != "/start":
                        if pmpermit_sql.is_approved(chat_id):
                            return
                        set_key(PMMESSAGE_CACHE, event.chat_id, response.id)
                        test11 = await event.client.send_message(chat, LWARN)
                        set_key(PMMESSAGE_CACHE, event.chat_id, test11.id)
                        response = await conv.get_response(chat)
                        if response.text != "/start":
                            if pmpermit_sql.is_approved(chat_id):
                                return
                            set_key(PMMESSAGE_CACHE, event.chat_id, response.id)
                            await event.client.send_message(chat, TWO)
                            await asyncio.sleep(3)
                            await event.client(functions.contacts.BlockRequest(chat_id))
                else:
                    if pmpermit_sql.is_approved(chat_id):
                        return
                    test12 = await event.client.send_message(
                        chat,
                        "You have entered an invalid command. Please send `/start` again or do not send another message if you do not wish to be blocked and reported.",
                    )
                    set_key(PMMESSAGE_CACHE, event.chat_id, test12.id)
                    response = await conv.get_response(chat)
                    z = response.text
                    if z != "/start":
                        if pmpermit_sql.is_approved(chat_id):
                            return
                        set_key(PMMESSAGE_CACHE, event.chat_id, response.id)
                        test13 = await event.client.send_message(chat, LWARN)
                        set_key(PMMESSAGE_CACHE, event.chat_id, test13.id)
                        response = await conv.get_response(chat)
                        if response.text != "/start":
                            if pmpermit_sql.is_approved(chat_id):
                                return
                            set_key(PMMESSAGE_CACHE, event.chat_id, response.id)
                            test14 = await event.client.send_message(chat, TWO)
                            set_key(PMMESSAGE_CACHE, event.chat_id, test14.id)
                            await asyncio.sleep(3)
                            await event.client(functions.contacts.BlockRequest(chat_id))
        except Exception as e:
            LOGS.info(str(e))
