'''@PhycoNinja13b'''
"""Commands:
.warn0
.warn1
.warn2
.warn3
.gbun
.fw
.ocb
.warng1
.warng2
.warng3
.bad1
.ban2
.bad3
.gbad"""
import asyncio
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from uniborg.util import admin_cmd


@borg.on(admin_cmd(pattern="warn1"))
async def _(event):
    if event.fwd_from:
        return
    mentions = "__You Have__  **1/3**  __warnings...__\n**Watch out!....**\n**Reason for warn:** __Halkat hai Sala__"
    chat = await event.get_input_chat()
    async for x in borg.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f""
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()

""".admin Plugin for @UniBorg"""
import asyncio
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from uniborg.util import admin_cmd


@borg.on(admin_cmd(pattern="warn2"))
async def _(event):
    if event.fwd_from:
        return
    mentions = "__You Have__  **2/3**  __warnings...__\n**Watch out!....**\n**Reason for warn:** __Chal Be Muthal__"
    chat = await event.get_input_chat()
    async for x in borg.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f""
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()

""".admin Plugin for @UniBorg"""
import asyncio
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from uniborg.util import admin_cmd


@borg.on(admin_cmd(pattern="warn3"))
async def _(event):
    if event.fwd_from:
        return
    mentions = "__You Have__  **3/3**  __warnings...__\n**Watch out!....**\n**Reason for warn:** __Badtamezz Juban Ladata Hai__"
    chat = await event.get_input_chat()
    async for x in borg.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f""
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()

""".admin Plugin for @UniBorg"""
import asyncio
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from uniborg.util import admin_cmd


@borg.on(admin_cmd(pattern="warn0"))
async def _(event):
    if event.fwd_from:
        return
    mentions = "**Warning Resetted By Nagato...**\n__You Have__  **0/3**  __warnings__\n**Chal Maaf Kia Bhai hai tu mera ;)"
    chat = await event.get_input_chat()
    async for x in borg.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f""
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()

""".admin Plugin for @UniBorg"""
import asyncio
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from uniborg.util import admin_cmd


@borg.on(admin_cmd(pattern="gbun"))
async def _(event):
    if event.fwd_from:
        return
    mentions = "__Warning!! User__ 𝙂𝘽𝘼𝙉𝙉𝙀𝘿 __By Nagato...__\n**Reason:** __Nikal Pehli Fursat Me Gendu__**"
    chat = await event.get_input_chat()
    async for x in borg.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f""
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()


@borg.on(admin_cmd(pattern="ocb"))
async def _(event):
    if event.fwd_from:
        return
    mentions = "**Warning..\n\nBattery Below 10%, Please Charge Your Phone**"
    chat = await event.get_input_chat()
    async for x in borg.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f""
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()

@borg.on(admin_cmd(pattern="fw"))
async def _(event):
    if event.fwd_from:
        return
    mentions = "`U Got A FloodWait:\nReason:telethon.errors.rpcerrorlist.FloodWaitError: A wait of 546578265716823 seconds is required (caused by EditMessageRequest)`"
    chat = await event.get_input_chat()
    async for x in borg.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f""
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()
    
""".admin Plugin for @UniBorg"""
import asyncio
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from uniborg.util import admin_cmd


@borg.on(admin_cmd(pattern="warng1"))
async def _(event):
    if event.fwd_from:
        return
    mentions = "__You Have__  **1/3**  __warnings...__\n**Watch out!....**\n**Reason for warn:** __Stop it Gey__"
    chat = await event.get_input_chat()
    async for x in borg.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f""
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()
    
""".admin Plugin for @UniBorg"""
import asyncio
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from uniborg.util import admin_cmd


@borg.on(admin_cmd(pattern="warng2"))
async def _(event):
    if event.fwd_from:
        return
    mentions = "__You Have__  **2/3**  __warnings...__\n**Watch out!....**\n**Reason for warn:** __Why so Gey?__"
    chat = await event.get_input_chat()
    async for x in borg.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f""
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()
    
""".admin Plugin for @UniBorg"""
import asyncio
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from uniborg.util import admin_cmd


@borg.on(admin_cmd(pattern="warng3"))
async def _(event):
    if event.fwd_from:
        return
    mentions = "__You Have__  **3/3**  __warnings...__\n**Watch out!....**\n**Reason for warn:** __No Gey Talks Here!!__"
    chat = await event.get_input_chat()
    async for x in borg.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f""
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()
    
""".admin Plugin for @UniBorg"""
import asyncio
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from uniborg.util import admin_cmd


@borg.on(admin_cmd(pattern="bad1"))
async def _(event):
    if event.fwd_from:
        return
    mentions = "__You Have__  **1/3**  __warnings...__\n**Watch out!....**\n**Reason for warn:** __Bad Admin__"
    chat = await event.get_input_chat()
    async for x in borg.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f""
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()
    
""".admin Plugin for @UniBorg"""
import asyncio
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from uniborg.util import admin_cmd


@borg.on(admin_cmd(pattern="bad2"))
async def _(event):
    if event.fwd_from:
        return
    mentions = "__You Have__  **2/3**  __warnings...__\n**Watch out!....**\n**Reason for warn:** __Who gave you Admin?__"
    chat = await event.get_input_chat()
    async for x in borg.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f""
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()
    
""".admin Plugin for @UniBorg"""
import asyncio
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from uniborg.util import admin_cmd


@borg.on(admin_cmd(pattern="bad3"))
async def _(event):
    if event.fwd_from:
        return
    mentions = "__You Have__  **3/3**  __warnings...__\n**Watch out!....**\n**Reason for warn:** __Don't mess with legend you Admin__"
    chat = await event.get_input_chat()
    async for x in borg.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f""
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()
    
""".admin Plugin for @UniBorg"""
import asyncio
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from uniborg.util import admin_cmd


@borg.on(admin_cmd(pattern="gbad"))
async def _(event):
    if event.fwd_from:
        return
    mentions = "__Warning!! Admin__ 𝙂𝘽𝘼𝙉𝙉𝙀𝘿 __By Nagato...__\n**Reason:** __Halkat hai yeh Admin xD__**"
    chat = await event.get_input_chat()
    async for x in borg.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f""
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()
