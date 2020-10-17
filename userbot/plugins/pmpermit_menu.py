"""
Support chatbox for pmpermit.
Used by incoming messages with trigger as /start
Will not work for already approved people.
Credits: written by ༺αиυвιѕ༻ {@A_Dark_Princ3}
"""
import asyncio

from telethon import events, functions

import userbot.plugins.sql_helper.pmpermit_sql as pmpermit_sql

from . import ALIVE_NAME, PM_START

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "cat"
PREV_REPLY_MESSAGE = {}


@bot.on(events.NewMessage(pattern=r"\/start", incoming=True))
async def _(event):
    chat_id = event.from_id
    if not pmpermit_sql.is_approved(chat_id):
        chat = await event.get_chat()
        if chat_id not in PM_START:
            PM_START.append(chat_id)
        if event.fwd_from:
            return
        if not event.is_private:
            return
        PM = (
            "Hello. You are accessing the availabe menu of my master, "
            f"{DEFAULTUSER}.\n"
            "__Let's make this smooth and let me know why you are here.__\n"
            "**Choose one of the following reasons why you are here:**\n\n"
            "`a`. To chat with my master\n"
            "`b`. To spam my master's inbox.\n"
            "`c`. To enquire something\n"
            "`d`. To request something\n"
        )
        ONE = (
            "__Okay. Your request has been registered. Do not spam my master's inbox.You can expect a reply within 24 light years. He is a busy man, unlike you probably.__\n\n"
            "**⚠️ You will be blocked and reported if you spam nibba. ⚠️**\n\n"
            "__Use__ `/start` __to go back to the main menu.__"
        )
        TWO = " `███████▄▄███████████▄  \n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓███░░░░░░░░░░░░█\n██████▀▀▀█░░░░██████▀  \n░░░░░░░░░█░░░░█  \n░░░░░░░░░░█░░░█  \n░░░░░░░░░░░█░░█  \n░░░░░░░░░░░█░░█  \n░░░░░░░░░░░░▀▀ `\n\n**So uncool, this is not your home. Go bother someone else. You have been blocked and reported until further notice.**"
        THREE = "__Okay. My master has not seen your message yet.He usually responds to people,though idk about retarted ones.__\n __He'll respond when he comes back, if he wants to.There's already a lot of pending messages😶__\n **Please do not spam unless you wish to be blocked and reported.**"
        FOUR = "`Okay. please have the basic manners as to not bother my master too much. If he wishes to help you, he will respond to you soon.`\n**Do not ask repeatdly else you will be blocked and reported.**"
        LWARN = "**This is your last warning. DO NOT send another message else you will be blocked and reported. Keep patience. My master will respond you ASAP.**\n__Use__ `/start` __to go back to the main menu.__"
        try:
            async with event.client.conversation(chat) as conv:
                if pmpermit_sql.is_approved(chat_id):
                    return
                await event.client.send_message(chat, PM)
                chat_id = event.from_id
                response = await conv.get_response(chat)
                y = response.text
                if y == "a":
                    if pmpermit_sql.is_approved(chat_id):
                        return
                    await event.client.send_message(chat, ONE)
                    response = await conv.get_response(chat)
                    if not response.text == "/start":
                        if pmpermit_sql.is_approved(chat_id):
                            return
                        await event.client.send_message(chat, LWARN)
                        response = await conv.get_response(chat)
                        if not response.text == "/start":
                            if pmpermit_sql.is_approved(chat_id):
                                return
                            await event.client.send_message(chat, TWO)
                            await asyncio.sleep(3)
                            await event.client(functions.contacts.BlockRequest(chat_id))
                elif y == "b":
                    if pmpermit_sql.is_approved(chat_id):
                        return
                    await event.client.send_message(chat, LWARN)
                    response = await conv.get_response(chat)
                    if not response.text == "/start":
                        if pmpermit_sql.is_approved(chat_id):
                            return
                        await event.client.send_message(chat, TWO)
                        await asyncio.sleep(3)
                        await event.client(functions.contacts.BlockRequest(chat_id))
                elif y == "c":
                    if pmpermit_sql.is_approved(chat_id):
                        return
                    await event.client.send_message(chat, THREE)
                    response = await conv.get_response(chat)
                    if not response.text == "/start":
                        if pmpermit_sql.is_approved(chat_id):
                            return
                        await event.client.send_message(chat, LWARN)
                        response = await conv.get_response(chat)
                        if not response.text == "/start":
                            if pmpermit_sql.is_approved(chat_id):
                                return
                            await event.client.send_message(chat, TWO)
                            await asyncio.sleep(3)
                            await event.client(functions.contacts.BlockRequest(chat_id))
                elif y == "d":
                    if pmpermit_sql.is_approved(chat_id):
                        return
                    await event.client.send_message(chat, FOUR)
                    response = await conv.get_response(chat)
                    if not response.text == "/start":
                        if pmpermit_sql.is_approved(chat_id):
                            return
                        await event.client.send_message(chat, LWARN)
                        response = await conv.get_response(chat)
                        if not response.text == "/start":
                            if pmpermit_sql.is_approved(chat_id):
                                return
                            await event.client.send_message(chat, TWO)
                            await asyncio.sleep(3)
                            await event.client(functions.contacts.BlockRequest(chat_id))
                else:
                    if pmpermit_sql.is_approved(chat_id):
                        return
                    await event.client.send_message(
                        chat,
                        "You have entered an invalid command. Please send `/start` again or do not send another message if you do not wish to be blocked and reported.",
                    )
                    response = await conv.get_response(chat)
                    z = response.text
                    if not z == "/start":
                        if pmpermit_sql.is_approved(chat_id):
                            return
                        await event.client.send_message(chat, LWARN)
                        await conv.get_response(chat)
                        if not response.text == "/start":
                            if pmpermit_sql.is_approved(chat_id):
                                return
                            await event.client.send_message(chat, TWO)
                            await asyncio.sleep(3)
                            await event.client(functions.contacts.BlockRequest(chat_id))
        except:
            pass
