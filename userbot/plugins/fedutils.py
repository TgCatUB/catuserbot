from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import catub

from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import _format, get_user_from_event, reply_id

LOGS = logging.getLogger(__name__)

plugin_category = "admin"
rose = "@MissRose_bot"


@catub.cat_cmd(
    pattern="f(ed)?info(?:\s|$)([\s\S]*)",
    command=("fedinfo", plugin_category),
    info={
        "header": "To get fedinfo from rose.",
        "description": "If no reply is given then shows you fedinfo of which you created",
        "usage": "{tr}fedinfo <fedid>",
    },
)
async def fetch_fedinfo(event):
    "To fetch fedinfo."
    input_str = (
        event.pattern_match.group(2).strip()
        if event.pattern_match.group(2) is not None
        else ""
    )
    catevent = await edit_or_reply(event, "`Fetching info about given fed...`")
    async with event.client.conversation(rose) as conv:
        try:
            await conv.send_message("/fedinfo " + input_str)
            response = await conv.get_response()
            await catevent.edit(response.text)
        except YouBlockedUserError:
            await edit_delete(
                catevent,
                "**Error while fecthing fedinfo:**\n__Unblock__ @MissRose_Bot __and try again!__",
                10,
            )
        except Exception as e:
            await edit_delete(
                catevent, f"**Error while fecthing fedinfo:**\n__{str(e)}__", 10
            )
        await event.client.send_read_acknowledge(conv.chat_id)
        conv.cancel()


@catub.cat_cmd(
    pattern="f(ed)?admins(?:\s|$)([\s\S]*)",
    command=("fadmins", plugin_category),
    info={
        "header": "To get fed admins from rose.",
        "description": "If no reply is given then shows you fedinfo of which you created",
        "usage": "{tr}fedadmins <fedid>",
    },
)
async def fetch_fedinfo(event):
    "To fetch fed admins."
    input_str = (
        event.pattern_match.group(2).strip()
        if event.pattern_match.group(2) is not None
        else ""
    )
    catevent = await edit_or_reply(event, "`Fetching admins list of given fed...`")
    async with event.client.conversation(rose) as conv:
        try:
            await conv.send_message("/fedadmins " + input_str)
            response = await conv.get_response()
            await catevent.edit(
                f"**Fedid:** ```{input_str}```\n\n" + response.text
                if input_str
                else response.text
            )
        except YouBlockedUserError:
            await edit_delete(
                catevent,
                "**Error while fecthing fedinfo:**\n__Unblock__ @MissRose_Bot __and try again!__",
                10,
            )
        except Exception as e:
            await edit_delete(
                catevent, f"**Error while fecthing fedinfo:**\n__{str(e)}__", 10
            )
        await event.client.send_read_acknowledge(conv.chat_id)
        conv.cancel()


@catub.cat_cmd(
    pattern="myfeds$",
    command=("myfeds", plugin_category),
    info={
        "header": "To get all feds where you are admin.",
        "usage": "{tr}myfeds",
    },
)
async def myfeds_fedinfo(event):
    "list all feds in which you are admin."
    catevent = await edit_or_reply(event, "`Fetching list of feds...`")
    replyid = await reply_id(event)
    async with event.client.conversation(rose) as conv:
        try:
            await conv.send_message("/myfeds")
            response = await conv.get_response()
            if "can only" in response.text:
                return await edit_delete(catevent, f"__{response.text}__")
            if "Looks like" in response.text:
                await response.click(0)
                response = await conv.get_response()
                await event.client.send_read_acknowledge(conv.chat_id)
                user = await event.client.get_me()
                await event.client.send_file(
                    event.chat_id,
                    response,
                    caption=f"List of feds in which {_format.mentionuser('I am' ,user.id)} admin are.",
                    reply_to=replyid,
                )
                await catevent.delete()
                return
            await catevent.edit(response.text)
        except YouBlockedUserError:
            await edit_delete(
                catevent,
                "**Error while fecthing myfeds:**\n__Unblock__ @MissRose_Bot __and try again!__",
                10,
            )
        except Exception as e:
            await edit_delete(
                catevent, f"**Error while fecthing myfeds:**\n__{str(e)}__", 10
            )
        await event.client.send_read_acknowledge(conv.chat_id)
        conv.cancel()


@catub.cat_cmd(
    pattern="f(ed)?stat(?:\s|$)([\s\S]*)",
    command=("fstat", plugin_category),
    info={
        "header": "To get fedstat data from rose.",
        "description": "If you haven't replied to any user or mentioned any user along with command then by default you will be input else mentioned user or replied user.",
        "usage": [
            "{tr}fstat list of all federations you are banned in.",
            "{tr}fstat <fedid> shows you info of you in the given fed."
            "{tr}fstat <userid/username/reply> list of all federations he is banned in.",
            "{tr}fstat <userid/username/reply> <fedid> shows you info of the that user in the given fed.",
        ],
    },
)
async def fstat_rose(event):
    "To get fedstat data from rose."
    catevent = await edit_or_reply(event, "`Fetching fedstat from given deatils...`")
    user, fedid = await get_user_from_event(
        event, catevent, secondgroup=True, noedits=True
    )
    if user is None:
        user = await event.client.get_me()
    if fedid is None:
        fedid = ""
    replyid = await reply_id(event)
    async with event.client.conversation(rose) as conv:
        try:
            await conv.send_message("/fedstat " + str(user.id) + " " + fedid.strip())
            response = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
            if "can only" in response.text:
                return await edit_delete(catevent, f"__{response.text}__")
            if fedid == "":
                response = await conv.get_edit()
                result = f"**List of feds** {_format.mentionuser(user.first_name ,user.id)} **has been banned in are.**\n\n"
            else:
                result = f"**Fban info about** {_format.mentionuser(user.first_name ,user.id)} **is**\n\n"
            if "Looks like" in response.message:
                await response.click(0)
                response = await conv.get_response()
                await event.client.send_read_acknowledge(conv.chat_id)
                await event.client.send_file(
                    event.chat_id,
                    response,
                    caption=f"List of feds {_format.mentionuser(user.first_name ,user.id)} has been banned in are.",
                    reply_to=replyid,
                )
                await catevent.delete()
                return
            await catevent.edit(result + response.text)
        except YouBlockedUserError:
            await edit_delete(
                catevent,
                "**Error while fecthing fedstat:**\n__Unblock__ @MissRose_Bot __and try again!__",
                10,
            )
        except Exception as e:
            await edit_delete(
                catevent, f"**Error while fecthing fedstat:**\n__{str(e)}__", 10
            )
        await event.client.send_read_acknowledge(conv.chat_id)
        conv.cancel()
