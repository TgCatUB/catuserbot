from telethon.errors import BadRequestError
from telethon.tl import functions
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChatAdminRights
from telethon.tl.types import ChatBannedRights
from telethon.errors import FloodWaitError
from .. import catub
from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply

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
    if type_of_group == "g":
        try:
            result = await event.client(
                functions.messages.CreateChatRequest(
                    users=[Config.TG_BOT_USERNAME],
                    # Not enough users (to create a chat, for example)
                    # Telegram, no longer allows creating a chat with ourselves
                    title=group_name,
                )
            )
            created_chat_id = result.chats[0].id
            result = await event.client(
                functions.messages.ExportChatInviteRequest(
                    peer=created_chat_id,
                )
            )
            await edit_or_reply(
                event, f"Group `{group_name}` created successfully. Join {result.link}"
            )
        except Exception as e:
            await edit_delete(event, f"**Error:**\n{str(e)}")
    elif type_of_group == "c":
        try:
            r = await event.client(
                functions.channels.CreateChannelRequest(
                    title=group_name,
                    about=descript,
                    megagroup=False,
                )
            )

            created_chat_id = r.chats[0].id
            result = await event.client(
                functions.messages.ExportChatInviteRequest(
                    peer=created_chat_id,
                )
            )
            await edit_or_reply(
                event,
                f"Channel `{group_name}` created successfully. Join {result.link}",
            )
        except Exception as e:
            await edit_delete(event, f"**Error:**\n{str(e)}")
    elif type_of_group == "b":
        answer = await create_supergroup(
            group_name, event.client, Config.TG_BOT_USERNAME, descript
        )
        if answer[0] != "error":
            await edit_or_reply(
                event,
                f"Mega group `{group_name}` created successfully. Join {answer[0].link}",
            )
            print(answer[1])
        else:
            await edit_delete(event, f"**Error:**\n{str(answer[1])}")
    else:
        await edit_delete(event, "Read `.help create` to know how to use me")


async def create_supergroup(group_name, client, botusername, descript):
    try:
        result = await client(
                functions.messages.CreateChatRequest(
                    users=[Config.TG_BOT_USERNAME],
                    # Not enough users (to create a chat, for example)
                    # Telegram, no longer allows creating a chat with ourselves
                    title=group_name,
                )
            )
        created_chat_id = result.chats[0].id
        result = await client(
                functions.messages.ExportChatInviteRequest(
                    peer=created_chat_id,
                )
            )
        await client(
            functions.channels.InviteToChannelRequest(
                channel=created_chat_id,
                users=[botusername],
            )
        )
    except Exception as e:
        return "error", str(e)
    lock_rights = ChatBannedRights(
            until_date=None,
            send_messages=False,
            send_media=False,
            send_stickers=False,
            send_gifs=False,
            send_games=False,
            send_inline=False,
            embed_links=False,
            send_polls=False,
            invite_users=False,
            pin_messages=True,
            change_info=False,
        )
    flag = True
    while flag:
        try:
            await event.client(
                    EditChatDefaultBannedRightsRequest(
                        peer=created_chat_id, banned_rights=lock_rights
                    )
                )
            flag = False
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds)
        except Exception as e:
            return "error", str(e)
    created_chat_id = (await event.client.get_entity(result.link)).id
    return result, created_chat_id
