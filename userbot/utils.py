from userbot import bot
from telethon import events
from userbot import CMD_LIST
import re

def command(**args):
    pattern = args.get("pattern", None)
    allow_sudo = args.get("allow_sudo", None)
    allow_edited_updates = args.get('allow_edited_updates', False)
    args['outgoing'] = args.get('outgoing', True)

    if pattern is not None and not pattern.startswith('(?i)'):
        args['pattern'] = '(?i)' + pattern
    
    reg = re.compile('(?:.)(.*)')
    if not pattern == None:
        cmd = re.search(reg, pattern)
        try:
            cmd = cmd.group(1).replace("$", "")
        except:
            pass

        CMD_LIST.update({f"{cmd}": f"{cmd}"})

    if "allow_edited_updates" in args:
        del args['allow_edited_updates']
    try:
        del args['allow_sudo'] # for now
    except:
        pass

    def decorator(func):
        if not allow_edited_updates:
            bot.add_event_handler(func, events.MessageEdited(**args))
        bot.add_event_handler(func, events.NewMessage(**args))

        return func

    return decorator
