# created by @Jisan7509

import asyncio
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

rom_name = """__**Available Roms List :- **__

 `aex` : __Get AospExtended builds __
 `aicp` : __Get Android Ice Cold Project builds __
 `aosip` : __Get Android Open Source illusion Project build __
 `pa` : __Get Paranoid Android (AOSPA) builds __
 `aqua` : __Get latest AquiriOS builds __
 `arrow` : __Get ArrowOS build __
 `bootleg` : __Get Bootleggers builds__ 
 `candy` : __Get CandyROM builds __
 `carbon` : __Get CarbonROM builds __
 `colt` : __Get ColtOS builds __
 `cosp` : __Get COSP builds __
 `crdroid` : __Get crDroid build__ 
 `dotos` : __Get dotOS builds __
 `dump` : __Dump firmware to git.rip__ 
 `evox` : __Get EvolutionX builds __
 `havoc` : __Get HavocOS builds __
 `licrog` : __Get LineageOS microG builds__ 
 `lineage` : __Get LineageOS builds __
 `omni` : __Get OmniROM builds __
 `pe` : __Get PixelExperience builds __
 `pdust` : __Get PixelDust builds __
 `pixys` : __Get PixyOS builds __
 `potato` : __Get POSP builds __
 `revenge` : __Get RevengeOS builds __
 `rr` : __Get ResurrectionRemix builds __
 `superior` : __Get SuperiorOS builds __
 `syberia` : __Get latest SyberiaOS builds__ 
 `viper` : __Get ViperOS builds __
 `xtended` : __Get MSM Xtended builds__"""

device_name = """__**Available Drvice List for Firmware :- **__

 `asus` : __Search Asus firmwares __
 `huawei` : __Search for Huawei firmwares __
 `moto` : __Search for Motorola firmwares __
 `op` : __Get firmwares for OnePlus devices __
 `xiaomi` : __Search for Xiaomi firmwares__"""


dev_name = """__**Available Devloper name for Gcam :- **__

 `AdamB` , `alexey070315` , `alone_in_dark` , `arnova8G2` , `arthur` , `baadnwz` , `backrider` , `boxer198615` , `bsg` , `burial` , `charles` , `cstark27` , `dieflix` , `dpstar7582` , `fractal` , `fu24` , `greatness` , `harysviewty` , `hass31` , `homersp` , `hpengw` , `idan` , `ivanich` , `jairo_rossi` , `jean` , `johngalt` , `kokroo` , `MadnessKnight` , `marcant01` , `marco` , `MarcosMucelin` , `Metzger100` , `mf182` , `miniuser123` , `MWP` , `namok` , `Nikita` , `nullbytepl` , `ojosehenrick` , `onfire` , `overwhelmer` , `PERCIFHM34` , `PitbulL` , `raznoptid` , `rz_end` , `san1ty` , `saneklic` , `savitar` , `scrubber` , `serjo87` , `sipollo` , `skulshady` , `the_dise` , `tigr` , `tolyan009` , `UltraM8` , `urikill` , `urnyx05` , `wichaya` , `wyroczen` , `xenius9` , `xtrme` , `zoran`"""
 
tools = """__**Available Android Tools :- **__

`microg` , `gapps` , `nanodroid` , `adb` , `fastboot` , `astudio` , `magisk`"""
 
xiaomi_cmd = """"__**Available Xiaomi commands :- **__

`firmware` , `vendor` , `specs` , `fastboot` , `recovery`"""

@bot.on(admin_cmd(pattern="rom(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="rom(?: |$)(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    details = event.pattern_match.group(1)
    catevent = await edit_or_reply(event, "```Processing...```")
    if not details:
        await catevent.edit(f"{rom_name}")
        return
    kakashi = details
    rom, code = kakashi.split(" ", 1)
    if rom.strip() in ("aex", "aicp","aosip","pa","aqua","arrow","bootlag","candy","carbon","colt","cosp","crdroid","dotos","dump","evox","havoc","licrog","lineage","omni","pe","pdust","pixys","potato","revenge","rr","superior","syberia","viper","extended"):
        await catevent.edit("```Finding Rom details...```")
    else:
        await catevent.edit("```Wrong Rom Name...```")
        await asyncio.sleep(1)
        await catevent.edit(f"{rom_name}")
        return
    async with event.client.conversation("@android_helper_bot") as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=995271804)
            )
            msg = await conv.send_message(f"/{details}")
            respond = await response
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await catevent.edit("```Unblock @android_helper_bot to use this .```")
            return
        else:
            await catevent.delete()
            await event.client.forward_messages(event.chat_id, respond.message)
            await event.client.delete_messages(conv.chat_id, [msg.id, respond.id])


@bot.on(admin_cmd(pattern="xiaomi(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="xiaomi(?: |$)(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    details = event.pattern_match.group(1)
    catevent = await edit_or_reply(event, "```Processing...```")
    if not details:
        await catevent.edit(f"{xiaomi_cmd}")
        return
    kakashi = details
    code, device = kakashi.split(" ", 1)
    if code.strip() in ("firmware", "vendor","specs","fastboot","recovery"):
        await catevent.edit("```Finding details, wait just a sec...```")
    else:
        await catevent.edit("```Wrong Pattern...```")
        await asyncio.sleep(1)
        await catevent.edit(f"{xiaomi_cmd}")
        return
    async with event.client.conversation("@XiaomiGeeksBot") as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=774181428)
            )
            msg = await conv.send_message(f"/{details}")
            respond = await response
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await catevent.edit("```Unblock @XiaomiGeeksBot to use this .```")
            return
        else:
            await catevent.delete()
            await event.client.forward_messages(event.chat_id, respond.message)
            await event.client.delete_messages(conv.chat_id, [msg.id, respond.id])


@bot.on(admin_cmd(pattern="recovery(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="recovery(?: |$)(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    details = event.pattern_match.group(1)
    catevent = await edit_or_reply(event, "```Processing...```")
    if not details:
        await catevent.edit("__**Available Recovery name :- **__\n\n1. `pb`\n2. `of`")
        return
    kakashi = details
    code, device = kakashi.split(" ", 1)
    if code.strip() in ("of", "pb"):
        await catevent.edit("```Finding Recovery, wait just a sec...```")
    else:
        await catevent.edit("```Wrong Pattern...```")
        await asyncio.sleep(1)
        await catevent.edit("__**Available Recovery name :- **__\n\n1. `pb`\n2. `of`")
        return
    async with event.client.conversation("@XiaomiGeeksBot") as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=774181428)
            )
            msg = await conv.send_message(f"/{details}")
            respond = await response
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await catevent.edit("```Unblock @XiaomiGeeksBot to use this .```")
            return
        else:
            await catevent.delete()
            await event.client.forward_messages(event.chat_id, respond.message)
            await event.client.delete_messages(conv.chat_id, [msg.id, respond.id])



@bot.on(admin_cmd(pattern="fw(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="fw(?: |$)(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    details = event.pattern_match.group(1)
    catevent = await edit_or_reply(event, "```Processing...```")
    if not details:
        await catevent.edit(f"{device_name}")
        return
    kakashi = details
    device, code = kakashi.split(" ", 1)
    if device.strip() in ("asus", "huawei","moto","op","xiaomi"):
        await catevent.edit("```Finding Firmware...```")
    else:
        await catevent.edit("```Wrong Device Name...```")
        await asyncio.sleep(1)
        await catevent.edit(f"{device_name}")
        return
    async with event.client.conversation("@android_helper_bot") as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=995271804)
            )
            msg = await conv.send_message(f"/{details}")
            respond = await response
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await catevent.edit("```Unblock @android_helper_bot to use this .```")
            return
        else:
            await catevent.delete()
            await event.client.forward_messages(event.chat_id, respond.message)
            await event.client.delete_messages(conv.chat_id, [msg.id, respond.id])


@bot.on(admin_cmd(pattern="gcam(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="gcam(?: |$)(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    details = event.pattern_match.group(1)
    catevent = await edit_or_reply(event, "```Processing...```")
    if not details:
        await catevent.edit(f"{dev_name}")
        return
    if details in ("AdamB","alexey070315","alone_in_dark","arnova8G2","arthur","baadnwz","backrider","boxer198615","bsg","burial","charles","cstark27","dieflix","dpstar7582","fractal","fu24","greatness","harysviewty","hass31","homersp","hpengw","idan","ivanich","jairo_rossi","jean","johngalt","kokroo","MadnessKnight","marcant01","marco","MarcosMucelin","Metzger100","mf182","miniuser123","MWP","namok","Nikita","nullbytepl","ojosehenrick","onfire","overwhelmer","PERCIFHM34","PitbulL","raznoptid","rz_end","san1ty","saneklic","savitar","scrubber","serjo87","sipollo","skulshady","the_dise","tigr","tolyan009","UltraM8","urikill","urnyx05","wichaya","wyroczen","xenius9","xtrme","zoran"):
        await catevent.edit("```Finding GoogleCamera...```")
    else:
        await catevent.edit("```Wrong Devloper Name...```")
        await asyncio.sleep(1)
        await catevent.edit(f"{dev_name}")
        return
    async with event.client.conversation("@android_helper_bot") as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=995271804)
            )
            msg = await conv.send_message(f"/gcam {details}")
            respond = await response
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await catevent.edit("```Unblock @android_helper_bot to use this .```")
            return
        else:
            await catevent.delete()
            await event.client.forward_messages(event.chat_id, respond.message)
            await event.client.delete_messages(conv.chat_id, [msg.id, respond.id])


@bot.on(admin_cmd(pattern="tool(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="tool(?: |$)(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    details = event.pattern_match.group(1)
    catevent = await edit_or_reply(event, "```Processing...```")
    if not details:
        await catevent.edit(f"{tools}")
        return
    if details in ("microg","gapps","nanodroid","adb","fastboot","astudio","magisk"):
        await catevent.edit("```Finding Android tool...```")
    else:
        await catevent.edit("```Wrong tool Name...```")
        await asyncio.sleep(1)
        await catevent.edit(f"{tools}")
        return
    async with event.client.conversation("@android_helper_bot") as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=995271804)
            )
            msg = await conv.send_message(f"/{details}")
            respond = await response
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await catevent.edit("```Unblock @android_helper_bot to use this .```")
            return
        else:
            await catevent.delete()
            await event.client.forward_messages(event.chat_id, respond.message)
            await event.client.delete_messages(conv.chat_id, [msg.id, respond.id])


CMD_HELP.update(
    {
        "phone": "__**PLUGIN NAME :** Phone__\
    \n\n📌** CMD ➥** `.rom` <rom code> <device code>\
    \n**Example :-** `.rom rr whyred`\
    \n**USAGE   ➥  **Send you the Rom.\
    \n\n📌** CMD ➥** `.fw` <rom code> <device code>\
    \n**Example :-** `.fw xiaomi whyred`\
    \n**USAGE   ➥  **Send you the Firmware.\
    \n\n📌** CMD ➥** `.xiaomi` <xiaomi tool> <device code>\
    \n**Example :-** `.xiaomi fastboot whyred`\
    \n**USAGE   ➥  **Get rom, recovery rom, fastboot of xiaomi devices.\
    \n\n📌** CMD ➥** `.recovery` <pb/of> <device code>\
    \n**Example :-** `.recovery of whyred`\
    \n**USAGE   ➥  **Get recovery for devices.\
    \n\n📌** CMD ➥** `.gapp` <devloper name>\
    \n**Example :-** `.gapp arnova8G2`\
    \n**USAGE   ➥  **Send you google cameras by their devloper name.\
    \n\n📌** CMD ➥** `.tool` <tool name>\
    \n**Example :-** `.tool adb`\
    \n**USAGE   ➥  **To get android tools.\
    \n\n***Note :-** To get all list of rom name,xiaomi, recovery, device name for fimware, tools name or gcam dev name.. use the cmd once without any input\
    "
    }
)