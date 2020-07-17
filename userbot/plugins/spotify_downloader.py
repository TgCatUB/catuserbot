""" Spotify downloader plugin by @Sur_vivor | Syntax: .spd <name>"""
import asyncio
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError, UserAlreadyParticipantError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from userbot.utils import admin_cmd

@borg.on(admin_cmd(outgoing=True, pattern="spd(?: |$)(.*)"))
async def _(event):
    if event.fwd_from:
        return
    link = event.pattern_match.group(1)
    chat = "@SpotifyMusicDownloaderBot"
    await event.edit("```Getting Your Music```")
    async with bot.conversation(chat) as conv:
          await asyncio.sleep(2)
          await event.edit("`Downloading music taking some times,  Stay Tuned.....`")
          try:
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=752979930))
              msg = await bot.send_message(chat, link)
              respond = await response
              res = conv.wait_event(events.NewMessage(incoming=True,from_users=752979930))
              r = await res
              """ - don't spam notif - """
              await bot.send_read_acknowledge(conv.chat_id)
          except YouBlockedUserError:
              await event.reply("```Please unblock @SpotifyMusicDownloaderBot and try again```")
              return
          await bot.forward_messages(event.chat_id, respond.message)
    await event.client.delete_messages(conv.chat_id,
                                       [msg.id, r.id, respond.id])
    await event.delete()
