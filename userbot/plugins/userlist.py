"""Get Administrators of any Chat*
Syntax: .userlist"""
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins, ChannelParticipantAdmin, ChannelParticipantCreator
from uniborg.util import admin_cmd
from telethon.errors.rpcerrorlist import (UserIdInvalidError,
                                          MessageTooLongError)
                                          
@borg.on(events.NewMessage(pattern=r"\.userlist ?(.*)", outgoing=True))
async def get_users(show):
    """ For .userslist command, list all of the users of the chat. """
    if not show.text[0].isalpha() and show.text[0] not in ("/", "#", "@", "!"):
        if not show.is_group:
            await show.edit("Are you sure this is a group?")
            return
        info = await show.client.get_entity(show.chat_id)
        title = info.title if info.title else "this chat"
        mentions = 'Users in {}: \n'.format(title)
        try:
            if not show.pattern_match.group(1):
                async for user in show.client.iter_participants(show.chat_id):
                    if not user.deleted:
                        mentions += f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    else:
                        mentions += f"\nDeleted Account `{user.id}`"
            else:
                searchq = show.pattern_match.group(1)
                async for user in show.client.iter_participants(show.chat_id, search=f'{searchq}'):
                    if not user.deleted:
                        mentions += f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    else:
                        mentions += f"\nDeleted Account `{user.id}`"
        except ChatAdminRequiredError as err:
            mentions += " " + str(err) + "\n"
        try:
            await show.edit(mentions)
        except MessageTooLongError:
            await show.edit("Damn, this is a huge group. Uploading users lists as file.")
            file = open("userslist.txt", "w+")
            file.write(mentions)
            file.close()
            await show.client.send_file(
                show.chat_id,
                "userslist.txt",
                caption='Users in {}'.format(title),
                reply_to=show.id,
            )
            remove("userslist.txt")
