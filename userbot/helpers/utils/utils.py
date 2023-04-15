# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import asyncio
import functools
import shlex
from typing import Tuple

from ...core.logger import logging

LOGS = logging.getLogger(__name__)


# executing of terminal commands
async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )


def run_sync(func, *args, **kwargs):
    return asyncio.get_event_loop().run_in_executor(
        None, functools.partial(func, *args, **kwargs)
    )


def run_async(loop, coro):
    return asyncio.run_coroutine_threadsafe(coro, loop).result()


def runasync(func: callable):
    """Run async functions with the right event loop."""
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(func)
