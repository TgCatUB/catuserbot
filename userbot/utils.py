from userbot import bot
from telethon import events
from userbot import CMD_LIST

def command(**args):
    pattern = args.get("pattern", None)
    allow_edited_updates = args.get('allow_edited_updates', False)
    args['outgoing'] = args.get('outgoing', True)

    if pattern is not None and not pattern.startswith('(?i)'):
        args['pattern'] = '(?i)' + pattern
    
    if '\.' in pattern:
        cmd = pattern.replace("\.", ".")
    else:
        cmd = pattern

    CMD_LIST.update({f"{cmd}: for CMD_LIST"})

    if "allow_edited_updates" in args:
        del args['allow_edited_updates']

    def decorator(func):
        if not allow_edited_updates:
            bot.add_event_handler(func, events.MessageEdited(**args))
        bot.add_event_handler(func, events.NewMessage(**args))

        return func

    return decorator
