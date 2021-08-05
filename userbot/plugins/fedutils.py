from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import catub

from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import _format, get_user_from_event, reply_id
from ..sql_helper.global_collectionjson import add_collection, get_collection

LOGS = logging.getLogger(__name__)

plugin_category = "admin"
rose = "@MissRose_bot"


@catub.cat_cmd(
    pattern="addfedto (\w+) ([-\w]+)",
    command=("addfedto", plugin_category),
    info={
        "header": "Add the federation to given group in database.",
        "description": "You can add multiple federations to one name like a group of feds under one name. And you can access all thoose feds by that name.",
        "usage": "{tr}addfedto <group name> <fedid>",
    },
)
async def quote_search(event):
    "Add the federation to database."
    fedgroup = event.pattern_match.group(1)
    fedid = event.pattern_match.group(2)
    if get_collection("fedids") is not None:
        feds = get_collection("fedids").json
    else:
        feds = {}
    if fedgroup in feds:
        fed_ids = feds[fedgroup]
        if fedid in fed_ids:
            return await edit_delete(
                event, "__This fed is already part of this fed group.__"
            )
        fed_ids.append(fedid)
        feds[fedgroup] = fed_ids
    else:
        feds[fedgroup] = [fedid]
    add_collection("fedids", feds)
    await edit_or_reply(event, "__The given fed is succesfully added to fed group.__")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#ADDFEDID\
        \n**Fedid:** `{fedid}`\
        \n**Fed Group:** `{fedgroup}`\
        \nThe above fedid is sucessfully added to that fed group.",
        )


@catub.cat_cmd(
    pattern="rmfedfrom (\w+) ([-\w]+)",
    command=("rmfedfrom", plugin_category),
    info={
        "header": "Remove the federation from given group in database.",
        "description": "To remove given fed from the given group name",
        "usage": "{tr}rmfedfrom <group name> <fedid>",
    },
)
async def quote_search(event):
    "To remove the federation to database."
    fedgroup = event.pattern_match.group(1)
    fedid = event.pattern_match.group(2)
    if get_collection("fedids") is not None:
        feds = get_collection("fedids").json
    else:
        feds = {}
    if fedgroup not in feds:
        return await edit_delete(
            event, "__There is no such fedgroup in your database.__"
        )
    fed_ids = feds[fedgroup]
    if fedid not in fed_ids:
        return await edit_delete(event, "__This fed is not part of given fed group.__")
    fed_ids.remove(fedid)
    feds[fedgroup] = fed_ids
    add_collection("fedids", feds)
    await edit_or_reply(
        event, "__The given fed is succesfully removed from fed group.__"
    )
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#REMOVEFEDID\
        \n**Fedid:** `{fedid}`\
        \n**Fed Group:** `{fedgroup}`\
        \nThe above fedid is sucessfully removed that fed group.",
        )


@catub.cat_cmd(
    pattern="listfed(s)?(?:\s|$)([\s\S]*)",
    command=("listfed", plugin_category),
    info={
        "header": "To list all feds in your database.",
        "description": "if you give input then will show only feds in that group else will show all feds in your database",
        "usage": ["{tr}listfed", "{tr}listfed <group name>"],
    },
)
async def quote_search(event):
    "To list federations in database."
    fedgroup = event.pattern_match.group(2)
    if get_collection("fedids") is not None:
        feds = get_collection("fedids").json
    else:
        feds = {}
    output = ""
    if not fedgroup:
        for fedgrp in feds:
            fedids = feds[fedgrp]
            if fedids != []:
                output += f"\n• **{fedgrp}:**\n"
                for fid in fedids:
                    output += f"☞ `{fid}`\n"
    elif fedgroup in feds:
        fedids = feds[fedgroup]
        if fedids != []:
            output += f"\n• **{fedgroup}:**\n"
            for fid in fedids:
                output += f"☞ `{fid}`\n"
    else:
        return await edit_delete(
            event, "__There is no such fedgroup in your database.__"
        )
    if output != "" and fedgroup:
        output = f"**The list of feds in the group** `{fedgroup}` **are:**\n" + output
    elif output != "":
        output = "**The list of all feds in your database are :**\n" + output
    else:
        output = (
            "__There are no feds in your database try by adding them using addfedto__"
        )
    await edit_or_reply(event, output)


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
