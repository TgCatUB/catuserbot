import asyncio

from . import catub, edit_or_reply

plugin_category = "fun"


@catub.cat_cmd(
    pattern="unoob$",
    command=("unoob", plugin_category),
    info={
        "header": "Fun animation try yourself to know more",
        "usage": "{tr}unoob",
    },
)
async def _(event):
    "animation command"
    animation_interval = 1
    animation_ttl = range(9)
    event = await edit_or_reply(event, "unnoob")
    animation_chars = [
        "EvErYbOdY",
        "iZ",
        "BiGGeSt",
        "NoOoB",
        "uNtiL",
        "YoU",
        "aRriVe",
        "😈",
        "EvErYbOdY iZ BiGGeSt NoOoB uNtiL YoU aRriVe 😈",
    ]
    for i in animation_ttl:
        await event.edit(animation_chars[i % 9])
        await asyncio.sleep(animation_interval)


@catub.cat_cmd(
    pattern="menoob$",
    command=("menoob", plugin_category),
    info={
        "header": "Fun animation try yourself to know more",
        "usage": "{tr}menoob",
    },
)
async def _(event):
    "animation command"
    animation_interval = 1
    animation_ttl = range(9)
    event = await edit_or_reply(event, "menoob")
    animation_chars = [
        "EvErYbOdY",
        "iZ",
        "BiGGeSt",
        "NoOoB",
        "uNtiL",
        "i",
        "aRriVe",
        "😈",
        "EvErYbOdY iZ BiGGeSt NoOoB uNtiL i aRriVe 😈",
    ]
    for i in animation_ttl:
        await event.edit(animation_chars[i % 9])
        await asyncio.sleep(animation_interval)


@catub.cat_cmd(
    pattern="upro$",
    command=("upro", plugin_category),
    info={
        "header": "Fun animation try yourself to know more",
        "usage": "{tr}upro",
    },
)
async def _(event):
    "animation command"
    animation_interval = 1
    animation_ttl = range(8)
    event = await edit_or_reply(event, "upro")
    animation_chars = [
        "EvErYbOdY",
        "iZ",
        "PeRu",
        "uNtiL",
        "YoU",
        "aRriVe",
        "😈",
        "EvErYbOdY iZ PeRu uNtiL YoU aRriVe 😈",
    ]
    for i in animation_ttl:
        await event.edit(animation_chars[i % 8])
        await asyncio.sleep(animation_interval)


@catub.cat_cmd(
    pattern="mepro$",
    command=("mepro", plugin_category),
    info={
        "header": "Fun animation try yourself to know more",
        "usage": "{tr}mepro",
    },
)
async def _(event):
    "animation command"
    animation_interval = 1
    animation_ttl = range(8)
    event = await edit_or_reply(event, "mepro")
    animation_chars = [
        "EvErYbOdY",
        "iZ",
        "PeRu",
        "uNtiL",
        "i",
        "aRriVe",
        "😈",
        "EvErYbOdY iZ PeRu uNtiL i aRriVe 😈",
    ]
    for i in animation_ttl:
        await event.edit(animation_chars[i % 8])
        await asyncio.sleep(animation_interval)


@catub.cat_cmd(
    pattern="quickheal$",
    command=("quickheal", plugin_category),
    info={
        "header": "Fun animation try yourself to know more",
        "usage": "{tr}quickheal",
    },
)
async def _(event):
    "animation command"
    animation_interval = 5
    animation_ttl = range(11)
    event = await edit_or_reply(event, "quickheal")
    animation_chars = [
        "`Downloading File..`",
        "`File Downloaded....`",
        "`Quick Heal Total Security Checkup\n\n\nSubscription: Pru User\nValid Until: 31/12/2099\n\nFile Scanned... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Quick Heal Total Security Checkup\n\n\nSubscription: Pru User\nValid Until: 31/12/2099\n\nFile Scanned... 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Quick Heal Total Security Checkup\n\n\nSubscription: Pru User\nValid Until: 31/12/2099\n\nFile Scanned... 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Quick Heal Total Security Checkup\n\n\nSubscription: Pru User\nValid Until: 31/12/2099\n\nFile Scanned... 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Quick Heal Total Security Checkup\n\n\nSubscription: Pru User\nValid Until: 31/12/2099\n\nFile Scanned... 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Quick Heal Total Security Checkup\n\n\nSubscription: Pru User\nValid Until: 31/12/2099\n\nFile Scanned... 52%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Quick Heal Total Security Checkup\n\n\nSubscription: Pru User\nValid Until: 31/12/2099\n\nFile Scanned... 84%\n█████████████████████▒▒▒▒ `",
        "`Quick Heal Total Security Checkup\n\n\nSubscription: Pru User\nValid Until: 31/12/2099\n\nFile Scanned... 100%\n█████████████████████████ `",
        "`Quick Heal Total Security Checkup\n\n\nSubscription: Pru User\nValid Until: 31/12/2099\n\nTask: 01 of 01 Files Scanned...\n\nResult: No Virus Found...`",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 11])


@catub.cat_cmd(
    pattern="sqh$",
    command=("sqh", plugin_category),
    info={
        "header": "Fun animation try yourself to know more",
        "usage": "{tr}sqh",
    },
)
async def _(event):
    "animation command"
    animation_interval = 0.1
    animation_ttl = range(11)
    event = await edit_or_reply(event, "sqh")
    animation_chars = [
        "`Downloading File..`",
        "`File Downloaded....`",
        "`Quick Heal Total Security Checkup\n\n\nSubscription: Pru User\nValid Until: 31/12/2099\n\nFile Scanned... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Quick Heal Total Security Checkup\n\n\nSubscription: Pru User\nValid Until: 31/12/2099\n\nFile Scanned... 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Quick Heal Total Security Checkup\n\n\nSubscription: Pru User\nValid Until: 31/12/2099\n\nFile Scanned... 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Quick Heal Total Security Checkup\n\n\nSubscription: Pru User\nValid Until: 31/12/2099\n\nFile Scanned... 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Quick Heal Total Security Checkup\n\n\nSubscription: Pru User\nValid Until: 31/12/2099\n\nFile Scanned... 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Quick Heal Total Security Checkup\n\n\nSubscription: Pru User\nValid Until: 31/12/2099\n\nFile Scanned... 52%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Quick Heal Total Security Checkup\n\n\nSubscription: Pru User\nValid Until: 31/12/2099\n\nFile Scanned... 84%\n█████████████████████▒▒▒▒ `",
        "`Quick Heal Total Security Checkup\n\n\nSubscription: Pru User\nValid Until: 31/12/2099\n\nFile Scanned... 100%\n█████████████████████████ `",
        "`Quick Heal Total Security Checkup\n\n\nSubscription: Pru User\nValid Until: 31/12/2099\n\nTask: 01 of 01 Files Scanned...\n\nResult: No Virus Found...`",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 11])


@catub.cat_cmd(
    pattern="vquickheal$",
    command=("vquickheal", plugin_category),
    info={
        "header": "Fun animation try yourself to know more",
        "usage": "{tr}vquickheal",
    },
)
async def _(event):
    "animation command"
    animation_interval = 5
    animation_ttl = range(11)
    event = await edit_or_reply(event, "vquickheal")
    animation_chars = [
        "`Downloading File..`",
        "`File Downloaded....`",
        "`Quick Heal Total Security Checkup\n\n\nSubscription: Pru User\nValid Until: 31/12/2099\n\nFile Scanned... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Quick Heal Total Security Checkup\n\n\nSubscription: Pru User\nValid Until: 31/12/2099\n\nFile Scanned... 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Quick Heal Total Security Checkup\n\n\nSubscription: Pru User\nValid Until: 31/12/2099\n\nFile Scanned... 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Quick Heal Total Security Checkup\n\n\nSubscription: Pru User\nValid Until: 31/12/2099\n\nFile Scanned... 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Quick Heal Total Security Checkup\n\n\nSubscription: Pru User\nValid Until: 31/12/2099\n\nFile Scanned... 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Quick Heal Total Security Checkup\n\n\nSubscription: Pru User\nValid Until: 31/12/2099\n\nFile Scanned... 52%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Quick Heal Total Security Checkup\n\n\nSubscription: Pru User\nValid Until: 31/12/2099\n\nFile Scanned... 84%\n█████████████████████▒▒▒▒ `",
        "`Quick Heal Total Security Checkup\n\n\nSubscription: Pru User\nValid Until: 31/12/2099\n\nFile Scanned... 100%\n█████████████████████████ `",
        "`Quick Heal Total Security Checkup\n\n\nSubscription: Pru User\nValid Until: 31/12/2099\n\nTask: 01 of 01 Files Scanned...\n\nResult:⚠️Virus Found⚠️\nMore Info: Torzan, Spyware, Adware`",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 11])


@catub.cat_cmd(
    pattern="macoc$",
    command=("macoc", plugin_category),
    info={
        "header": "Fun animation try yourself to know more",
        "usage": "{tr}macoc",
    },
)
async def _(event):
    "animation command"
    animation_interval = 0.5
    animation_ttl = range(11)
    event = await edit_or_reply(event, "macos")
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
        "`Welcome...\n\nStock OS: Symbian OS\nCurrent OS: Hackintosh`\n\n**My PC Specs:**\n\n **CPU:** __2.9GHz Intel Core i9-8950HK (hexa-core, 12MB cache, up to 4.8GHz)__\n\n**Graphics:** __Nvidia GeForce GTX 1080 OC (8GB GDDR5X)__\n\n**RAM:** __32GB DDR4 (2,666MHz)__\n\n**Screen:** __17.3-inch, QHD (2,560 x 1,440) 120Hz G-Sync__\n\n**Storage:** __512GB PCIe SSD, 1TB HDD (7,200 rpm)__\n\n**Ports:** __2 x USB 3.0, 1 x USB-C 3.0, 1 x USB-C (Thunderbolt 3), HDMI, mini DisplayPort, Ethernet, headphone jack, microphone jack__\n\n**Connectivity:** __Killer 1550 802.11ac Wi-Fi, Bluetooth 5.0__\n\n**Camera:** __Alienware FHD camera, Tobii IR Eye-tracking with Windows Hello__\n\n**Size:** __16.7 x 13.1 x 1.18 inches (42.4 x 33.2 x 2.99cm; W x D x H)__",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 11])


@catub.cat_cmd(
    pattern="windows$",
    command=("windows", plugin_category),
    info={
        "header": "Fun animation try yourself to know more",
        "usage": "{tr}windows",
    },
)
async def _(event):
    "animation command"
    animation_interval = 0.5
    animation_ttl = range(11)
    event = await edit_or_reply(event, "windows")
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
        "`Welcome...\n\nStock OS: Symbian OS\nCurrent OS: Windows 10`\n\n**My PC Specs:**\n\n **CPU:** __3.4GHz ryzen 9 5950x (16-core,32 threads 64MB cache, up to 4.9GHz)__\n\n**Graphics:** __Nvidia GeForce RTX 3090 OC (24GB GDDR6X)__\n\n**RAM:** __64GB DDR4 (4000MHz)__\n\n**Screen:** __17.3-inch, UHD (3840 x 2160) 144Hz Hdr G-Sync__\n\n**Storage:** __512GB nvme gen 4 SSD, 5 TB HDD (7,200 rpm)__\n\n**Ports:** __2 x USB 3.1, 1 x USB-C 3.0, 1 x USB-C (Thunderbolt 3), 2 HDMI2.0, mini DisplayPort, Ethernet, headphone jack, microphone jack__\n\n**Connectivity:** __Killer 1550 802.11ac Wi-Fi, Bluetooth 5.0__\n\n**Camera:** __Alienware FHD camera, Tobii IR Eye-tracking with Windows Hello__\n\n**Size:** __16.7 x 13.1 x 1.18 inches (42.4 x 33.2 x 2.99cm; W x D x H)__",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 11])


@catub.cat_cmd(
    pattern="linux$",
    command=("linux", plugin_category),
    info={
        "header": "Fun animation try yourself to know more",
        "usage": "{tr}linux",
    },
)
async def _(event):
    "animation command"
    animation_interval = 0.5
    animation_ttl = range(11)
    event = await edit_or_reply(event, "linux")
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
        "`Welcome...\n\nStock OS: Symbian OS\nCurrent OS: Linux`\n\n**My PC Specs:**\n\n **CPU:** __2.9GHz Intel Core i9-8950HK (hexa-core, 12MB cache, up to 4.8GHz)__\n\n**Graphics:** __Nvidia GeForce GTX 1080 OC (8GB GDDR5X)__\n\n**RAM:** __32GB DDR4 (2,666MHz)__\n\n**Screen:** __17.3-inch, QHD (2,560 x 1,440) 120Hz G-Sync__\n\n**Storage:** __512GB PCIe SSD, 1TB HDD (7,200 rpm)__\n\n**Ports:** __2 x USB 3.0, 1 x USB-C 3.0, 1 x USB-C (Thunderbolt 3), HDMI, mini DisplayPort, Ethernet, headphone jack, microphone jack__\n\n**Connectivity:** __Killer 1550 802.11ac Wi-Fi, Bluetooth 5.0__\n\n**Camera:** __Alienware FHD camera, Tobii IR Eye-tracking with Windows Hello__\n\n**Size:** __16.7 x 13.1 x 1.18 inches (42.4 x 33.2 x 2.99cm; W x D x H)__",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 11])


@catub.cat_cmd(
    pattern="stock$",
    command=("stock", plugin_category),
    info={
        "header": "Fun animation try yourself to know more",
        "usage": "{tr}stock",
    },
)
async def _(event):
    "animation command"
    animation_interval = 0.5
    animation_ttl = range(11)
    event = await edit_or_reply(event, "stock")
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
        "`Welcome...\n\nStock OS: Symbian OS\nCurrent OS: Symbian OS`\n\n**My PC Specs:**\n\n **CPU:** __2.9GHz Intel Core i9-8950HK (hexa-core, 12MB cache, up to 4.8GHz)__\n\n**Graphics:** __Nvidia GeForce GTX 1080 OC (8GB GDDR5X)__\n\n**RAM:** __32GB DDR4 (2,666MHz)__\n\n**Screen:** __17.3-inch, QHD (2,560 x 1,440) 120Hz G-Sync__\n\n**Storage:** __512GB PCIe SSD, 1TB HDD (7,200 rpm)__\n\n**Ports:** __2 x USB 3.0, 1 x USB-C 3.0, 1 x USB-C (Thunderbolt 3), HDMI, mini DisplayPort, Ethernet, headphone jack, microphone jack__\n\n**Connectivity:** __Killer 1550 802.11ac Wi-Fi, Bluetooth 5.0__\n\n**Camera:** __Alienware FHD camera, Tobii IR Eye-tracking with Windows Hello__\n\n**Size:** __16.7 x 13.1 x 1.18 inches (42.4 x 33.2 x 2.99cm; W x D x H)__",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 11])


@catub.cat_cmd(
    pattern="os$",
    command=("os", plugin_category),
    info={
        "header": "Fun animation try yourself to know more",
        "usage": "{tr}os",
    },
)
async def _(event):
    "animation command"
    animation_interval = 0.1
    animation_ttl = range(7)
    event = await edit_or_reply(event, "os")
    animation_chars = [
        "`Scanning OS...`",
        "`Scanning OS......`",
        "__Current Loaded OS: Symbian OS__\n\n**To Boot Other OS, Use The Following Trigger:**\n☑️ `.macos`\n☑️ `.windows`\n☑️ `.linux`\n☑️ `.stock`",
        "__Current Loaded OS: Symbian OS__\n\n**To Boot Other OS, Use The Following Trigger:**\n✅ `.macos`\n☑️ `.windows`\n☑️ `.linux`\n☑️ `.stock`",
        "__Current Loaded OS: Symbian OS__\n\n**To Boot Other OS, Use The Following Trigger:**\n✅ `.macos`\n✅ `.windows`\n☑️ `.linux`\n☑️ `.stock`",
        "__Current Loaded OS: Symbian OS__\n\n**To Boot Other OS, Use The Following Trigger:**\n✅ `.macos`\n✅ `.windows`\n✅ `.linux`\n☑️ `.stock`",
        "__Current Loaded OS: Symbian OS__\n\n**To Boot Other OS, Use The Following Trigger:**\n✅ `.macos`\n✅ `.windows`\n✅ `.linux`\n✅ `.stock`\n\nDeveloped By: @catuserbot17",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 7])
