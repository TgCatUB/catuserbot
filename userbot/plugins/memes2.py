import asyncio
from userbot.utils import admin_cmd


@borg.on(admin_cmd(pattern="ccry$"))
async def cry(e):
        await e.edit("(;´༎ຶД༎ຶ)")

@borg.on(admin_cmd(pattern="fp$"))
async def facepalm(e):
        await e.edit("🤦‍♂")
