##Created by @Jisan7509
#credit @GulfysHalfyyyy

import asyncio
from userbot.utils import admin_cmd

@borg.on(admin_cmd(pattern=r"ohnoo"))
async def kakashi(bsdk):
    if bsdk.fwd_from:
        return
    animation_interval = 1
    animation_ttl = range(0, 11)
    await bsdk.edit(f"**Ohhh nooooo **💦💦...")
    animation_chars = [
        "**Ohhh Baby..**😈",
        "__**Ohh Yeaah..**__\n\n 😈\n  |\  \n  |  \   \n 8=👊-D\n  |   \         \n 👟 👟       😲",
        "__**Ohh ohhh..**__\n\n 😈\n  |\  \n  |  \   \n  8=👊-D\n  |   \         \n 👟 👟       😲",
        "__**Ohh.. **__\n\n 😈\n  |\  \n  |  \   \n 8=👊-D\n  |   \         \n 👟 👟       😲",
        "__**Ohh baby..**__\n\n 😈\n  |\  \n  |  \   \n8=👊-D💦\n  |   \         \n 👟 👟       😲",
        "__**Yeaah..**__\n\n 😣\n  |\  \n  |  \   \n 8=👊-D💦\n  |   \         \n 👟 👟       😲",
        "__**Yeaah Yaaah..**__\n\n 😣\n  |\  \n  |  \   \n  8=👊-D💦\n  |   \         💦\n 👟 👟       😲",
        "__**Yaah baby..**__\n\n 😘\n  |\  \n  |  \   \n 8=👊-D💦\n  |   \         💦\n 👟 👟       🤤",
        "__**Ohhh..**__\n\n 😍\n  |\  \n  |  \   \n8=👊-D💦\n  |   \         💦\n 👟 👟       🤤",
        "__**Love u..**__\n\n 😘\n  |\  \n  |  \   \n 8=👊-D💦\n  |   \         \n 👟 👟       🤤",
        "__**Love u babe**__\n\n 😍\n  |\  \n  |  \   \n 8=👊-D\n  |   \         \n 👟 👟       🤤",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await bsdk.edit(animation_chars[i % 11])

@borg.on(admin_cmd(pattern=r"ohyaah"))
async def kakashi(baby):
    await baby.edit("**💪💪Ohhh Yeeah Baby**...\n\n"
         "／ イ  ..........(((ヽ   \n"
         "(  ﾉ       ￣—--＼    \n"
         "| (＼  (\🎩/)   ｜    )  \n"
         "ヽ ヽ` ( ͡° ͜ʖ ͡°) _ノ    /  \n"
         " ＼ | ⌒Ｙ⌒ /  /  \n"
         "   ｜ヽ  ｜  ﾉ ／  \n"
         "     ＼トー仝ーイ \n"
         "        ｜ ミ土彡/ \n"
         "         ) \      °   /  \n"
         "        (     \🌿 /  \n"
         "         /       /ѼΞΞΞΞΞΞΞD💨💦\n"
         "      /  /     /      \ \   \  \n"
         "      ( (    ).           ) ).  ) \n"
         "     (      ).            ( |    | \n"
         "      |    /                \    |\n"
         "      👞.                  👞")
                      
