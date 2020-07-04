#credits to @mrconfused 
from telethon import events, errors, functions, types
import inspect
import traceback
import asyncio
import sys
import io
from userbot.utils import admin_cmd
from userbot import CMD_HELP

@borg.on(admin_cmd(pattern="calc"))
async def _(event):
    if event.fwd_from or event.via_bot_id:
        return
    await event.edit("Processing ...")
    cmd = event.text.split(" ", maxsplit=1)[1]
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
        
    san = f"print({cmd})"
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(san, event)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Something went wrong"

    final_output = "**EQUATION**: `{}` \n\n **SOLUTION**: \n`{}` \n".format(cmd, evaluation)
    await event.edit(final_output)

async def aexec(code, event):
    exec(
        f'async def __aexec(event): ' +
        ''.join(f'\n {l}' for l in code.split('\n'))
    )
    return await locals()['__aexec'](event)

CMD_HELP.update({"calc": "`.calc` your equation :\
      \nUSAGE: solves the given maths equation by bodmass rule. "
}) 
