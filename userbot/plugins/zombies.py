# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Cmd= `.zombie`
Usage: Searches for deleted accounts in a groups and channels.
Use .zombies clean to remove deleted accounts from the groups and channels.
\nPorted by ©[NIKITA](t.me/kirito6969) and ©[EYEPATCH](t.me/NeoMatrix90)"""

from telethon import events
from userbot.utils import admin_cmd,sudo_cmd
from asyncio import sleep
from os import remove
import asyncio
from telethon.errors import (BadRequestError, ChatAdminRequiredError,
                             UserAdminInvalidError)
from telethon.errors.rpcerrorlist import (UserIdInvalidError,
                                          MessageTooLongError)
from telethon.tl.functions.channels import (EditAdminRequest,
                                            EditBannedRequest,
                                            EditPhotoRequest)
from telethon.tl.types import (ChannelParticipantsAdmins, ChatAdminRights,
                               ChatBannedRights, MessageEntityMentionName,
                               MessageMediaPhoto)
from userbot import CMD_HELP, bot 

BOTLOG = True
BOTLOG_CHATID = Config.PRIVATE_GROUP_BOT_API_ID

# =================== CONSTANT ===================

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)


UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

        
@borg.on(admin_cmd(pattern=f"zombies ?(.*)"))
async def rm_deletedacc(show):
    """ For .zombies command, list all the ghost/deleted/zombie accounts in a chat. """

    con = show.pattern_match.group(1).lower()
    del_u = 0
    del_status = "`No deleted accounts found, Group is clean`"

    if con != "clean":
        await show.edit("`Searching for ghost/deleted/zombie accounts...`")
        async for user in show.client.iter_participants(show.chat_id):

            if user.deleted:
                del_u += 1
                await sleep(1)
        if del_u > 0:
            del_status = f"`Found` **{del_u}** ghost/deleted/zombie account(s) in this group,\
            \nclean them by using `.zombies clean`"
        await show.edit(del_status)
        return

    # Here laying the sanity check
    chat = await show.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Well
    if not admin and not creator:
        await show.edit("`I am not an admin here!`")
        return

    await show.edit("`Deleting deleted accounts...\nOh I can do that?!?!`")
    del_u = 0
    del_a = 0

    async for user in show.client.iter_participants(show.chat_id):
        if user.deleted:
            try:
                await show.client(
                    EditBannedRequest(show.chat_id, user.id, BANNED_RIGHTS))
            except ChatAdminRequiredError:
                await show.edit("`I don't have ban rights in this group`")
                return
            except UserAdminInvalidError:
                del_u -= 1
                del_a += 1
            await show.client(
                EditBannedRequest(show.chat_id, user.id, UNBAN_RIGHTS))
            del_u += 1


    if del_u > 0:
        del_status = f"Cleaned **{del_u}** deleted account(s)"

    if del_a > 0:
        del_status = f"Cleaned **{del_u}** deleted account(s) \
        \n**{del_a}** deleted admin accounts are not removed"


    await show.edit(del_status)
    await sleep(2)
    await show.delete()
    
    if BOTLOG:
        await show.client.send_message(
            BOTLOG_CHATID, "#CLEANUP\n"
            f"Cleaned **{del_u}** deleted account(s) !!\
            \nCHAT: {show.chat.title}(`{show.chat_id}`)")

        
               
@borg.on(sudo_cmd(pattern="zombies ?(.*)", allow_sudo=True))  
async def rm_deletedacc(show):
    if show.fwd_from:
        return
    con = show.pattern_match.group(1)
    """ For .zombies command, list all the ghost/deleted/zombie accounts in a chat. """

    del_u = 0
    del_status = "`No deleted accounts found, Group is clean`"

    if con != "clean":
        cat = await show.reply("`Searching for ghost/deleted/zombie accounts...`")
        await asyncio.sleep(2)
        await cat.delete()
        async for user in show.client.iter_participants(show.chat_id):

            if user.deleted:
                del_u += 1
                await sleep(1)
        if del_u > 0:
            del_status = f"`Found` **{del_u}** ghost/deleted/zombie account(s) in this group,\
            \nclean them by using `.zombies clean`"
        await show.reply(del_status)
        return

    # Here laying the sanity check
    chat = await show.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Well
    if not admin and not creator:
        await show.reply("`I am not an admin here!`")
        return

    cat2 = await show.reply("`Deleting deleted accounts...\nOh I can do that?!?!`")
    await asyncio.sleep(2)
    await cat2.delete()
    del_u = 0
    del_a = 0

    async for user in show.client.iter_participants(show.chat_id):
        if user.deleted:
            try:
                await show.client(
                    EditBannedRequest(show.chat_id, user.id, BANNED_RIGHTS))
            except ChatAdminRequiredError:
                await show.reply("`I don't have ban rights in this group`")
                return
            except UserAdminInvalidError:
                del_u -= 1
                del_a += 1
            await show.client(
                EditBannedRequest(show.chat_id, user.id, UNBAN_RIGHTS))
            del_u += 1


    if del_u > 0:
        del_status = f"Cleaned **{del_u}** deleted account(s)"

    if del_a > 0:
        del_status = f"Cleaned **{del_u}** deleted account(s) \
        \n**{del_a}** deleted admin accounts are not removed"


    cat3 = await show.reply(del_status)
    await sleep(2)
    await cat3.delete()

CMD_HELP.update({
    "zombies":
    ".zombies\
\nUsage: Searches for deleted accounts in a group. Use .delusers clean to remove deleted accounts from the group.\
"
})

