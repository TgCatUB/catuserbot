from userbot import catub
from userbot.core.events import NewMessage

from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers.utils import _format
from ..sql_helper import global_collection as sql
from . import _format, get_user_from_event
import sys
import os

plugin_category = "tools"

__keyword__ = "sudousers"
plugin_category = "tools"
SUDO_STRING1 = "This user is already in your sudo Users list"
SUDO_STRING2 = (
    "This user is already in your sudo users list and his userdata has been updated now"
)
SUDO_STRING3 = "is successfully added to your sudo users list."
SUDO_STRING4 = "is successfully removed from your sudo users list."
SUDO_STRING5 = "is not in your sudo users list."
SUDO_STRING6 = "There are no sudo users for your bot"


async def _init() -> None:
    sudousers = sql.get_item_collectionlist(__keyword__)
    Config.SUDO_USERS.clear()
    for user_d in sudousers:
        Config.SUDO_USERS.add(user_d[0])


@catub.cat_cmd(
    pattern="addsudo(:? |$)(.*)",
    command=("addsudo", plugin_category),
    info={
        "header": "To add user as your sudo.",
        "usage": "{tr}addsudo <username/reply/mention>",
    },
)
async def _(event):
    "To add user to sudo."
    replied_user, error_i_a = await get_user_from_event(event)
    if replied_user is None:
        return
    userdata = [
        replied_user.id,
        replied_user.first_name,
        replied_user.username,
    ]
    if sql.is_in_collectionlist(__keyword__, userdata):
        return await edit_or_reply(event, SUDO_STRING1, parse_mode=_format.parse_pre)
    sudousers = sql.get_item_collectionlist(__keyword__)
    for user_d in sudousers:
        if str(user_d[0]) == str(replied_user.id):
            sql.rm_from_collectionlist(__keyword__, user_d)
            sql.add_to_collectionlist(__keyword__, userdata)
            return await edit_or_reply(
                event, SUDO_STRING2, parse_mode=_format.parse_pre
            )
    sql.add_to_collectionlist(__keyword__, userdata)
    Config.SUDO_USERS.add(replied_user.id)
    args = [sys.executable, "-m", "userbot"]
    os.execle(sys.executable, *args, os.environ)
    return await edit_or_reply(
        event,
        f"[{replied_user.first_name}](tg://user?id={replied_user.id}) " + SUDO_STRING3,
    )


@catub.cat_cmd(
    pattern="delsudo(:? |$)(.*)",
    command=("delsudo", plugin_category),
    info={
        "header": "To remove user from your sudo.",
        "usage": "{tr}delsudo <username/reply/mention>",
    },
)
async def _(event):
    "To del user from sudo."
    replied_user, error_i_a = await get_user_from_event(event)
    if replied_user is None:
        return
    sudousers = sql.get_item_collectionlist(__keyword__)
    for user_d in sudousers:
        if str(user_d[0]) == str(replied_user.id):
            sql.rm_from_collectionlist(__keyword__, user_d)
            Config.SUDO_USERS.remove(user_d[0])
            return await edit_or_reply(
                event,
                f"[{replied_user.first_name}](tg://user?id={replied_user.id}) "
                + SUDO_STRING4,
            )
    await edit_or_reply(
        event,
        f"[{replied_user.first_name}](tg://user?id={replied_user.id}) " + SUDO_STRING5,
    )


@catub.cat_cmd(
    pattern="sudousers$",
    command=("sudousers", plugin_category),
    info={
        "header": "To list users for whom you are sudo.",
        "usage": "{tr}sudousers",
    },
)
async def _(event):
    "To list Your sudo users"
    sudocount = sql.num_collectionlist_item(__keyword__)
    if sudocount == 0:
        return await edit_or_reply(event, SUDO_STRING6, parse_mode=_format.parse_pre)
    sudousers = sql.get_item_collectionlist(__keyword__)
    output = "**SUDO USERS**\n\n"
    for user_d in sudousers:
        if user_d[2] is not None:
            output += f"[{user_d[1]}](https://t.me/{user_d[2]})\n"
        else:
            output += f"[{user_d[1]}](tg://user?id={user_d[0]})\n"
    await edit_or_reply(event, output)


catub.loop.create_task(_init())
