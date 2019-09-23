from userbot import bot
from telethon import events
from config import Config
from userbot import LOAD_PLUG
from userbot import CMD_LIST
import re
import logging

def command(**args):
    import inspect
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = previous_stack_frame.filename.replace("userbot/plugins/", "").replace(".py", "")
    if 1 == 0:
        return print("stupidity at its best")
    else:
        pattern = args.get("pattern", None)
        allow_sudo = args.get("allow_sudo", None)
        allow_edited_updates = args.get('allow_edited_updates', False)
        args["incoming"] = args.get("incoming", False)
        args["outgoing"] = True
        if bool(args["incoming"]):
            args["outgoing"] = False

        try:
            if pattern is not None and not pattern.startswith('(?i)'):
                args['pattern'] = '(?i)' + pattern
        except:
            pass

        reg = re.compile('(?:.)(.*)')
        if not pattern == None:
            try:
                cmd = re.search(reg, pattern)
                try:
                    cmd = cmd.group(1).replace("$", "")
                except:
                    pass

                CMD_LIST.update({f"{cmd}": f"{cmd}"})
            except:
                pass

        if allow_sudo:
            args["from_users"] = list(Config.SUDO_USERS)
            # Mutually exclusive with outgoing (can only set one of either).
            args["incoming"] = True
        del allow_sudo

        if "allow_edited_updates" in args:
            del args['allow_edited_updates']

        def decorator(func):
            if allow_edited_updates:
                bot.add_event_handler(func, events.MessageEdited(**args))
            bot.add_event_handler(func, events.NewMessage(**args))
            LOAD_PLUG.update({file_test: func})
            return func

        return decorator


def load_module(shortname):
    import userbot.utils
    import sys
    import importlib
    from pathlib import Path
    path = Path(f"userbot/plugins/{shortname}.py")
    name = "userbot.plugins.{}".format(shortname)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    mod.bot = bot
    mod.Config = Config
    mod.command = command
    mod.log = logging.basicConfig(level=logging.WARNING)
    # support for uniborg
    sys.modules["uniborg.util"] = userbot.utils
    mod.borg = bot
    # support for paperplaneextended
    sys.modules["userbot.events"] = userbot.utils
    spec.loader.exec_module(mod)

def remove_plugin(shortname):
    for key, value in LOAD_PLUG.items():
        if key == shortname:
            bot.remove_event_handler(value)

def admin_cmd(pattern=None, **args):
    allow_sudo = args.get("allow_sudo", False)

    # get the pattern from the decorator
    if pattern is not None:
        if pattern.startswith("\#"):
            # special fix for snip.py
            args["pattern"] = re.compile(pattern)
        else:
            args["pattern"] = re.compile("\." + pattern)

    args["outgoing"] = True
    # should this command be available for other users?
    if allow_sudo:
        args["from_users"] = list(Config.SUDO_USERS)
        # Mutually exclusive with outgoing (can only set one of either).
        args["incoming"] = True
        del args["allow_sudo"]

    # error handling condition check
    elif "incoming" in args and not args["incoming"]:
        args["outgoing"] = True

    # add blacklist chats, UB should not respond in these chats
    allow_edited_updates = False
    if "allow_edited_updates" in args and args["allow_edited_updates"]:
        allow_edited_updates = args["allow_edited_updates"]
        del args["allow_edited_updates"]

    # check if the plugin should listen for outgoing 'messages'
    is_message_enabled = True
    try:
        print(func)
    except:
        pass
    return events.NewMessage(**args)

""" Userbot module for managing events.
 One of the main components of the userbot. """

from telethon import events
import asyncio
from userbot import bot
from traceback import format_exc
from time import gmtime, strftime
import math
import subprocess
import sys
import traceback
import datetime


def register(**args):
    """ Register a new event. """
    import inspect
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = previous_stack_frame.filename.replace("userbot/plugins/", "").replace(".py", "")
    pattern = args.get('pattern', None)
    disable_edited = args.get('disable_edited', False)

    if pattern is not None and not pattern.startswith('(?i)'):
        args['pattern'] = '(?i)' + pattern

    if "disable_edited" in args:
        del args['disable_edited']

    def decorator(func):
        if not disable_edited:
            bot.add_event_handler(func, events.MessageEdited(**args))
        bot.add_event_handler(func, events.NewMessage(**args))
        LOAD_PLUG.update({file_test: func})

        return func

    return decorator


def errors_handler(func):
    async def wrapper(errors):
        try:
            await func(errors)
        except BaseException:

            date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            new = {
                'error': str(sys.exc_info()[1]),
                'date': datetime.datetime.now()
            }

            text = "**USERBOT CRASH REPORT**\n\n"

            link = "[here](https://t.me/PaperplaneExtendedSupport)"
            text += "If you wanna you can report it"
            text += f"- just forward this message {link}.\n"
            text += "Nothing is logged except the fact of error and date\n"

            ftext = "\nDisclaimer:\nThis file uploaded ONLY here,"
            ftext += "\nwe logged only fact of error and date,"
            ftext += "\nwe respect your privacy,"
            ftext += "\nyou may not report this error if you've"
            ftext += "\nany confidential data here, no one will see your data\n\n"

            ftext += "--------BEGIN USERBOT TRACEBACK LOG--------"
            ftext += "\nDate: " + date
            ftext += "\nGroup ID: " + str(errors.chat_id)
            ftext += "\nSender ID: " + str(errors.sender_id)
            ftext += "\n\nEvent Trigger:\n"
            ftext += str(errors.text)
            ftext += "\n\nTraceback info:\n"
            ftext += str(traceback.format_exc())
            ftext += "\n\nError text:\n"
            ftext += str(sys.exc_info()[1])
            ftext += "\n\n--------END USERBOT TRACEBACK LOG--------"

            command = "git log --pretty=format:\"%an: %s\" -5"

            ftext += "\n\n\nLast 5 commits:\n"

            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await process.communicate()
            result = str(stdout.decode().strip()) \
                + str(stderr.decode().strip())

            ftext += result

    return wrapper
