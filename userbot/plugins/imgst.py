import datetime
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from userbot.utils import admin_cmd
from userbot import bot 

@borg.on(admin_cmd(pattern="itos ?(.*)"))
async def _(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit("Sir this is not a image message reply to image message")
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.media:
       await event.edit("Sir, This is not a image ")
       return
    chat = "@buildstickerbot"
    await event.edit("Making a sticker")
    async with event.client.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=164977173))
              await event.client.forward_messages(chat, reply_message)
              response = await response 
          except YouBlockedUserError: 
              await event.reply("Unblock me (@buildstickerbot) and try again")
              return
          if response.text.startswith("Hi!"):
             await event.edit("Can you kindly disable your forward privacy settings for good?")
          else: 
             await event.delete()
             await event.client.send_message(event.chat_id, response.message)
          await bot.send_read_acknowledge(conv.chat_id)
            
@borg.on(admin_cmd(pattern="stoi ?(.*)"))
async def _(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit("Sir reply to sticker message")
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.media:
       await event.edit("Sir Reply to sticker message")
       return
    chat = "@stickers_to_image_bot"
    await event.edit("Making a image")
    async with event.client.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=611085086))
              await event.client.forward_messages(chat, reply_message)
              response = await response 
          except YouBlockedUserError: 
              await event.reply("Unblock me (@stickers_to_image_bot) to work")
              return
          if response.text.startswith("I understand only stickers"):
              await event.edit("Sorry i cant't convert it check wheter is non animated sticker or not")
          else:
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=611085086))
              response = await response
              if response.text.startswith("..."):
                  response = conv.wait_event(events.NewMessage(incoming=True,from_users=611085086))
                  response = await response
                  await event.delete()
                  await event.client.send_message(event.chat_id, response.message , reply_to = reply_message.id)
              else:
                  await event.edit("try again")
          await bot.send_read_acknowledge(conv.chat_id)
