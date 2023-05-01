# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import asyncio

from telethon.errors import FloodWaitError, MessageNotModifiedError

from ..Config import Config
from ..sql_helper.globals import gvarstatus
from .data import _vcusers_list


class check_owner:
    def __init__(self, func=None, vc=False):
        self.func = func
        self.vc = vc

    def __call__(self, *args, **kwargs):
        if not self.func:
            return self.__class__(args[0], vc=self.vc)

        async def wrapper(*args, **kwargs):
            c_q = args[0]
            if c_q.query.user_id and (
                c_q.query.user_id == Config.OWNER_ID
                or c_q.query.user_id in Config.SUDO_USERS
                or (self.vc and c_q.query.user_id in _vcusers_list())
            ):
                try:
                    await self.func(c_q)
                except FloodWaitError as e:
                    await asyncio.sleep(e.seconds + 5)
                except MessageNotModifiedError:
                    pass
            else:
                HELP_TEXT = (
                    gvarstatus("HELP_TEXT")
                    or "Only My Master can Access This !!\n\nDeploy your own Catuserbot."
                )
                await c_q.answer(
                    HELP_TEXT,
                    alert=True,
                )

        return wrapper(*args, **kwargs)
