from telethon.tl import functions

from . import catub, edit_or_reply

plugin_category = "tools"


@catub.cat_cmd(
    pattern="create (b|g|c) (.*)",
    command=("create", plugin_category),
    info={
        "header": "To create a private group/channel with userbot.",
        "description": "Use this cmd to create super group , normal group or channel.",
        "flags": {
            "b": "to create a private super group",
            "g": "To create a private basic group.",
            "c": "to create a private channel",
        },
        "usage": "{tr}create (b|g|c) <name of group/channel>",
        "examples": "{tr}create b catuserbot",
    },
)
async def _(event):
    "To create a private group/channel with userbot"
    type_of_group = event.pattern_match.group(1)
    group_name = event.pattern_match.group(2)
    if type_of_group == "c":
        descript = "This is a Test Channel created using catuserbot"
    else:
        descript = "This is a Test Group created using catuserbot"
    event = await edit_or_reply(event, "creating......")
    if type_of_group == "b":
        try:
            result = await event.client(
                functions.messages.CreateChatRequest(
                    users=["@sarah_robot"],
                    title=group_name,
                )
            )
            created_chat_id = result.chats[0].id
            await event.client(
                functions.messages.DeleteChatUserRequest(
                    chat_id=created_chat_id, user_id="@sarah_robot"
                )
            )
            result = await event.client(
                functions.messages.ExportChatInviteRequest(
                    peer=created_chat_id,
                )
            )
            await event.edit(
                "Group `{}` created successfully. Join {}".format(
                    group_name, result.link
                )
            )
        except Exception as e:
            await event.edit(str(e))
    elif type_of_group in ["g", "c"]:
        try:
            r = await event.client(
                functions.channels.CreateChannelRequest(
                    title=group_name,
                    about=descript,
                    megagroup=type_of_group != "c",
                )
            )

            created_chat_id = r.chats[0].id
            result = await event.client(
                functions.messages.ExportChatInviteRequest(
                    peer=created_chat_id,
                )
            )
            await event.edit(
                "Channel `{}` created successfully. Join {}".format(
                    group_name, result.link
                )
            )
        except Exception as e:
            await event.edit(str(e))
    else:
        await event.edit("Read `.help create` to know how to use me")
