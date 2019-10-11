# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

""" Command: .dab , .brain 

credit: lejend @r4v4n4"""

import random

from telethon import events, types, functions, utils


def choser(cmd, pack, blacklist={}):
    docs = None
    @borg.on(events.NewMessage(pattern=rf'\.{cmd}', outgoing=True))
    async def handler(event):
        await event.delete()

        nonlocal docs
        if docs is None:
            docs = [
                utils.get_input_document(x)
                for x in (await borg(functions.messages.GetStickerSetRequest(types.InputStickerSetShortName(pack)))).documents
                if x.id not in blacklist
            ]

        await event.respond(file=random.choice(docs))


choser('brain', 'supermind')
choser('dab', 'DabOnHaters', {
    1653974154589768377,
    1653974154589768312,
    1653974154589767857,
    1653974154589768311,
    1653974154589767816,
    1653974154589767939,
    1653974154589767944,
    1653974154589767912,
    1653974154589767911,
    1653974154589767910,
    1653974154589767909,
    1653974154589767863,
    1653974154589767852,
    1653974154589768677
})
