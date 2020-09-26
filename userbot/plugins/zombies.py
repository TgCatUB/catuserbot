# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Cmd= `.zombie`
Usage: Searches for deleted accounts in a groups and channels.
Use .zombies clean to remove deleted accounts from the groups and channels.
\nPorted by ©[NIKITA](t.me/kirito6969) and ©[EYEPATCH](t.me/NeoMatrix90)"""

from asyncio import sleep

from telethon.errors import ChatAdminRequiredError, UserAdminInvalidError

from .. import CMD_HELP
from ..utils import admin_cmd, edit_or_reply, sudo_cmd

if Config.PRIVATE_GROUP_BOT_API_ID is None:
    BOTLOG = False
else:
    BOTLOG = True
    BOTLOG_CHATID = Config.PRIVATE_GROUP_BOT_API_ID


@borg.on(admin_cmd(pattern=f"zombies ?(.*)"))
@borg.on(sudo_cmd(pattern="zombies ?(.*)", allow_sudo=True))
async def rm_deletedacc(show):
    con = show.pattern_match.group(1).lower()
    del_u = 0
    del_status = "`No deleted accounts found, Group is clean`"
    if con != "clean":
        event = await edit_or_reply(
            show, "`Searching for ghost/deleted/zombie accounts...`"
        )
        async for user in bot.iter_participants(show.chat_id):
            if user.deleted:
                del_u += 1
                await sleep(0.5)
        if del_u > 0:
            del_status = f"`Found` **{del_u}** ghost/deleted/zombie account(s) in this group,\
            \nclean them by using `.zombies clean`"
        await event.edit(del_status)
        return
    # Here laying the sanity check
    chat = await show.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    # Well
    if not admin and not creator:
        await edit_or_reply(show, "`I am not an admin here!`")
        return
    event = await edit_or_reply(
        show, "`Deleting deleted accounts...\nOh I can do that?!?!`"
    )
    del_u = 0
    del_a = 0
    async for user in show.client.iter_participants(show.chat_id):
        if user.deleted:
            try:
                await show.client.kick_participant(show.chat_id, user.id)
                await sleep(0.5)
            except ChatAdminRequiredError:
                await event.edit("`I don't have ban rights in this group`")
                return
            except UserAdminInvalidError:
                del_u -= 1
                del_a += 1
    if del_u > 0:
        del_status = f"Cleaned **{del_u}** deleted account(s)"
    if del_a > 0:
        del_status = f"Cleaned **{del_u}** deleted account(s) \
        \n**{del_a}** deleted admin accounts are not removed"
    await event.edit(del_status)
    await sleep(5)
    await show.delete()
    if BOTLOG:
        await show.client.send_message(
            BOTLOG_CHATID,
            "#CLEANUP\n"
            f"Cleaned **{del_u}** deleted account(s) !!\
            \nCHAT: {show.chat.title}(`{show.chat_id}`)",
        )


CMD_HELP.update(
    {
        "zombies": "**Plugin :** `zombies`\
        \n\n**Syntax : **`.zombies`\
        \n**Usage :** Searches for deleted accounts in a group. Use `.zombies clean` to remove deleted accounts from the group.\
        "
    }
)
