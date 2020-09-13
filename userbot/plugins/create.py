"""Create Private Groups
Available Commands:
.create (b|g) GroupName"""
from telethon.tl import functions

from .. import CMD_HELP
from ..utils import admin_cmd, edit_or_reply, sudo_cmd


@borg.on(admin_cmd(pattern="create (b|g|c) (.*)"))  # pylint:disable=E0602
@borg.on(sudo_cmd(pattern="create (b|g|c) (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    type_of_group = event.pattern_match.group(1)
    group_name = event.pattern_match.group(2)
    event = await edit_or_reply(event, "creating......")
    if type_of_group == "b":
        try:
            result = await borg(
                functions.messages.CreateChatRequest(  # pylint:disable=E0602
                    users=["@sarah_robot"],
                    # Not enough users (to create a chat, for example)
                    # Telegram, no longer allows creating a chat with ourselves
                    title=group_name,
                )
            )
            created_chat_id = result.chats[0].id
            await borg(
                functions.messages.DeleteChatUserRequest(
                    chat_id=created_chat_id, user_id="@sarah_robot"
                )
            )
            result = await borg(
                functions.messages.ExportChatInviteRequest(
                    peer=created_chat_id,
                )
            )
            await event.edit(
                "Group `{}` created successfully. Join {}".format(
                    group_name, result.link
                )
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await event.edit(str(e))
    elif type_of_group == "g" or type_of_group == "c":
        try:
            r = await borg(
                functions.channels.CreateChannelRequest(  # pylint:disable=E0602
                    title=group_name,
                    about="This is a Test from @mrconfused",
                    megagroup=False if type_of_group == "c" else True,
                )
            )
            created_chat_id = r.chats[0].id
            result = await borg(
                functions.messages.ExportChatInviteRequest(
                    peer=created_chat_id,
                )
            )
            await event.edit(
                "Channel `{}` created successfully. Join {}".format(
                    group_name, result.link
                )
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await event.edit(str(e))
    else:
        await event.edit("Read `.info create` to know how to use me")


CMD_HELP.update(
    {
        "create": "__**PLUGIN NAME :** Create__\
    \n\n📌** CMD ➥** `.create b`\
    \n**USAGE   ➥  **Creates a super group and send you link\
    \n\n📌** CMD ➥** `.create g`\
    \n**USAGE   ➥  **Creates a private group and sends you link\
    \n\n📌** CMD ➥** `.create c`\
    \n**USAGE   ➥  **Creates a Channel and sends you link\
    \n\n**Here the bot accout is owner**\
    "
    }
)
