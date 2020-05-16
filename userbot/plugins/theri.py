"""Emoji

Available Commands:

.pyavam"""

from telethon import events

import asyncio





@borg.on(events.NewMessage(pattern=r"\.(.*)", outgoing=True))

async def _(event):

    if event.fwd_from:

        return

    animation_interval = 3

    animation_ttl = range(0, 20)

    input_str = event.pattern_match.group(1)

    if input_str == "pyavam":

        await event.edit(input_str)

        animation_chars = [
        
            "**Finding User Info..**",
            "**Finding User Info....**",
            "**(1) തന്ത ഇല്ല തായൊളി**",
            "**(1) വെപ്പാണ്ടി തായൊളി*",
            "**(2) Finding this user main തായൊളി തരങ്ങൾ...**",
            "**(2) Finding this user main തന്ത ഇല്ല തരങ്ങൾ...*",
            "**(3) Fatherless: ☑️**",
            "**(3) Fatherless: ✅**",    
            "**(4) Son of street DOG: ☑️**",
            "**(4) Son of street DOG: ✅**",
            "**(5) വെപ്പാണ്ടി ഉപയോഗിക്കുന്നു: ☑️**",
            "**(5) വെപ്പാണ്ടി ഉപയോഗിക്കുന്നു: ✅**",
            "**(6) Eats Any ones shit: ☑️**",
            "**(6) Eats Any ones shit: ✅**",
            "**(7) Mother Fucker: ☑️**",
            "**(7) Mother Fucker: ✅**",
            "**(8) Checking with DNA: ☑️**",
            "**(8) DNA Matching: ✅**",
            "**ചുരുക്കി പറഞ്ഞ നിന്റെ 8 തന്തകളിൽ ഒരാൾ എന്റെ Master  ആണ്*",
            "**ശരിയായ തന്തയെ കണ്ടു പിടിച്ചതിൽ നീ സന്തോഷവാൻ ആണോ Options : YES & NO Otherwise നീ ഒരു തന്ത ഇല്ല കഴുവേറി ആണ്**"

 ]

        for i in animation_ttl:

            await asyncio.sleep(animation_interval)

            await event.edit(animation_chars[i % 20])
