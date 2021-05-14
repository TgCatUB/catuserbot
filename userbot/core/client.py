import datetime
import inspect
import re
import sys
import traceback
from pathlib import Path
from typing import Dict, List, Union

from telethon import TelegramClient, events

from ..Config import Config
from ..helpers.utils import _catutils
from . import BOT_INFO, CMD_INFO, GRP_INFO, PLG_INFO
from .cmdinfo import _format_about
from .events import MessageEdited, NewMessage
from .fasttelethon import download_file, upload_file
from .logger import logging
from .managers import edit_delete
from .sudo import _sudousers_list

LOGS = logging.getLogger(__name__)


class REGEX:
    def __init__(self):
        self.regex = ""
        self.regex1 = ""
        self.regex2 = ""


REGEX_ = REGEX()


class CatUserBotClient(TelegramClient):
    def cat_cmd(
        self: TelegramClient,
        pattern: str or tuple = None,
        info: Union[str, Dict[str, Union[str, List[str], Dict[str, str]]]]
        or tuple = None,
        groups_only: bool = False,
        allow_sudo: bool = True,
        edited: bool = True,
        disable_errors: bool = False,
        command: str or tuple = None,
        **kwargs,
    ) -> callable:  # sourcery no-metrics
        kwargs["func"] = kwargs.get("func", lambda e: e.via_bot_id is None)
        kwargs.setdefault("forwards", False)
        stack = inspect.stack()
        previous_stack_frame = stack[1]
        file_test = Path(previous_stack_frame.filename)
        file_test = file_test.stem.replace(".py", "")
        # get the pattern from the decorator
        if command is not None:
            command = list(command)
            if not command[1] in BOT_INFO:
                BOT_INFO.append(command[1])
            try:
                if not file_test in GRP_INFO[command[1]]:
                    GRP_INFO[command[1]].append(file_test)
            except BaseException:
                GRP_INFO.update({command[1]: [file_test]})
            try:
                PLG_INFO[file_test].append(command[0])
            except BaseException:
                PLG_INFO.update({file_test: [command[0]]})
            CMD_INFO[command[0]] = [_format_about(info)]
        if pattern is not None:
            if (
                pattern.startswith(r"\#")
                or not pattern.startswith(r"\#")
                and pattern.startswith(r"^")
            ):
                REGEX_.regex1 = REGEX_.regex2 = re.compile(pattern)
            else:
                reg1 = "\\" + Config.COMMAND_HAND_LER
                reg2 = "\\" + Config.SUDO_COMMAND_HAND_LER
                REGEX_.regex1 = re.compile(reg1 + pattern)
                REGEX_.regex2 = re.compile(reg2 + pattern)

        def decorator(func):
            async def wrapper(check):
                if groups_only and not check.is_group:
                    await edit_delete(check, "`I don't think this is a group.`", 10)
                    return
                try:
                    await func(check)
                except events.StopPropagation:
                    raise events.StopPropagation
                except KeyboardInterrupt:
                    pass
                except BaseException as e:
                    # Check if we have to disable error logging.
                    LOGS.exception(e)  # Log the error in console
                    if not disable_errors:
                        if Config.PRIVATE_GROUP_BOT_API_ID == 0:
                            return
                        date = (datetime.datetime.now()).strftime("%m/%d/%Y, %H:%M:%S")
                        ftext = f"\nDisclaimer:\nThis file is pasted only here ONLY here,\
                                  \nwe logged only fact of error and date,\nwe respect your privacy,\
                                  \nyou may not report this error if you've\
                                  \nany confidential data here, no one will see your data\
                                  \n\n--------BEGIN USERBOT TRACEBACK LOG--------\
                                  \nDate: {date}\nGroup ID: {str(check.chat_id)}\
                                  \nSender ID: {str(check.sender_id)}\
                                  \n\nEvent Trigger:\n{str(check.text)}\
                                  \n\nTraceback info:\n{str(traceback.format_exc())}\
                                  \n\nError text:\n{str(sys.exc_info()[1])}"
                        new = {
                            "error": str(sys.exc_info()[1]),
                            "date": datetime.datetime.now(),
                        }
                        ftext += "\n\n--------END USERBOT TRACEBACK LOG--------"
                        command = 'git log --pretty=format:"%an: %s" -5'
                        ftext += "\n\n\nLast 5 commits:\n"
                        output = (await _catutils.runcmd(command))[:2]
                        result = output[0] + output[1]
                        ftext += result
                        from ..helpers.utils.format import paste_text

                        pastelink = paste_text(ftext)
                        text = "**CatUserbot Error report**\n\n"
                        link = "[here](https://t.me/catuserbot_support)"
                        text += "If you wanna you can report it"
                        text += f"- just forward this message {link}.\n"
                        text += (
                            "Nothing is logged except the fact of error and date\n\n"
                        )
                        text += f"**Error report : ** [{new['error']}]({pastelink})"
                        await check.client.send_message(
                            Config.PRIVATE_GROUP_BOT_API_ID, text, link_preview=False
                        )

            from .session import catub

            if not func.__doc__ is None:
                CMD_INFO[command[0]].append((func.__doc__).strip())
            if pattern is not None:
                if allow_sudo:
                    if edited:
                        catub.add_event_handler(
                            wrapper,
                            MessageEdited(
                                pattern=REGEX_.regex1, outgoing=True, **kwargs
                            ),
                        )
                        catub.add_event_handler(
                            wrapper,
                            MessageEdited(
                                pattern=REGEX_.regex2,
                                from_users=_sudousers_list(),
                                **kwargs,
                            ),
                        )
                    catub.add_event_handler(
                        wrapper,
                        NewMessage(pattern=REGEX_.regex1, outgoing=True, **kwargs),
                    )
                    catub.add_event_handler(
                        wrapper,
                        NewMessage(
                            pattern=REGEX_.regex2,
                            from_users=_sudousers_list(),
                            **kwargs,
                        ),
                    )
                else:
                    if edited:
                        catub.add_event_handler(
                            wrapper,
                            MessageEdited(
                                pattern=REGEX_.regex1, outgoing=True, **kwargs
                            ),
                        )
                    catub.add_event_handler(
                        wrapper,
                        NewMessage(pattern=REGEX_.regex1, outgoing=True, **kwargs),
                    )
            else:
                if edited:
                    catub.add_event_handler(func, events.MessageEdited(**kwargs))
                catub.add_event_handler(func, events.NewMessage(**kwargs))
            return wrapper

        return decorator

    def bot_cmd(
        self: TelegramClient,
        disable_errors: bool = False,
        **kwargs,
    ) -> callable:  # sourcery no-metrics
        kwargs["func"] = kwargs.get("func", lambda e: e.via_bot_id is None)
        def decorator(func):
            async def wrapper(check):
                try:
                    await func(check)
                except events.StopPropagation:
                    raise events.StopPropagation
                except KeyboardInterrupt:
                    pass
                except BaseException as e:
                    # Check if we have to disable error logging.
                    LOGS.exception(e)  # Log the error in console
                    if not disable_errors:
                        if Config.PRIVATE_GROUP_BOT_API_ID == 0:
                            return
                        date = (datetime.datetime.now()).strftime("%m/%d/%Y, %H:%M:%S")
                        ftext = f"\nDisclaimer:\nThis file is pasted only here ONLY here,\
                                    \nwe logged only fact of error and date,\nwe respect your privacy,\
                                    \nyou may not report this error if you've\
                                    \nany confidential data here, no one will see your data\
                                    \n\n--------BEGIN USERBOT TRACEBACK LOG--------\
                                    \nDate: {date}\nGroup ID: {str(check.chat_id)}\
                                    \nSender ID: {str(check.sender_id)}\
                                    \n\nEvent Trigger:\n{str(check.text)}\
                                    \n\nTraceback info:\n{str(traceback.format_exc())}\
                                    \n\nError text:\n{str(sys.exc_info()[1])}"
                        new = {
                            "error": str(sys.exc_info()[1]),
                            "date": datetime.datetime.now(),
                        }
                        ftext += "\n\n--------END USERBOT TRACEBACK LOG--------"
                        command = 'git log --pretty=format:"%an: %s" -5'
                        ftext += "\n\n\nLast 5 commits:\n"
                        output = (await _catutils.runcmd(command))[:2]
                        result = output[0] + output[1]
                        ftext += result
                        from ..helpers.utils.format import paste_text

                        pastelink = paste_text(ftext)
                        text = "**CatUserbot Error report**\n\n"
                        link = "[here](https://t.me/catuserbot_support)"
                        text += "If you wanna you can report it"
                        text += f"- just forward this message {link}.\n"
                        text += (
                            "Nothing is logged except the fact of error and date\n\n"
                        )
                        text += f"**Error report : ** [{new['error']}]({pastelink})"
                        await check.client.send_message(
                            Config.PRIVATE_GROUP_BOT_API_ID, text, link_preview=False
                        )

            from .session import catub
            catub.tgbot.add_event_handler(func, events.NewMessage(**kwargs))
            return wrapper

        return decorator

    async def get_traceback(self, exc: Exception) -> str:
        return "".join(
            traceback.format_exception(etype=type(exc), value=exc, tb=exc.__traceback__)
        )

    def _kill_running_processes(self) -> None:
        """Kill all the running asyncio subprocessess"""
        for _, process in self.running_processes.items():
            try:
                process.kill()
                LOGS.debug("Killed %d which was still running.", process.pid)
            except Exception as e:
                LOGS.debug(e)
        self.running_processes.clear()


CatUserBotClient.fast_download_file = download_file
CatUserBotClient.fast_upload_file = upload_file
