"""Syntax : .gps <location name>
  help from @sunda005 and @SpEcHIDe
  credits :@mrconfused
  don't edit credits"""

from geopy.geocoders import Nominatim
from userbot.utils import admin_cmd, sudo_cmd
from telethon.tl import types
from userbot import CMD_HELP 


@borg.on(admin_cmd(pattern="gps ?(.*)"))
async def gps(event):
    if event.fwd_from:
        return
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    input_str = event.pattern_match.group(1)

    if not input_str:
        return await event.edit("what should i find give me location.")

    await event.edit("finding")

    geolocator = Nominatim(user_agent="catuserbot")
    geoloc = geolocator.geocode(input_str)

    if geoloc:
        lon = geoloc.longitude
        lat = geoloc.latitude
        await reply_to_id.reply(
            input_str,
            file=types.InputMediaGeoPoint(
                types.InputGeoPoint(
                    lat, lon
                )
            )
        )
        await event.delete()
    else:
        await event.edit("i coudn't find it")
        
        
@borg.on(sudo_cmd(pattern="gps ?(.*)", allow_sudo = True))
async def gps(event):
    if event.fwd_from:
        return
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    input_str = event.pattern_match.group(1)

    if not input_str:
        return await event.reply("what should i find give me location.")

    cat = await event.reply("finding")

    geolocator = Nominatim(user_agent="catuserbot")
    geoloc = geolocator.geocode(input_str)

    if geoloc:
        lon = geoloc.longitude
        lat = geoloc.latitude
        await reply_to_id.reply(
            input_str,
            file=types.InputMediaGeoPoint(
                types.InputGeoPoint(
                    lat, lon
                )
            )
        )
        await cat.delete()
    else:
        await cat.edit("i coudn't find it")

        
CMD_HELP.update({"gps": "`.gps` <location name> :\
      \nUSAGE: sends you the given location name\
      "
})           
