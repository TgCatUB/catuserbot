import asyncio
import os
import shlex
from typing import Optional, Tuple


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


async def update_requirements():
    try:
        await runcmd("pip install --upgrade pip")
        print("Pip is upto-date")
    except BaseException:
        print("Error while updating pip")
    try:
        await runcmd("pip install -r requirements.txt")
        print("Succesfully Updated requirements")
    except Exception as e:
        print(f"Error while installing requirments {str(e)}")


loop = asyncio.get_event_loop()
loop.run_until_complete(update_requirements())
loop.close()
