"""Emoji

Available Commands:

.emoji shrug

.emoji apple

.emoji :/

.emoji -_-"""

from telethon import events

import asyncio





@borg.on(events.NewMessage(pattern=r"\.(.*)", outgoing=True))

async def _(event):

    if event.fwd_from:

        return

    animation_interval = 0.5

    animation_ttl = range(0, 11)

    input_str = event.pattern_match.group(1)

    if input_str == "macos":

        await event.edit(input_str)

        animation_chars = [
        
            "`Connecting To Hackintosh...`",
            "`Initiating Hackintosh Login.`",
            "`Loading Hackintosh... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Loading Hackintosh... 3%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Loading Hackintosh... 9%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",    
            "`Loading Hackintosh... 23%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Loading Hackintosh... 39%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Loading Hackintosh... 69%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Loading Hackintosh... 89%\n█████████████████████▒▒▒▒ `",
            "`Loading Hackintosh... 100%\n█████████████████████████ `",
            "`Welcome...\n\nStock OS: Symbian OS\nCurrent OS: Hackintosh`\n\n**My PC Specs:**\n\n **CPU:** __2.9GHz Intel Core i9-8950HK (hexa-core, 12MB cache, up to 4.8GHz)__\n\n**Graphics:** __Nvidia GeForce GTX 1080 OC (8GB GDDR5X)__\n\n**RAM:** __32GB DDR4 (2,666MHz)__\n\n**Screen:** __17.3-inch, QHD (2,560 x 1,440) 120Hz G-Sync__\n\n**Storage:** __512GB PCIe SSD, 1TB HDD (7,200 rpm)__\n\n**Ports:** __2 x USB 3.0, 1 x USB-C 3.0, 1 x USB-C (Thunderbolt 3), HDMI, mini DisplayPort, Ethernet, headphone jack, microphone jack__\n\n**Connectivity:** __Killer 1550 802.11ac Wi-Fi, Bluetooth 5.0__\n\n**Camera:** __Alienware FHD camera, Tobii IR Eye-tracking with Windows Hello__\n\n**Size:** __16.7 x 13.1 x 1.18 inches (42.4 x 33.2 x 2.99cm; W x D x H)__"
        ]

        for i in animation_ttl:

            await asyncio.sleep(animation_interval)

            await event.edit(animation_chars[i % 11])


@borg.on(events.NewMessage(pattern=r"\.(.*)", outgoing=True))

async def _(event):

    if event.fwd_from:

        return

    animation_interval = 0.5

    animation_ttl = range(0, 11)

    input_str = event.pattern_match.group(1)

    if input_str == "windows":

        await event.edit(input_str)

        animation_chars = [
        
            "`Connecting To Windows 10...`",
            "`Initiating Windows 10 Login.`",
            "`Loading Windows 10... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Loading Windows 10... 3%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Loading Windows 10... 9%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",    
            "`Loading Windows 10... 23%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Loading Windows 10... 39%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Loading Windows 10... 69%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Loading Windows 10... 89%\n█████████████████████▒▒▒▒ `",
            "`Loading Windows 10... 100%\n█████████████████████████ `",
            "`Welcome...\n\nStock OS: Symbian OS\nCurrent OS: Windows 10`\n\n**My PC Specs:**\n\n **CPU:** __2.9GHz Intel Core i9-8950HK (hexa-core, 12MB cache, up to 4.8GHz)__\n\n**Graphics:** __Nvidia GeForce GTX 1080 OC (8GB GDDR5X)__\n\n**RAM:** __32GB DDR4 (2,666MHz)__\n\n**Screen:** __17.3-inch, QHD (2,560 x 1,440) 120Hz G-Sync__\n\n**Storage:** __512GB PCIe SSD, 1TB HDD (7,200 rpm)__\n\n**Ports:** __2 x USB 3.0, 1 x USB-C 3.0, 1 x USB-C (Thunderbolt 3), HDMI, mini DisplayPort, Ethernet, headphone jack, microphone jack__\n\n**Connectivity:** __Killer 1550 802.11ac Wi-Fi, Bluetooth 5.0__\n\n**Camera:** __Alienware FHD camera, Tobii IR Eye-tracking with Windows Hello__\n\n**Size:** __16.7 x 13.1 x 1.18 inches (42.4 x 33.2 x 2.99cm; W x D x H)__"
        ]

        for i in animation_ttl:

            await asyncio.sleep(animation_interval)

            await event.edit(animation_chars[i % 11])



@borg.on(events.NewMessage(pattern=r"\.(.*)", outgoing=True))

async def _(event):

    if event.fwd_from:

        return

    animation_interval = 0.5

    animation_ttl = range(0, 11)

    input_str = event.pattern_match.group(1)

    if input_str == "linux":

        await event.edit(input_str)

        animation_chars = [
        
            "`Connecting To Linux...`",
            "`Initiating Linux Login.`",
            "`Loading Linux... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Loading Linux... 3%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Loading Linux... 9%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",    
            "`Loading Linux... 23%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Loading Linux... 39%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Loading Linux... 69%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Loading Linux... 89%\n█████████████████████▒▒▒▒ `",
            "`Loading Linux... 100%\n█████████████████████████ `",
            "`Welcome...\n\nStock OS: Symbian OS\nCurrent OS: Linux`\n\n**My PC Specs:**\n\n **CPU:** __2.9GHz Intel Core i9-8950HK (hexa-core, 12MB cache, up to 4.8GHz)__\n\n**Graphics:** __Nvidia GeForce GTX 1080 OC (8GB GDDR5X)__\n\n**RAM:** __32GB DDR4 (2,666MHz)__\n\n**Screen:** __17.3-inch, QHD (2,560 x 1,440) 120Hz G-Sync__\n\n**Storage:** __512GB PCIe SSD, 1TB HDD (7,200 rpm)__\n\n**Ports:** __2 x USB 3.0, 1 x USB-C 3.0, 1 x USB-C (Thunderbolt 3), HDMI, mini DisplayPort, Ethernet, headphone jack, microphone jack__\n\n**Connectivity:** __Killer 1550 802.11ac Wi-Fi, Bluetooth 5.0__\n\n**Camera:** __Alienware FHD camera, Tobii IR Eye-tracking with Windows Hello__\n\n**Size:** __16.7 x 13.1 x 1.18 inches (42.4 x 33.2 x 2.99cm; W x D x H)__"
        ]

        for i in animation_ttl:

            await asyncio.sleep(animation_interval)

            await event.edit(animation_chars[i % 11])


@borg.on(events.NewMessage(pattern=r"\.(.*)", outgoing=True))

async def _(event):

    if event.fwd_from:

        return

    animation_interval = 0.5

    animation_ttl = range(0, 11)

    input_str = event.pattern_match.group(1)

    if input_str == "stock":

        await event.edit(input_str)

        animation_chars = [
        
            "`Connecting To Symbian OS...`",
            "`Initiating Symbian OS Login.`",
            "`Loading Symbian OS... 0%\n█████████████████████████ `",
            "`Loading Symbian OS... 3%\n█████████████████████▒▒▒▒ `",
            "`Loading Symbian OS... 9%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ `",    
            "`Loading Symbian OS... 23%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Loading Symbian OS... 39%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Loading Symbian OS... 69%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Loading Symbian OS... 89%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Loading Symbian OS... 100%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Welcome...\n\nStock OS: Symbian OS\nCurrent OS: Symbian OS`\n\n**My PC Specs:**\n\n **CPU:** __2.9GHz Intel Core i9-8950HK (hexa-core, 12MB cache, up to 4.8GHz)__\n\n**Graphics:** __Nvidia GeForce GTX 1080 OC (8GB GDDR5X)__\n\n**RAM:** __32GB DDR4 (2,666MHz)__\n\n**Screen:** __17.3-inch, QHD (2,560 x 1,440) 120Hz G-Sync__\n\n**Storage:** __512GB PCIe SSD, 1TB HDD (7,200 rpm)__\n\n**Ports:** __2 x USB 3.0, 1 x USB-C 3.0, 1 x USB-C (Thunderbolt 3), HDMI, mini DisplayPort, Ethernet, headphone jack, microphone jack__\n\n**Connectivity:** __Killer 1550 802.11ac Wi-Fi, Bluetooth 5.0__\n\n**Camera:** __Alienware FHD camera, Tobii IR Eye-tracking with Windows Hello__\n\n**Size:** __16.7 x 13.1 x 1.18 inches (42.4 x 33.2 x 2.99cm; W x D x H)__"
        ]

        for i in animation_ttl:

            await asyncio.sleep(animation_interval)

            await event.edit(animation_chars[i % 11])


@borg.on(events.NewMessage(pattern=r"\.(.*)", outgoing=True))

async def _(event):

    if event.fwd_from:

        return

    animation_interval = 0.1

    animation_ttl = range(0, 7)

    input_str = event.pattern_match.group(1)

    if input_str == "os":

        await event.edit(input_str)

        animation_chars = [
        
            "`Scanning OS...`",
            "`Scanning OS......`",
            "__Current Loaded OS: Symbian OS__\n\n**To Boot Other OS, Use The Following Trigger:**\n☑️ `.macos`\n☑️ `.windows`\n☑️ `.linux`\n☑️ `.stock`",
            "__Current Loaded OS: Symbian OS__\n\n**To Boot Other OS, Use The Following Trigger:**\n✅ `.macos`\n☑️ `.windows`\n☑️ `.linux`\n☑️ `.stock`",
            "__Current Loaded OS: Symbian OS__\n\n**To Boot Other OS, Use The Following Trigger:**\n✅ `.macos`\n✅ `.windows`\n☑️ `.linux`\n☑️ `.stock`",
            "__Current Loaded OS: Symbian OS__\n\n**To Boot Other OS, Use The Following Trigger:**\n✅ `.macos`\n✅ `.windows`\n✅ `.linux`\n☑️ `.stock`",
            "__Current Loaded OS: Symbian OS__\n\n**To Boot Other OS, Use The Following Trigger:**\n✅ `.macos`\n✅ `.windows`\n✅ `.linux`\n✅ `.stock`\n\nDeveloped By: @shivamkchoudhary"
 ]

        for i in animation_ttl:

            await asyncio.sleep(animation_interval)

            await event.edit(animation_chars[i % 7])
