import asyncio

from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import BOTLOG, BOTLOG_CHATID, catub

from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import _format, get_user_from_event, reply_id
from ..sql_helper.global_collectionjson import add_collection, get_collection

LOGS = logging.getLogger(__name__)
FBAN_GROUP_ID = Config.FBAN_GROUP_ID

plugin_category = "admin"
rose = "@MissRose_bot"

fbanresults = [
    "New FedBan",
    "FedBan Reason update",
    "has already been fbanned, with the exact same reason.",
]

unfbanresults = ["I'll give", "Un-FedBan", "un-FedBan"]


@catub.cat_cmd(
    pattern="fban(?:\s|$)([\s\S]*)",
    command=("fban", plugin_category),
    info={
        "header": "Ban the person in your database federations",
        "description": "Will fban the person in the all feds of given category which you stored in database.",
        "usage": "{tr}fban <userid/username/reply> <category> <reason>",
    },
)
async def group_fban(event):
    "fban a person."
    if FBAN_GROUP_ID == 0:
        return await edit_delete(
            event,
            "__For working of this cmd you need to set FBAN_GROUP_ID in heroku vars__",
        )
    user, reason = await get_user_from_event(event)
    if not user:
        return
    if user.id == event.client.uid:
        return await edit_delete(event, "__You can't fban yourself.__")
    if not reason:
        return await edit_delete(
            event, "__You haven't mentioned category name and reason for fban__"
        )
    reasons = reason.split(" ", 1)
    fedgroup = reasons[0]
    reason = "Not Mentioned" if len(reasons) == 1 else reasons[1]
    if get_collection("fedids") is not None:
        feds = get_collection("fedids").json
    else:
        feds = {}
    if fedgroup in feds:
        fedids = feds[fedgroup]
    else:
        return await edit_delete(
            event, f"__There is no such '{fedgroup}' named fedgroup in your database.__"
        )
    catevent = await edit_or_reply(
        event, f"Fbanning {_format.mentionuser(user.first_name ,user.id)}.."
    )
    fedchat = FBAN_GROUP_ID
    success = 0
    errors = []
    total = 0
    for i in fedids:
        total += 1
        try:
            async with event.client.conversation(fedchat) as conv:
                await conv.send_message(f"/joinfed {i}")
                reply = await conv.get_response()
                await event.client.send_read_acknowledge(
                    conv.chat_id, message=reply, clear_mentions=True
                )
                if (
                    "All new federation bans will now also remove the members from this chat."
                    not in reply.text
                ):
                    return await edit_delete(
                        catevent,
                        "__You must be owner of the group(FBAN_GROUP_ID) to perform this action__",
                        10,
                    )
                await conv.send_message(f"/fban {user.id} {reason}")
                reply = await conv.get_response()
                await event.client.send_read_acknowledge(
                    conv.chat_id, message=reply, clear_mentions=True
                )
                check = False
                for txt in fbanresults:
                    if txt in reply.text:
                        success += 1
                        check = True
                if not check:
                    errors.append(reply.text)
        except Exception as e:
            errors.append(str(e))
    success_report = f"{_format.mentionuser(user.first_name ,user.id)} is succesfully banned in {success} feds of {total}\
        \n**Reason:** __{reason}__.\n"
    if errors != []:
        success_report += "\n**Error:**"
        for txt in errors:
            success_report += f"\n☞ __{txt}__"
    await edit_or_reply(catevent, success_report)


@catub.cat_cmd(
    pattern="unfban(?:\s|$)([\s\S]*)",
    command=("unfban", plugin_category),
    info={
        "header": "UnBan the person in your database federations",
        "description": "Will unfban the person in the all feds of given category which you stored in database.",
        "usage": "{tr}unfban <userid/username/reply> <category> <reason>",
    },
)
async def group_unfban(event):
    "unfban a person."
    if FBAN_GROUP_ID == 0:
        return await edit_delete(
            event,
            "__For working of this cmd you need to set FBAN_GROUP_ID in heroku vars__",
        )
    user, reason = await get_user_from_event(event)
    if not user:
        return
    if user.id == event.client.uid:
        return await edit_delete(event, "__You can't unfban yourself.__")
    if not reason:
        return await edit_delete(
            event, "__You haven't mentioned category name and reason for unfban__"
        )
    reasons = reason.split(" ", 1)
    fedgroup = reasons[0]
    reason = "Not Mentioned" if len(reasons) == 1 else reasons[1]
    if get_collection("fedids") is not None:
        feds = get_collection("fedids").json
    else:
        feds = {}
    if fedgroup in feds:
        fedids = feds[fedgroup]
    else:
        return await edit_delete(
            event, f"__There is no such '{fedgroup}' named fedgroup in your database.__"
        )
    catevent = await edit_or_reply(
        event, f"Unfbanning {_format.mentionuser(user.first_name ,user.id)}.."
    )
    fedchat = FBAN_GROUP_ID
    success = 0
    errors = []
    total = 0
    for i in fedids:
        total += 1
        try:
            async with event.client.conversation(fedchat) as conv:
                await conv.send_message(f"/joinfed {i}")
                reply = await conv.get_response()
                await event.client.send_read_acknowledge(
                    conv.chat_id, message=reply, clear_mentions=True
                )
                if (
                    "All new federation bans will now also remove the members from this chat."
                    not in reply.text
                ):
                    return await edit_delete(
                        catevent,
                        "__You must be owner of the group(FBAN_GROUP_ID) to perform this action__",
                        10,
                    )
                await conv.send_message(f"/unfban {user.id} {reason}")
                reply = await conv.get_response()
                await event.client.send_read_acknowledge(
                    conv.chat_id, message=reply, clear_mentions=True
                )
                check = False
                for txt in unfbanresults:
                    if txt in reply.text:
                        success += 1
                        check = True
                if not check:
                    errors.append(reply.text)
        except Exception as e:
            errors.append(str(e))
    success_report = f"{_format.mentionuser(user.first_name ,user.id)} is succesfully unbanned in {success} feds of {total}\
        \n**Reason:** __{reason}__.\n"
    if errors != []:
        success_report += "\n**Error:**"
        for txt in errors:
            success_report += f"\n☞ __{txt}__"
    await edit_or_reply(catevent, success_report)


@catub.cat_cmd(
    pattern="addfedto (\w+|-all) ([-\w]+)",
    command=("addfedto", plugin_category),
    info={
        "header": "Add the federation to given category in database.",
        "description": "You can add multiple federations to one category like a group of feds under one category. And you can access all thoose feds by that name.",
        "flags": {
            "-all": "If you want to add all your feds to database then use this as {tr}addfedto -all <category name>"
        },
        "usage": [
            "{tr}addfedto <category name> <fedid>",
            "{tr}addfedto -all <category name>",
        ],
    },
)
async def quote_search(event):  # sourcery no-metrics
    "Add the federation to database."
    fedgroup = event.pattern_match.group(1)
    fedid = event.pattern_match.group(2)
    if get_collection("fedids") is not None:
        feds = get_collection("fedids").json
    else:
        feds = {}
    if fedgroup == "-all":
        catevent = await edit_or_reply(event, "`Adding all your feds to database...`")
        fedidstoadd = []
        async with event.client.conversation("@MissRose_bot") as conv:
            try:
                await conv.send_message("/myfeds")
                await asyncio.sleep(2)
                try:
                    response = await conv.get_response()
                except asyncio.exceptions.TimeoutError:
                    return await edit_or_reply(
                        catevent,
                        "__Rose bot is not responding try again later.__",
                    )
                if "can only" in response.text:
                    return await edit_delete(catevent, f"__{response.text}__")
                if "make a file" in response.text or "Looks like" in response.text:
                    await response.click(0)
                    await asyncio.sleep(2)
                    response_result = await conv.get_response()
                    await asyncio.sleep(2)
                    if response_result.media:
                        fed_file = await event.client.download_media(
                            response_result,
                            "fedlist",
                        )
                        await asyncio.sleep(5)
                        fedfile = open(fed_file, errors="ignore")
                        lines = fedfile.readlines()
                        for line in lines:
                            try:
                                fedidstoadd.append(line[:36])
                            except Exception:
                                pass
                else:
                    text_lines = response.text.split("`")
                    for fed_id in text_lines:
                        if len(fed_id) == 36 and fed_id.count("-") == 4:
                            fedidstoadd.append(fed_id)
            except YouBlockedUserError:
                await edit_delete(
                    catevent,
                    "**Error while fecthing myfeds:**\n__Unblock__ @MissRose_Bot __and try again!__",
                    10,
                )
            except Exception as e:
                await edit_delete(
                    catevent, f"**Error while fecthing myfeds:**\n__{e}__", 10
                )
            await event.client.send_read_acknowledge(conv.chat_id)
            conv.cancel()
        if not fedidstoadd:
            return await edit_or_reply(
                catevent,
                "__I have failed to fetch your feds or you are not admin of any fed.__",
            )
        feds[fedid] = fedidstoadd
        add_collection("fedids", feds)
        await edit_or_reply(
            catevent,
            f"__Successfully added all your feds to database group__ **{fedid}**.",
        )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#ADDFEDID\
                \n**Fed Group:** `{fedid}`\
                \nSuccessfully added all your feds to above database category.",
            )
        return
    if fedgroup in feds:
        fed_ids = feds[fedgroup]
        if fedid in fed_ids:
            return await edit_delete(
                event, "__This fed is already part of this fed category.__"
            )
        fed_ids.append(fedid)
        feds[fedgroup] = fed_ids
    else:
        feds[fedgroup] = [fedid]
    add_collection("fedids", feds)
    await edit_or_reply(
        event, "__The given fed is succesfully added to fed category.__"
    )
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#ADDFEDID\
            \n**Fedid:** `{fedid}`\
            \n**Fed Group:** `{fedgroup}`\
            \nThe above fedid is sucessfully added to that fed category.",
        )


@catub.cat_cmd(
    pattern="rmfedfrom (\w+|-all) ([-\w]+)",
    command=("rmfedfrom", plugin_category),
    info={
        "header": "Remove the federation from given category in database.",
        "description": "To remove given fed from the given category name",
        "flags": {
            "-all": "If you want to delete compelete category then use this flag as {tr}rmfedfrom -all <category name>"
        },
        "usage": [
            "{tr}rmfedfrom <category name> <fedid>",
            "{tr}rmfedfrom -all <category name>",
        ],
    },
)
async def quote_search(event):
    "To remove the federation from database."
    fedgroup = event.pattern_match.group(1)
    fedid = event.pattern_match.group(2)
    if get_collection("fedids") is not None:
        feds = get_collection("fedids").json
    else:
        feds = {}
    if fedgroup == "-all":
        if fedid not in feds:
            return await edit_delete(
                event, "__There is no such fedgroup in your database.__"
            )
        feds[fedid] = []
        add_collection("fedids", feds)
        await edit_or_reply(
            event, f"__Succesfully removed all feds in the category {fedid}__"
        )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#REMOVEFEDID\
            \n**Fed Group:** `{fedid}`\
            \nDeleted this Fed category in your database.",
            )
        return
    if fedgroup not in feds:
        return await edit_delete(
            event, "__There is no such fedgroup in your database.__"
        )
    fed_ids = feds[fedgroup]
    if fedid not in fed_ids:
        return await edit_delete(
            event, "__This fed is not part of given fed category.__"
        )
    fed_ids.remove(fedid)
    feds[fedgroup] = fed_ids
    add_collection("fedids", feds)
    await edit_or_reply(
        event, "__The given fed is succesfully removed from fed category.__"
    )
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#REMOVEFEDID\
        \n**Fedid:** `{fedid}`\
        \n**Fed Group:** `{fedgroup}`\
        \nThe above fedid is sucessfully removed that fed category.",
        )


@catub.cat_cmd(
    pattern="listfed(s)?(?:\s|$)([\s\S]*)",
    command=("listfed", plugin_category),
    info={
        "header": "To list all feds in your database.",
        "description": "if you give input then will show only feds in that category else will show all feds in your database",
        "usage": ["{tr}listfed", "{tr}listfed <category name>"],
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
        output = (
            f"**The list of feds in the category** `{fedgroup}` **are:**\n" + output
        )
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
                catevent, f"**Error while fecthing fedinfo:**\n__{e}__", 10
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
                catevent, f"**Error while fecthing fedinfo:**\n__{e}__", 10
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
                catevent, f"**Error while fecthing myfeds:**\n__{e}__", 10
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
                catevent, f"**Error while fecthing fedstat:**\n__{e}__", 10
            )
        await event.client.send_read_acknowledge(conv.chat_id)
        conv.cancel()
