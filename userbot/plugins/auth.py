import asyncio
import time
from telethon import events, utils, tl
from telethon.tl.types import UpdateChannel, InputUserSelf, PeerChannel
from telethon.tl.functions.channels import GetParticipantRequest
from userbot.utils import admin_cmd
# {user_id: expiration timestamp}
add_auths = {}
AUTH_TIME = 60 * 10

async def on_added(inviter_id, chat_id):
    if inviter_id == borg.uid:
        logger.info(f'Ignoring self add to {chat_id}')
        return
    if add_auths.get(inviter_id, 0) >= time.time():
        logger.info(f'Removing temporary auth for {inviter_id}')
        del add_auths[inviter_id]
        return
    logger.info(f'Leaving {chat_id} (added by {inviter_id})')
    await borg.kick_participant(chat_id, 'me')


# seems to happen on joining/leaving a channel
@borg.on(events.Raw(types=UpdateChannel))
async def on_update_chan(e):
    channel_id = utils.get_peer_id(PeerChannel(e.channel_id))
    entity = e._entities.get(channel_id)
    if isinstance(entity, tl.types.ChannelForbidden):
        return
    if isinstance(entity, tl.types.Channel) and entity.left:
        return
    channel = await borg.get_input_entity(channel_id)
    self_participant = await borg(GetParticipantRequest(channel, InputUserSelf()))
    if not isinstance(self_participant, (tl.types.ChannelParticipantSelf, tl.types.ChannelParticipantAdmin)):
        return
    inviter_id = self_participant.participant.inviter_id
    await on_added(inviter_id, channel_id)


@borg.on(events.ChatAction(func=lambda e: e.user_added or e.created))
async def on_group_added(e):
    am = e.action_message
    if borg.uid not in getattr(am.action, 'users', []):
        return
    await on_added(am.from_id, am.to_id)

@borg.on(admin_cmd(pattern=f".auth", allow_sudo=True))
@borg.on(events.NewMessage(pattern=r"\.auth", outgoing=True, func=lambda e: e.is_private))
async def on_auth(e):
    logger.info(f'Adding temporary auth for {e.chat_id}')
    add_auths[e.chat_id] = time.time() + AUTH_TIME
    await e.delete()
