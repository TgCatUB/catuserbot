# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""Urban Dictionary
Syntax: .ud Query"""
import asyncurban
from PyDictionary import PyDictionary

from .. import CMD_HELP
from ..utils import admin_cmd, edit_or_reply, sudo_cmd


@borg.on(admin_cmd(pattern="ud (.*)"))
@borg.on(sudo_cmd(pattern="ud (.*)", allow_sudo=True))
async def _(event):
    word = event.pattern_match.group(1)
    urban = asyncurban.UrbanDictionary()
    try:
        mean = await urban.get_word(word)
        await edit_or_reply(
            event,
            "Text: **{}**\n\nMeaning: **{}**\n\nExample: __{}__".format(
                mean.word, mean.definition, mean.example
            ),
        )
    except asyncurban.WordNotFoundError:
        await edit_or_reply(event, "No result found for **" + word + "**")


@borg.on(admin_cmd(pattern="meaning (.*)"))
@borg.on(sudo_cmd(pattern="meaning (.*)", allow_sudo=True))
async def _(event):
    word = event.pattern_match.group(1)
    dictionary = PyDictionary()
    cat = dictionary.meaning(word)
    output = f"**Word :** __{word}__\n\n"
    try:
        for a, b in cat.items():
            output += f"**{a}**\n"
            for i in b:
                output += f"☞__{i}__\n"
        await edit_or_reply(event, output)
    except Exception:
        await edit_or_reply(event, f"Couldn't fetch meaning of {word}")


CMD_HELP.update(
    {
        "dictionary": "**Plugin :** `dictionary`\
    \n\n**Syntax :** `.ud query`\
    \n**Usage : **fetches meaning from Urban dictionary\
    \n\n**Syntax : **`.meaning query`\
    \n**Usage : **Fetches meaning of the given word\
    "
    }
)
