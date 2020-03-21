"""
Contains code used by other kbass_* plugins
"""
from userbot import utils


async def get_target_message(borg, event):
    """
    If the event is a reply, returns the reply message if it's from us
    If event is not a reply, then it tries to return the most recent message
    from us
    """
    target = await event.get_reply_message()
    if event.is_reply and target.from_id == borg.uid:
        return target
    if not target:
        return await util.get_recent_self_message(borg, event)


def self_reply_cmd(borg, pattern):
    def wrapper(function):
        @borg.on(util.admin_cmd(pattern))
        async def wrapped(event, *args, **kwargs):
            await event.delete()
            target = await get_target_message(borg, event)
            if not target:
                return
            return await function(event, target, *args, **kwargs)
        return wrapped
    return wrapper


def self_reply_selector(borg, cmd):
    def wrapper(function):
        @borg.on(util.admin_cmd(cmd + r"( [+-]?\d+)?$"))
        async def wrapped(event, *args, **kwargs):
            await event.delete()
            reply = await event.get_reply_message()
            if not reply:
                return
            num_offset = int(event.pattern_match.group(1) or 0)
            reverse = num_offset > 0

            targets = [reply] if reverse else []
            targets.extend(await borg.get_messages(
                await event.get_input_chat(),
                limit=abs(num_offset),
                offset_id=reply.id,
                reverse=reverse
            ))
            if not reverse:
                # reverse the list because we want things to always be in
                # history order
                targets.reverse()
                targets.append(reply)

            return await function(event, targets, num_offset, *args, **kwargs)
        return wrapped
    return wrapper
