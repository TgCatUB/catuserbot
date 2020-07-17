""" Spotify / Deezer downloader plugin by @anubisxx | Syntax: .dzd link"""
import asyncio
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError, UserAlreadyParticipantError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from userbot.utils import admin_cmd

@borg.on(admin_cmd(outgoing=True, pattern="dzd(?: |$)(.*)"))
async def DeezLoader(Deezlod):
    if Deezlod.fwd_from:
        return
    d_link = Deezlod.pattern_match.group(1)
    if ".com" not in d_link:
        await Deezlod.edit("` I need a link to download something pro.`**(._.)**")
    else:
        await Deezlod.edit("🎶**Initiating Download!**🎶")
    chat = "@DeezLoadBot"
    async with bot.conversation(chat) as conv:
          try:
              msg_start = await conv.send_message("/start")
              response = await conv.get_response()
              r = await conv.get_response()
              msg = await conv.send_message(d_link)
              details = await conv.get_response()
              song = await conv.get_response()
              """ - don't spam notif - """
              await bot.send_read_acknowledge(conv.chat_id)
          except YouBlockedUserError:
              await Deezlod.edit("**Error:** `Unblock` @DeezLoadBot `and retry!`")
              return
          await bot.send_file(Deezlod.chat_id, song, caption=details.text)
          await Deezlod.client.delete_messages(conv.chat_id,
                                             [msg_start.id, response.id, r.id, msg.id, details.id, song.id])
          await Deezlod.delete()
