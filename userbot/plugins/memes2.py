#Added by @Sur_vivor
import asyncio
import random
import re
import time
from random import choice, randint
from collections import deque
from telethon import events
import requests
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from userbot.utils import admin_cmd


# ================= CONSTANT =================


GAMBAR_TITIT = """
🍆🍆
🍆🍆🍆
  🍆🍆🍆
    🍆🍆🍆
     🍆🍆🍆
       🍆🍆🍆
        🍆🍆🍆
         🍆🍆🍆
          🍆🍆🍆
          🍆🍆🍆
      🍆🍆🍆🍆
 🍆🍆🍆🍆🍆🍆
 🍆🍆🍆  🍆🍆🍆
    🍆🍆       🍆🍆
"""

# ===========================================

@borg.on(admin_cmd(pattern=r"hf$"))
async def facepalm(e):
    """ Facepalm  🤦‍♂ """
    await e.edit("🤦‍♂")

@borg.on(admin_cmd(pattern=r"corona$"))
async def iqless(e):
    await e.edit("Antivirus scan was completed \n⚠️ Warning! This  donkey has Corona Virus")


@borg.on(admin_cmd(pattern=r"ggl (.*)"))
async def let_me_google_that_for_you(lmgtfy_q):
    textx = await lmgtfy_q.get_reply_message()
    qry = lmgtfy_q.pattern_match.group(1)
    if qry:
        query = str(qry)
    elif textx:
        query = textx
        query = query.message
    query_encoded = query.replace(" ", "+")
    lfy_url = f"http://lmgtfy.com/?s=g&iie=1&q={query_encoded}"
    payload = {'format': 'json', 'url': lfy_url}
    r = requests.get('http://is.gd/create.php', params=payload)
    await lmgtfy_q.edit(f"Tap this blue, help yourself.\
    \n[{query}]({r.json()['shorturl']})")


@borg.on(admin_cmd(outgoing=True, pattern="fail$"))
async def fail(e):
        await e.edit("`\n▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄ `" 
                     "`\n████▌▄▌▄▐▐▌█████ `"    
                     "`\n████▌▄▌▄▐▐▌▀████ `"       
                     "`\n▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀ `")    


@borg.on(admin_cmd(outgoing=True, pattern="lol$"))
async def lol(e):
        await e.edit("`\n╱┏┓╱╱╱╭━━━╮┏┓╱╱╱╱ `" 
                     "`\n╱┃┃╱╱╱┃╭━╮┃┃┃╱╱╱╱ `"       
                     "`\n╱┃┗━━┓┃╰━╯┃┃┗━━┓╱ `" 
                     "`\n╱┗━━━┛╰━━━╯┗━━━┛╱ `")
    
@borg.on(admin_cmd(outgoing=True, pattern="rock$"))
async def lol(e):
        await e.edit("`\n┈╭╮┈┈┈┈┈┈┈┈┈┈┈┈ `"
                     "`\n┈┃┃┈╭╮┈┏╮╭╮╭╮┃╭ `"
                     "`\n┈┃┃┈┃┃┈┣┫┃┃┃┈┣┫ `"
                     "`\n┈┃┣┳┫┃┈┃╰╰╯╰╯┃╰ `"
                     "`\n╭┻┻┻┫┃┈┈╭╮┃┃━┳━ `"
                     "`\n┃╱╭━╯┃┈┈┃┃┃┃┈┃┈ `"
                     "`\n╰╮╱╱╱┃┈┈╰╯╰╯┈┃┈ `")

    
@borg.on(admin_cmd(outgoing=True, pattern="lool$"))
async def lool(e):
        await e.edit("`\n╭╭━━━╮╮┈┈┈┈┈┈┈┈┈┈\n┈┃╭━━╯┈┈┈┈▕╲▂▂╱▏┈\n┈┃┃╱▔▔▔▔▔▔▔▏╱▋▋╮┈`"
                     "`\n┈┃╰▏┃╱╭╮┃╱╱▏╱╱▆┃┈\n┈╰━▏┗━╰╯┗━╱╱╱╰┻┫┈\n┈┈┈▏┏┳━━━━▏┏┳━━╯┈`"
                     "`\n┈┈┈▏┃┃┈┈┈┈▏┃┃┈┈┈┈ `")
                     


@borg.on(admin_cmd(outgoing=True, pattern="nih$"))
async def nih(e):
        await e.edit("`\n(\_/)`"
                     "`\n(•_•)`"
                     "`\n >🌹 *`"
                     "`\n                    `"
                     "`\n(\_/)`"
                     "`\n(•_•)`"
                     "`\n🌹<\ *`")


@borg.on(admin_cmd(outgoing=True, pattern="hoi$"))  
async def gtfo(e):
        await e.edit("`\n█████████`" 
                     "`\n█▄█████▄█`"    
                     "`\n█▼▼▼▼▼`"       
                     "`\n█  Hello Man`"
                     "`\n█▲▲▲▲▲`"
                     "`\n█████████`"
                    "`\n ██   ██`")               


@borg.on(admin_cmd(outgoing=True, pattern="ml(?: |$)(.*)"))
async def gtfo(e):
        message = e.pattern_match.group(1)
        await e.edit("`\n█████████`" 
                     "`\n█▄█████▄█`"    
                     "`\n█▼▼▼▼▼`"       
                     f"`\n█  {message}`"
                     "`\n█▲▲▲▲▲`"
                     "`\n█████████`"
                    "`\n ██   ██`")               


@borg.on(admin_cmd(outgoing=True, pattern="taco$")) 
async def taco(e):
        await e.edit("\n{\__/}"
                     "\n(●_●)"
                     "\n( >🌮 Want a taco?")


@borg.on(admin_cmd(outgoing=True, pattern="paw$"))  
async def paw(e):
        await e.edit("`(=ↀωↀ=)")


@borg.on(admin_cmd(outgoing=True, pattern="tf$")) 
async def tf(e):
        await e.edit("(̿▀̿ ̿Ĺ̯̿̿▀̿ ̿)̄  ")  
      

@borg.on(admin_cmd(outgoing=True, pattern="gay$"))           
async def gey(e):
        await e.edit("`\n┈┈┈╭━━━━━╮┈┈┈┈┈\n┈┈┈┃┊┊┊┊┊┃┈┈┈┈┈`"
                     "`\n┈┈┈┃┊┊╭━╮┻╮┈┈┈┈\n┈┈┈╱╲┊┃▋┃▋┃┈┈┈┈\n┈┈╭┻┊┊╰━┻━╮┈┈┈┈`"
                     "`\n┈┈╰┳┊╭━━━┳╯┈┈┈┈\n┈┈┈┃┊┃╰━━┫┈U GAY`"
                    "\n┈┈┈┈┈┈┏━┓┈┈┈┈┈┈")    


@borg.on(admin_cmd(outgoing=True, pattern="bot$"))
async def bot(e):
        await e.edit("` \n   ╲╲╭━━━━╮ \n╭╮┃▆┈┈▆┃╭╮ \n┃╰┫▽▽▽┣╯┃ \n╰━┫△△△┣━╯`"
                     "`\n╲╲┃┈┈┈┈┃  \n╲╲┃┈┏┓┈┃ `")


@borg.on(admin_cmd(outgoing=True, pattern="hai$"))
async def hey(e):
        await e.edit("\n┈┈┈╱▔▔▔▔╲┈╭━━━━━\n┈┈▕▂▂▂▂▂▂▏┃HELLO!┊😀`"
                     "`\n┈┈▕▔▇▔▔┳▔▏╰┳╮HELLO!┊\n┈┈▕╭━╰╯━╮▏━╯╰━━━\n╱▔▔▏▅▅▅▅▕▔▔╲┈┈┈┈`"
                     "`\n▏┈┈╲▂▂▂▂╱┈┈┈▏┈┈┈`")


@borg.on(admin_cmd(outgoing=True, pattern="nou$"))
async def nou(e):
        await e.edit("`\n┈╭╮╭╮\n┈┃┃┃┃\n╭┻┗┻┗╮`"
                     "`\n┃┈▋┈▋┃\n┃┈╭▋━╮━╮\n┃┈┈╭╰╯╰╯╮`"
                     "`\n┫┈┈  NoU\n┃┈╰╰━━━━╯`"
                     "`\n┗━━┻━┛`")



@borg.on(admin_cmd(outgoing=True, pattern="mf$"))
async def gtfo(e):
        await e.edit(
"\n......................................../´¯/) "
"\n......................................,/¯../ "
"\n...................................../..../ "
"\n..................................../´.¯/"
"\n..................................../´¯/"
"\n..................................,/¯../ "
"\n................................../..../ "
"\n................................./´¯./"
"\n................................/´¯./"
"\n..............................,/¯../ "
"\n............................./..../ "
"\n............................/´¯/"
"\n........................../´¯./"
"\n........................,/¯../ "
"\n......................./..../ "
"\n....................../´¯/"
"\n....................,/¯../ "
"\n.................../..../ "
"\n............./´¯/'...'/´¯¯`·¸ "
"\n........../'/.../..../......./¨¯\ "
"\n........('(...´...´.... ¯~/'...') "
"\n.........\.................'...../ "
"\n..........''...\.......... _.·´ "
"\n............\..............( "
"\n..............\.............\...")



@borg.on(admin_cmd(outgoing=True, pattern="sayhi$"))
async def shalom(e):
    await e.edit(
        "\n💛💛💛💛💛💛💛💛💛"
        "\n💛🔷🔷🔷🔷🔷🔷🔷💛"
        "\n💛💛💛💛🔷💛💛💛💛"
        "\n💛💛💛💛🔷💛💛💛💛"
        "\n💛💛💛💛🔷💛💛💛💛"
        "\n💛🔷🔷🔷🔷️🔷🔷🔷💛"
        "\n💛💛💛💛💛💛💛💛💛"
        "\n💛💛💛💛💛💛💛💛💛"
        "\n💛🔷💛💛️💛💛💛🔷💛"
        "\n💛🔷🔷🔷🔷🔷🔷🔷💛"
        "\n💛🔷🔷🔷🔷🔷🔷️🔷💛"
        "\n💛🔷💛💛💛💛️💛🔷💛"
        "\n💛💛💛💛💛💛💛💛💛")

@borg.on(admin_cmd(outgoing=True, pattern=r"(?:penis|dick)\s?(.)?"))
async def emoji_penis(e):
    emoji = e.pattern_match.group(1)
    titid = GAMBAR_TITIT
    if emoji:
        titid = titid.replace('🍆', emoji)
    await e.edit(titid)


@borg.on(admin_cmd(pattern=f"muth", outgoing=True))

async def _(event):

    if event.fwd_from:

        return

    animation_interval = 0.3

    animation_ttl = range(0, 100)
         
    animation_chars = [

            "8✊️===D",

            "8=✊️==D",

            "8==✊️=D",

            "8===✊️D",

            "8==✊️=D",

            "8=✊️==D",

            "8✊️===D",

            "8===✊️D💦",

            "8==✊️=D💦💦",

            "8=✊️==D💦💦💦"

        ]

    for i in animation_ttl:
        
            await asyncio.sleep(animation_interval)
        
            await event.edit(animation_chars[i % 8])

emojis = {
    "yee": "ツ",
    "happy": "(ʘ‿ʘ)",
    "veryhappy": "=͟͟͞͞٩(๑☉ᴗ☉)੭ु⁾⁾",
    "amazed": "ヾ(o✪‿✪o)ｼ",
    "crying": "༎ຶ︵༎ຶ",
    "dicc": "╰U╯☜(◉ɷ◉ )",
    "fek": "╰U╯\n(‿ˠ‿)",
    "ded": "✖‿✖",
    "sad": "⊙︿⊙",
    "lenny": "( ͡°( ͡° ͜ʖ( ͡° ͜ʖ ͡°)ʖ ͡°) ͡°)",
    "idc": "¯\_(ツ)_/¯",
    "f": "😂😂😂😂😂😂😂😂\n😂😂😂😂😂😂😂😂😂\n😂😂\n😂😂\n😂😂😂😂😂😂\n😂😂😂😂😂😂\n😂😂\n😂😂\n😂😂\n😂😂\n😂😂"
}

unpacked_emojis = ""

for emoji in emojis:
    unpacked_emojis += f"`{emoji}`\n"
    
@borg.on(admin_cmd(pattern="emoji ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    try:
        req_emoji = emojis[str(input_str)]
        await event.edit(req_emoji)
    except KeyError:
        await event.edit("Emoji not found!")
