# BY @Deonnn
""" Game of Thrones Dialogues That You Can Use In Everyday Situations
 command .gotm
 by @Deonnn
"""

from telethon import events

import asyncio

import os

import sys

import random



@borg.on(events.NewMessage(pattern=r"\.gotm", outgoing=True))

async def _(event):

    if event.fwd_from:

        return

    await event.edit("Thinking... 🤔")

    await asyncio.sleep(2)

    x=(random.randrange(1,30))

    if x==1:

        await event.edit("[To your teachers on failing you in all your papers confidently, every time...](https://telegra.ph/file/431d178780f9bff353047.jpg)", link_preview=True)

    if x==2:

        await event.edit("[A shift from the mainstream darling, sweetheart, jaanu, and what not...](https://telegra.ph/file/6bbb86a6c7d2c4a61e102.jpg)", link_preview=True)

    if x==3:

        await event.edit("[To the guy who's friendzone-ing you...](https://telegra.ph/file/8930b05e9535e9b9b8229.jpg)", link_preview=True)

    if x==4:

        await event.edit("[When your friend asks for his money back...](https://telegra.ph/file/2df575ab38df5ce9dbf5e.jpg)", link_preview=True)

    if x==5:

        await event.edit("[A bad-ass reply to who do you think you are?](https://telegra.ph/file/3a35a0c37f4418da9f702.jpg)", link_preview=True)

    if x==6:

        await event.edit("[When the traffic police stops your car and asks for documents...](https://telegra.ph/file/52612d58d6a61315a4c3a.jpg)", link_preview=True)

    if x==7:

        await event.edit("[ When your friend asks about the food he/she just cooked and you don't want to break his/her heart...](https://telegra.ph/file/702df36088f5c26fef931.jpg)", link_preview=True)    

    if x==8:

        await event.edit("[When you're out of words...](https://telegra.ph/file/ba748a74bcab4a1135d2a.jpg)", link_preview=True)

    if x==9:

        await event.edit("[When you realize your wallet is empty...](https://telegra.ph/file/a4508324b496d3d4580df.jpg)", link_preview=True)

    if x==10:

        await event.edit("[When shit is about to happen...](https://telegra.ph/file/e15d9d64f9f25e8d05f19.jpg)", link_preview=True)

    if x==11:

        await event.edit("[When that oversmart classmate shouts a wrong answer in class...](https://telegra.ph/file/1a225a2e4b7bfd7f7a809.jpg)", link_preview=True)

    if x==12:

        await event.edit("[When things go wrong in a big fat Indian wedding...](https://telegra.ph/file/db69e17e85bb444caca32.jpg)", link_preview=True)

    if x==13:

        await event.edit("[A perfect justification for breaking a promise...](https://telegra.ph/file/0b8fb8fb729d157844ac9.jpg)", link_preview=True)

    if x==14:

        await event.edit("[When your friend just won't stop LOL-ing on something silly you said...](https://telegra.ph/file/247fa54106c32318797ae.jpg)", link_preview=True)

    if x==15:

        await event.edit("[When someone makes a joke on you...](https://telegra.ph/file/2ee216651443524eaafcf.jpg)", link_preview=True)

    if x==16:

        await event.edit("[When your professor insults you in front of the class...](https://telegra.ph/file/a2dc7317627e514a8e180.jpg)", link_preview=True)

    if x==17:

        await event.edit("[When your job interviewer asks if you're nervous...](https://telegra.ph/file/9cc147d0bf8adbebf164b.jpg)", link_preview=True)

    if x==18:

        await event.edit("[When you're sick of someone complaining about the heat outside...](https://telegra.ph/file/9248635263c52b968f968.jpg)", link_preview=True)

    if x==19:

        await event.edit("[When your adda is occupied by outsiders...](https://telegra.ph/file/ef537007ba6d9d4cbd384.jpg)", link_preview=True)

    if x==20:

        await event.edit("[When you don't have the right words to motivate somebody...](https://telegra.ph/file/2c932d769ae4c5fbed368.jpg)", link_preview=True)

    if x==21:

        await event.edit("[When the bouncer won't let you and your group of friends in because you're all under-aged...](https://telegra.ph/file/6c8ca79f1e20ebd04391c.jpg)", link_preview=True)

    if x==22:

        await event.edit("[To the friend who wants you to take the fall for his actions...](https://telegra.ph/file/d4171b9bc9104b5d972d9.jpg)", link_preview=True)

    if x==23:

        await event.edit("[When that prick of a bully wouldn't take your words seriously...](https://telegra.ph/file/188d73bd24cf866d8d8d0.jpg)", link_preview=True)

    if x==24:

        await event.edit("[ When you're forced to go shopping/watch a football match with your partner...](https://telegra.ph/file/6e129f138c99c1886cb2b.jpg)", link_preview=True)

    if x==25:

        await event.edit("[To the large queue behind you after you get the last concert/movie ticket...](https://telegra.ph/file/2423f213dd4e4282a31ea.jpg)", link_preview=True)

    if x==26:

        await event.edit("[When your parents thought you'd fail but you prove them wrong...](https://telegra.ph/file/39cc5098466f622bf21e3.jpg)", link_preview=True)

    if x==27:

        await event.edit("[A justification for not voting!](https://telegra.ph/file/87d475a8f9a8350d2450e.jpg)", link_preview=True)

    if x==28:

        await event.edit("[When your partner expects you to do too many things...](https://telegra.ph/file/68bc768d36e08862bf94e.jpg)", link_preview=True)

    if x==29:

        await event.edit("[When your friends cancel on the plan you made at the last minute...](https://telegra.ph/file/960b58c8f625b17613307.jpg)", link_preview=True)

    if x==30:

        await event.edit("[For that friend of yours who does not like loud music and head banging...](https://telegra.ph/file/acbce070d3c52b921b2bd.jpg)", link_preview=True)
