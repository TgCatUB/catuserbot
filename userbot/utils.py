from userbot import bot
from telethon import events
from var import Var
from pathlib import Path
from userbot.uniborgConfig import Config
from userbot import LOAD_PLUG, CMD_LIST
import re
import logging
import inspect
import math
import os
import time
import asyncio
from traceback import format_exc
from time import gmtime, strftime
import subprocess
import sys
import traceback
import datetime
from telethon.tl.functions.messages import GetPeerDialogsRequest
from typing import List

# the secret configuration specific things
ENV = bool(os.environ.get("ENV", False))
if ENV:
    from userbot.uniborgConfig import Config
else:
    if os.path.exists("config.py"):
        from config import Development as Config
        
def command(**args):
    args["func"] = lambda e: e.via_bot_id is None

    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
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

        reg = re.compile('(.*)')
        if not pattern == None:
            try:
                cmd = re.search(reg, pattern)
                try:
                    cmd = cmd.group(1).replace("$", "").replace("\\", "").replace("^", "")
                except:
                    pass

                try:
                    CMD_LIST[file_test].append(cmd)
                except:
                    CMD_LIST.update({file_test: [cmd]})
            except:
                pass

        if allow_sudo:
            args["from_users"] = list(Config.SUDO_USERS)
            args["incoming"] = True
            del args["allow_sudo"]
        
        # error handling condition check
        elif "incoming" in args and not args["incoming"]:
            args["outgoing"] = True

        # add blacklist chats, UB should not respond in these chats
        args["blacklist_chats"] = True
        black_list_chats = list(Config.UB_BLACK_LIST_CHAT)
        if len(black_list_chats) > 0:
            args["chats"] = black_list_chats

        if "allow_edited_updates" in args:
            del args['allow_edited_updates']

        def decorator(func):
            if allow_edited_updates:
                bot.add_event_handler(func, events.MessageEdited(**args))
            bot.add_event_handler(func, events.NewMessage(**args))
            try:
                LOAD_PLUG[file_test].append(func)
            except:
                LOAD_PLUG.update({file_test: [func]})
            return func

        return decorator


def load_module(shortname):
    if shortname.startswith("__"):
        pass
    elif shortname.endswith("_"):
        import userbot.utils
        import sys
        import importlib
        from pathlib import Path
        path = Path(f"userbot/plugins/{shortname}.py")
        name = "userbot.plugins.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        print("Successfully (re)imported "+shortname)
    else:
        import userbot.utils
        import sys
        import importlib
        from pathlib import Path
        path = Path(f"userbot/plugins/{shortname}.py")
        name = "userbot.plugins.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.bot = bot
        mod.tgbot = bot.tgbot
        mod.Var = Var
        mod.command = command
        mod.logger = logging.getLogger(shortname)
        # support for uniborg
        sys.modules["uniborg.util"] = userbot.utils
        mod.Config = Config
        mod.borg = bot
        # support for paperplaneextended
        sys.modules["userbot.events"] = userbot.utils
        spec.loader.exec_module(mod)
        # for imports
        sys.modules["userbot.plugins."+shortname] = mod
        print("Successfully (re)imported "+shortname)

def remove_plugin(shortname):
    try:
        try:
            for i in LOAD_PLUG[shortname]:
                bot.remove_event_handler(i)
            del LOAD_PLUG[shortname]

        except:
            name = f"userbot.plugins.{shortname}"

            for i in reversed(range(len(bot._event_builders))):
                ev, cb = bot._event_builders[i]
                if cb.__module__ == name:
                    del bot._event_builders[i]
    except:
        raise ValueError
        

def admin_cmd(**args):
    args["func"] = lambda e: e.via_bot_id is None
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    pattern = args.get("pattern", None)
    allow_sudo = args.get("allow_sudo", False)

    # get the pattern from the decorator
    if pattern is not None:
        if pattern.startswith("\#"):
            # special fix for snip.py
            args["pattern"] = re.compile(pattern)
        else:
            args["pattern"] = re.compile("\." + pattern)
            cmd = "." + pattern
            try:
                CMD_LIST[file_test].append(cmd)
            except:
                CMD_LIST.update({file_test: [cmd]})
                
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
    args["blacklist_chats"] = True
    black_list_chats = list(Config.UB_BLACK_LIST_CHAT)
    if len(black_list_chats) > 0:
        args["chats"] = black_list_chats

    # check if the plugin should allow edited updates
    allow_edited_updates = False
    if "allow_edited_updates" in args and args["allow_edited_updates"]:
        allow_edited_updates = args["allow_edited_updates"]
        del args["allow_edited_updates"]

    # check if the plugin should listen for outgoing 'messages'
    is_message_enabled = True

    return events.NewMessage(**args)


async def is_read(borg, entity, message, is_out=None):
    """
    Returns True if the given message (or id) has been read
    if a id is given, is_out needs to be a bool
    """
    is_out = getattr(message, "out", is_out)
    if not isinstance(is_out, bool):
        raise ValueError(
            "Message was id but is_out not provided or not a bool")
    message_id = getattr(message, "id", message)
    if not isinstance(message_id, int):
        raise ValueError("Failed to extract id from message")

    dialog = (await borg(GetPeerDialogsRequest([entity]))).dialogs[0]
    max_id = dialog.read_outbox_max_id if is_out else dialog.read_inbox_max_id
    return message_id <= max_id





def register(**args):
    """ Register a new event. """
    args["func"] = lambda e: e.via_bot_id is None

    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    pattern = args.get('pattern', None)
    disable_edited = args.get('disable_edited', False)
    allow_sudo = args.get("allow_sudo", False)
    
    if pattern is not None and not pattern.startswith('(?i)'):
        args['pattern'] = '(?i)' + pattern

    if "disable_edited" in args:
        del args['disable_edited']
    
    reg = re.compile('(.*)')
    if not pattern == None:
        try:
            cmd = re.search(reg, pattern)
            try:
                cmd = cmd.group(1).replace("$", "").replace("\\", "").replace("^", "")
            except:
                pass

            try:
                CMD_LIST[file_test].append(cmd)
            except:
                CMD_LIST.update({file_test: [cmd]})
        except:
            pass
      
    if allow_sudo:
        args["from_users"] = list(Config.SUDO_USERS)
        # Mutually exclusive with outgoing (can only set one of either).
        args["incoming"] = True
        del args["allow_sudo"]
        
    args["blacklist_chats"] = True
    black_list_chats = list(Config.UB_BLACK_LIST_CHAT)
    if len(black_list_chats) > 0:
        args["chats"] = black_list_chats   

    def decorator(func):
        if not disable_edited:
            bot.add_event_handler(func, events.MessageEdited(**args))
        bot.add_event_handler(func, events.NewMessage(**args))
        try:
            LOAD_PLUG[file_test].append(func)
        except Exception as e:
            LOAD_PLUG.update({file_test: [func]})

        return func

    return decorator


def errors_handler(func):
    async def wrapper(event):
        try:
            return await func(event)
        except Exception:
            pass
    return wrapper



async def progress(current, total, event, start, type_of_ps):
    """Generic progress_callback for both
    upload.py and download.py"""
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        progress_str = "[{0}{1}]\nPercent: {2}%\n".format(
            ''.join(["█" for i in range(math.floor(percentage / 5))]),
            ''.join(["░" for i in range(20 - math.floor(percentage / 5))]),
            round(percentage, 2))
        tmp = progress_str + \
            "{0} of {1}\nETA: {2}".format(
                humanbytes(current),
                humanbytes(total),
                time_formatter(estimated_total_time)
            )
        await event.edit("{}\n {}".format(
            type_of_ps,
            tmp
        ))


def humanbytes(size):
    """Input size in bytes,
    outputs in a human readable format"""
    # https://stackoverflow.com/a/49361727/4723940
    if not size:
        return ""
    # 2 ** 10 = 1024
    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {
        0: "",
        1: "Ki",
        2: "Mi",
        3: "Gi",
        4: "Ti"
    }
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


def time_formatter(milliseconds: int) -> str:
    """Inputs time in milliseconds, to get beautified time,
    as string"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "") + \
        ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2]


class Loader():
    def __init__(self, func=None, **args):
        self.Var = Var
        bot.add_event_handler(func, events.NewMessage(**args))

        

# https://github.com/andy-gh/prettyjson/blob/master/prettyjson.py


def prettyjson(obj, indent=2, maxlinelength=80):
    """Renders JSON content with indentation and line splits/concatenations to fit maxlinelength.
    Only dicts, lists and basic types are supported"""

    items, _ = getsubitems(obj, itemkey="", islast=True, maxlinelength=maxlinelength - indent, indent=indent)
    return indentitems(items, indent, level=0)


def getsubitems(obj, itemkey, islast, maxlinelength, indent):
    items = []
    is_inline = True      # at first, assume we can concatenate the inner tokens into one line

    isdict = isinstance(obj, dict)
    islist = isinstance(obj, list)
    istuple = isinstance(obj, tuple)
    isbasictype = not (isdict or islist or istuple)

    maxlinelength = max(0, maxlinelength)

    # build json content as a list of strings or child lists
    if isbasictype:
        # render basic type
        keyseparator  = "" if itemkey == "" else ": "
        itemseparator = "" if islast else ","
        items.append(itemkey + keyseparator + basictype2str(obj) + itemseparator)

    else:
        # render lists/dicts/tuples
        if isdict:    opening, closing, keys = ("{", "}", iter(obj.keys()))
        elif islist:  opening, closing, keys = ("[", "]", range(0, len(obj)))
        elif istuple: opening, closing, keys = ("[", "]", range(0, len(obj)))    # tuples are converted into json arrays

        if itemkey != "": opening = itemkey + ": " + opening
        if not islast: closing += ","

        count = 0
        itemkey = ""
        subitems = []

        # get the list of inner tokens
        for (i, k) in enumerate(keys):
            islast_ = i == len(obj)-1
            itemkey_ = ""
            if isdict: itemkey_ = basictype2str(k)
            inner, is_inner_inline = getsubitems(obj[k], itemkey_, islast_, maxlinelength - indent, indent)
            subitems.extend(inner)                        # inner can be a string or a list
            is_inline = is_inline and is_inner_inline     # if a child couldn't be rendered inline, then we are not able either

        # fit inner tokens into one or multiple lines, each no longer than maxlinelength
        if is_inline:
            multiline = True

            # in Multi-line mode items of a list/dict/tuple can be rendered in multiple lines if they don't fit on one.
            # suitable for large lists holding data that's not manually editable.

            # in Single-line mode items are rendered inline if all fit in one line, otherwise each is rendered in a separate line.
            # suitable for smaller lists or dicts where manual editing of individual items is preferred.

            # this logic may need to be customized based on visualization requirements:
            if (isdict): multiline = False
            if (islist): multiline = True

            if (multiline):
                lines = []
                current_line = ""
                current_index = 0

                for (i, item) in enumerate(subitems):
                    item_text = item
                    if i < len(inner)-1: item_text = item + ","

                    if len (current_line) > 0:
                        try_inline = current_line + " " + item_text
                    else:
                        try_inline = item_text

                    if (len(try_inline) > maxlinelength):
                        # push the current line to the list if maxlinelength is reached
                        if len(current_line) > 0: lines.append(current_line)
                        current_line = item_text
                    else:
                        # keep fitting all to one line if still below maxlinelength
                        current_line = try_inline

                    # Push the remainder of the content if end of list is reached
                    if (i == len (subitems)-1): lines.append(current_line)

                subitems = lines
                if len(subitems) > 1: is_inline = False
            else: # single-line mode
                totallength = len(subitems)-1   # spaces between items
                for item in subitems: totallength += len(item)
                if (totallength <= maxlinelength): 
                    str = ""
                    for item in subitems: str += item + " "  # insert space between items, comma is already there
                    subitems = [ str.strip() ]               # wrap concatenated content in a new list
                else:
                    is_inline = False


        # attempt to render the outer brackets + inner tokens in one line 
        if is_inline:
            item_text = ""
            if len(subitems) > 0: item_text = subitems[0]
            if len(opening) + len(item_text) + len(closing) <= maxlinelength:
                items.append(opening + item_text + closing)
            else:
                is_inline = False

        # if inner tokens are rendered in multiple lines already, then the outer brackets remain in separate lines
        if not is_inline:
            items.append(opening)       # opening brackets
            items.append(subitems)      # Append children to parent list as a nested list
            items.append(closing)       # closing brackets

    return items, is_inline


def basictype2str(obj):
    if isinstance (obj, str):
        strobj = "\"" + str(obj) + "\""
    elif isinstance(obj, bool): 
        strobj = { True: "true", False: "false" }[obj]
    else:
        strobj = str(obj)
    return strobj


def indentitems(items, indent, level):
    """Recursively traverses the list of json lines, adds indentation based on the current depth"""
    res = ""
    indentstr = " " * (indent * level)
    for (i, item) in enumerate(items):
        if isinstance(item, list): 
            res += indentitems(item, indent, level+1)
        else:
            islast = (i==len(items)-1)
            # no new line character after the last rendered line
            if level==0 and islast:
                res += indentstr + item
            else:
                res += indentstr + item + "\n"            
    return res


def parse_arguments(message: str, valid: List[str]) -> (dict, str):
    options = {}

    # Handle boolean values
    for opt in findall(r'([.!]\S+)', message):
        if opt[1:] in valid:
            if opt[0] == '.':
                options[opt[1:]] = True
            elif opt[0] == '!':
                options[opt[1:]] = False
            message = message.replace(opt, '')

    # Handle key/value pairs
    for opt in findall(r'(\S+):(?:"([\S\s]+)"|(\S+))', message):
        key, val1, val2 = opt
        value = val2 or val1[1:-1]
        if key in valid:
            if value.isnumeric():
                value = int(value)
            elif match(r'[Tt]rue|[Ff]alse', value):
                match(r'[Tt]rue', value)
            options[key] = value
            message = message.replace(f"{key}:{value}", '')

    return options, message.strip()
