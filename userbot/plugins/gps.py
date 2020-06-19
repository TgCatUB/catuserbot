"""
Syntax : .gps <location name>
help from @sunda005 and @spechide
credits :@mrconfused
don't edit credits
  """

from geopy.geocoders import Nominatim
from userbot.utils import admin_cmd, sudo_cmd
from telethon import events
import asyncio
from telethon.tl import types
from userbot import CMD_HELP 

@borg.on(admin_cmd(pattern="gps ?(.*)"))
async def gps(event):
    if event.fwd_from:
        return
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    input_str = event.pattern_match.group(1)
 
    if not input_str:
        return await event.edit("what should i find give me location.")
    else:
         await event.edit("finding")
         
    geolocator = Nominatim(user_agent="catuserbot")
    geoloc = geolocator.geocode(input_str) 
    if geoloc:
        lon = geoloc.longitude
        lat = geoloc.latitude
        await borg.send_file(event.chat_id, file=types.InputMediaGeoPoint(types.InputGeoPoint(lat, lon)),reply_to=reply_to_id)
        await event.delete()
    else:
        await event.edit("i coudn't fint it")
        
@borg.on(sudo_cmd(pattern="gps ?(.*)", allow_sudo = True))
async def gps(event):
    if event.fwd_from:
        return
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    input_str = event.pattern_match.group(1)
 
    if not input_str:
        return await event.edit("what should i find give me location.")
    else:
         await event.edit("finding")
         
    geolocator = Nominatim(user_agent="catuserbot")
    geoloc = geolocator.geocode(input_str) 
    if geoloc:
        lon = geoloc.longitude
        lat = geoloc.latitude
        await borg.send_file(event.chat_id, file=types.InputMediaGeoPoint(types.InputGeoPoint(lat, lon)),reply_to=reply_to_id)
        await event.delete()
    else:
        await event.edit("i coudn't fint it")      
        
CMD_HELP.update({"gps": "`.gps` <location name> :\
      \nUSAGE: sends you the given location name\
      "
})           
