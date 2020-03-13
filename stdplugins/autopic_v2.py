"""
Time In Profile Pic.....
Command: `.autopp`

:::::Credit Time::::::
1) Coded By: @s_n_a_p_s
2) Ported By: @r4v4n4 (Noodz Lober)
3) End Game Help By: @spechide
4) Custom / Modified Plugin for some magical effects by this Legendary Guy @PhycoNinja13b

If U Noob Don't Play with Codes!! Learn Programming Then Come Here!! 
If u use this plugin without Permit, Then ur mama Gey! Ur father Lesbo!! 

TROJAN ALERT!!!

#curse: who ever edits this credit section will goto hell

⚠️DISCLAIMER⚠️

USING THIS PLUGIN CAN RESULT IN ACCOUNT BAN + CAS BAN + SPAM BAN + ACCOUNT SUSPENSION . WE DONT CARE ABOUT BAN, SO WE ARR USING THIS.
"""
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from pySmartDL import SmartDL
from telethon.tl import functions
from uniborg.util import admin_cmd
import asyncio
import shutil 
import random, re


FONT_FILE_TO_USE = "Fonts/ArchitectsDaughter.ttf"
CAPTION_FONT = "Fonts/Tangerine_Bold.ttf"
#Add telegraph media links of profile pics that are to be used
TELEGRAPH_MEDIA_LINKS = ["https://telegra.ph/file/7bf34f4f660a5f267427c.jpg",#1
                         "https://telegra.ph/file/36f9cfd97adc06bb421c3.jpg",#2
                         "https://telegra.ph/file/180339377beac7566a813.jpg",#3
                         "https://telegra.ph/file/7b429ac29e2ad9f1cc430.jpg",#4
                         "https://telegra.ph/file/e0c109d2daabfe4b2fbe8.jpg",#5
                         "https://telegra.ph/file/a78d290914947f057e4dc.jpg",#6
                         "https://telegra.ph/file/ac61ab7de0fbcc13f4d1d.jpg",#7
                         "https://telegra.ph/file/af33ec6241a14b98b27fb.jpg",#8
                         "https://telegra.ph/file/86bd29ffe67b8f742347e.jpg",#9
                         "https://telegra.ph/file/1804a0db32ce314dcbdad.jpg",#10
                         "https://telegra.ph/file/1437c9d51050b04a76946.jpg",#11
                         "https://telegra.ph/file/b1e65396f9349e3a646b7.jpg",#12
                         "https://telegra.ph/file/221d287c7d906d62bc998.jpg",#13
                         "https://telegra.ph/file/c5985d986d307dbe6a2fc.jpg",#14
                         "https://telegra.ph/file/4720409d42b6ddd8f38d4.jpg",#15
                         "https://telegra.ph/file/b4ed05106b8180b5133e1.jpg",#16
                         "https://telegra.ph/file/73ebf7957ecff2a8e8c7a.jpg",#17
                         "https://telegra.ph/file/e9d84e798aafa7ef4b650.jpg",#18
                         "https://telegra.ph/file/8661cf3a0ce4463a77b9f.jpg",#19
                         "https://telegra.ph/file/8878107fb4e0ab5d9febf.jpg",#20
                         "https://telegra.ph/file/88c585ffe5a3e2e278574.jpg",#21
                         "https://telegra.ph/file/9f9e647bc98b8993be796.jpg",#22
                         "https://telegra.ph/file/421481b9bbcfc5a183323.jpg",#23
                         "https://telegra.ph/file/345d40b3d20cdd504f2f9.jpg",#24
                         "https://telegra.ph/file/172b69e6e4d14928f01c8.jpg",#25
                         "https://telegra.ph/file/e75925b3ecc50ef334e93.jpg",#26
                         "https://telegra.ph/file/28c40315b599536a4b9e1.jpg",#27
                         "https://telegra.ph/file/b0f411aae05d81885200c.jpg",#28
                         "https://telegra.ph/file/ccc3b767ff31bafafd13b.jpg",#29
                         "https://telegra.ph/file/87c3b6bce1c4e3d45be28.jpg",#30
                         "https://telegra.ph/file/4c74f6c28dfc54c3ea6df.jpg",#31
                         "https://telegra.ph/file/560520795122b7e0b0337.jpg",#32
                         "https://telegra.ph/file/9c0122b59ba1f47be441a.jpg",#33
                         "https://telegra.ph/file/a7723bf114636ccf87a32.jpg",#34
                         "https://telegra.ph/file/f79924691e6da3631214d.jpg",#35
                         "https://telegra.ph/file/1e1935cdc29942b171f42.jpg",#36
                         "https://telegra.ph/file/37bd37eca582ee3b0468e.jpg",#37
                         "https://telegra.ph/file/f9d322be52f493f3671fc.jpg",#38
                         "https://telegra.ph/file/8a546023badf9634de44d.jpg",#39
                         "https://telegra.ph/file/0c5044cabd94bd92a34a3.jpg",#40
                         "https://telegra.ph/file/aa4753127cbf1f8e9b8b6.jpg",#41
                         "https://telegra.ph/file/4addb937d3361f6da0a41.jpg",#42
                         "https://telegra.ph/file/761cbd5f00bec18fdd26e.jpg",#43
                         "https://telegra.ph/file/9b71ff72ed6ff49778abc.jpg",#44
                         "https://telegra.ph/file/06a8438b6d849bacb43ec.jpg",#45
                         "https://telegra.ph/file/957b5e204ac62daab4c02.jpg",#46
                         "https://telegra.ph/file/b391dcebf0bb3b4919ad4.jpg",#47
                         "https://telegra.ph/file/008938cf6dee6c3c7a005.jpg",#48
                         "https://telegra.ph/file/f2b531f2e6d6411e8f61f.jpg",#49
                         "https://telegra.ph/file/38eb23adf6ba2bd1a14ee.jpg",#50
                         "https://telegra.ph/file/3f62dddad60ff7a198e71.jpg",#51
                         "https://telegra.ph/file/5f52ca21d111e4dd911f5.jpg",#52
                         "https://telegra.ph/file/c5c405bb98191f43f1a71.jpg",#53
                         "https://telegra.ph/file/76f667c46eef2bbd1b291.jpg",#54
                         "https://telegra.ph/file/c2cad0975cafc839ab3bb.jpg",#55
                         "https://telegra.ph/file/0f96096bb5bf0431a2e46.jpg",#56
                         "https://telegra.ph/file/74d4ac176512717a1b3e0.jpg",#57
                         "https://telegra.ph/file/af8c40bf59a9ec6ce2297.jpg",#58
                         "https://telegra.ph/file/e12c691b79c66bc44477b.jpg",#59
                         "https://telegra.ph/file/3771ff01f14930c2dfd71.jpg",#60
                         "https://telegra.ph/file/49ce28ce6e860fd63cebd.jpg",#61
                         "https://telegra.ph/file/d5be02df4f57b697eb34f.jpg",#62
                         "https://telegra.ph/file/d56e31d6fd199695e12a4.jpg",#63
                         "https://telegra.ph/file/0c5a92dbbf3f5b787df24.jpg",#64
                         "https://telegra.ph/file/316043d4de3df580d0c9b.jpg",#65
                         "https://telegra.ph/file/b0403367d70f9f8a4ceaf.jpg",#66
                         "https://telegra.ph/file/4e0b3c716837646ffd435.jpg",#67
                         "https://telegra.ph/file/77ae1802bd4a3d0a5bd03.jpg",#68
                         "https://telegra.ph/file/f96f65017297e3e338786.jpg",#69
                         "https://telegra.ph/file/42c8f53975e23dcd3a700.jpg",#70
                         "https://telegra.ph/file/6d5438340e3815fafe661.jpg",#71
                         "https://telegra.ph/file/ba68fa53af8f40394bcbe.jpg",#72
                         "https://telegra.ph/file/4c737ee35f901d009eaa0.jpg",#73
                         "https://telegra.ph/file/2101fca6d06c405e9aa82.jpg",#74
                         "https://telegra.ph/file/626e70521bc56f4dc9beb.jpg",#75
                         "https://telegra.ph/file/1433c80e2055d68d0d59c.jpg",#76
                         "https://telegra.ph/file/0a09a5a62144c9d4b43f7.jpg",#77
                         "https://telegra.ph/file/8760afd08fefcac814867.jpg",#78
                         "https://telegra.ph/file/5d9ec0a591fba3878e587.jpg",#79
                         "https://telegra.ph/file/d3576c072c5ebe7c03b0a.jpg",#80
                         "https://telegra.ph/file/fc64586442cfa38216546.jpg",#81
                         "https://telegra.ph/file/3fe749fd4ceaa16f452ee.jpg",#82
                         "https://telegra.ph/file/8fdf6d7245fd17ba6a7e6.jpg",#83
                         "https://telegra.ph/file/8dfafb57169050ea35096.jpg",#84
                         "https://telegra.ph/file/542c981728754a08a5d76.jpg",#85
                         "https://telegra.ph/file/96df071e4d23d5f632dc3.jpg",#86
                         "https://telegra.ph/file/4e8ce18f9f77e4b05036f.jpg",#87
                         "https://telegra.ph/file/e801ca9882c87c51554fc.jpg",#88
                         "https://telegra.ph/file/1588dcb2ada747be2398b.jpg",#89
                         "https://telegra.ph/file/13363e8de5424ebee6331.jpg",#90
                         "https://telegra.ph/file/13966487d61bf9a106ace.jpg",#91
                         "https://telegra.ph/file/fd215a6615eb80a5a4793.jpg",#92
                         "https://telegra.ph/file/e88fd1d0ebecabce5b4a9.jpg",#93
                         "https://telegra.ph/file/116ed2adaa26b7ce95b33.jpg",#94
                         "https://telegra.ph/file/c75834f633a01c146494e.jpg",#95
                         "https://telegra.ph/file/414368b1ce56d3c692e0d.jpg",#96
                         "https://telegra.ph/file/bdeead924afc42d5daa56.jpg",#97
                         "https://telegra.ph/file/adfdce9d79921f5f25943.jpg",#98
                         "https://telegra.ph/file/c412af6cdf9cfdab786ec.jpg",#99
                         "https://telegra.ph/file/f8c8bef0114fc92f936b1.jpg",#100
                         "https://telegra.ph/file/3e24e82a91c0165bbce92.jpg",#101
                         "https://telegra.ph/file/54b0998e0c33f042c9d56.jpg",#102
                         "https://telegra.ph/file/5f2ad3cc273543c2ae547.jpg",#103
                         "https://telegra.ph/file/ccec12eeeddcbc77bc146.jpg",#104
                         "https://telegra.ph/file/a9674171c75e32a4aaa81.jpg",#105
                         "https://telegra.ph/file/b3a0729e9cef797396215.jpg",#106
                         "https://telegra.ph/file/5a1e5378915de1672fb2f.jpg",#107
                         "https://telegra.ph/file/5de0991e7a6728cbed9ea.jpg",#108
                         "https://telegra.ph/file/d2a8cdbcd9af25e524726.jpg",#109
                         "https://telegra.ph/file/b78d92fcd0c45bff9f3a4.jpg",#110
                         "https://telegra.ph/file/b2628094ff25da273ef0b.jpg",#111
                         "https://telegra.ph/file/5368ef86099de439743d2.jpg",#112
                         "https://telegra.ph/file/ac178c67651dd9c62e310.jpg",#113
                         "https://telegra.ph/file/a5af026478b4baaa6860b.jpg",#114
                         "https://telegra.ph/file/799684abcc27bfad3fdfe.jpg",#115
                         "https://telegra.ph/file/b9d16b0cdd199fe84ca07.jpg",#116
                         "https://telegra.ph/file/280679fb793b0af677df2.jpg",#117
                         "https://telegra.ph/file/d6740b6a45db9cf20476c.jpg",#118
                         "https://telegra.ph/file/dbf52ddc0486ddead0b41.jpg",#119
                         "https://telegra.ph/file/fd82ce40c7ceb97706c11.jpg",#120
                         "https://telegra.ph/file/a4b41de83c493a41dede3.jpg",#121
                         "https://telegra.ph/file/aef80fdb31cd710cdcc09.jpg",#122
                         "https://telegra.ph/file/6000d833cd6f49b250222.jpg",#123
                         "https://telegra.ph/file/3cd2c017b1b0101899ae0.jpg",#124
                         "https://telegra.ph/file/035d4f324c43e0164e487.jpg",#125
                         "https://telegra.ph/file/cff668c01cc6324535e65.jpg",#126
                         "https://telegra.ph/file/398c02b9fd24aa0351176.jpg",#127
                         "https://telegra.ph/file/028f19c020c3441cf96e9.jpg",#128
                         "https://telegra.ph/file/d1b80277398781b2808fa.jpg",#129
                         "https://telegra.ph/file/47afa35e3da8a749830fc.jpg",#130
                         "https://telegra.ph/file/b0f9d7a1cf6f3f2448458.jpg",#131
                         "https://telegra.ph/file/1b8fc058066ef4c13e1d7.jpg",#132
                         "https://telegra.ph/file/d75ff1a21722afe15e1f3.jpg",#133
                         "https://telegra.ph/file/b8b5d2b5fe64af8668e1f.jpg",#134
                         "https://telegra.ph/file/8dbf6da7f402eba89b8d4.jpg",#135
                         "https://telegra.ph/file/0568995e8d71f31cc5d9c.jpg",#136
                         "https://telegra.ph/file/487904cd734797f9156f9.jpg",#137
                         "https://telegra.ph/file/d1c3ce16b6964f5d2c259.jpg",#138
                         "https://telegra.ph/file/4afada63b5eb3a159e63d.jpg",#139
                         "https://telegra.ph/file/dc70f8b34b996f5afa1fe.jpg",#140
                         "https://telegra.ph/file/f44cf843384c85fd5e0b2.jpg",#141
                         "https://telegra.ph/file/0576d6cd6f0275b5f0e92.jpg",#142
                         "https://telegra.ph/file/bf9ac95ec344c77ec59c3.jpg",#143
                         "https://telegra.ph/file/969e29b6042142f3335c8.jpg",#144
                         "https://telegra.ph/file/d4a870993ad673f31ff43.jpg",#145
                         "https://telegra.ph/file/13db1c43c648ea9c16ca0.jpg",#146
                         "https://telegra.ph/file/11137946091f5dae31dcf.jpg",#147
                         "https://telegra.ph/file/0ae3d2580f7222b65ff9a.jpg" #148

                        ]
@borg.on(admin_cmd(pattern="autopp ?(.*)"))
async def autopic(event):
    while True:
        piclink = random.randint(0, len(TELEGRAPH_MEDIA_LINKS) - 1)
        AUTOPP = TELEGRAPH_MEDIA_LINKS[piclink]
        downloaded_file_name = "./ravana/original_pic.png"
        downloader = SmartDL(AUTOPP, downloaded_file_name, progress_bar=True)
        downloader.start(blocking=False)
        photo = "photo_pfp.png"
        while not downloader.isFinished():
            place_holder = None
    
    
        shutil.copy(downloaded_file_name, photo)
        im = Image.open(photo)
        current_time = datetime.now().strftime("\n \n \n Time: %H:%M:%S \n Date: %d/%m/%y ")
        caption = "\n \n \n \n \n Take Me Back To The Place I Belong "
        img = Image.open(photo)
        drawn_text = ImageDraw.Draw(img)
        fnt = ImageFont.truetype(FONT_FILE_TO_USE, 23)
        cafnt = ImageFont.truetype(CAPTION_FONT, 50)
        drawn_text.text((310, 530), current_time, font=fnt, fill=(230,230,255))
        drawn_text.text((150, 530), caption, font=cafnt, fill=(221,230,255))
        img.save(photo)
        file = await event.client.upload_file(photo)  # pylint:disable=E0602
        try:
            await event.client(functions.photos.UploadProfilePhotoRequest(  # pylint:disable=E0602
                file
            ))
            os.remove(photo)
            
            await asyncio.sleep(50)
        except:
            return
