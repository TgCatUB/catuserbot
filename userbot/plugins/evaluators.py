# Execute GNU/Linux commands inside Telegram

import asyncio
import io
import os
import sys
import traceback

from ..utils import admin_cmd, edit_or_reply, sudo_cmd
from . import *


@bot.on(admin_cmd(pattern="exec(?: |$|\n)(.*)", command="exec"))
@bot.on(sudo_cmd(pattern="exec(?: |$|\n)(.*)", command="exec", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    cmd = "".join(event.text.split(maxsplit=1)[1:])
    if not cmd:
        return await edit_delete(event, "`What should i execute?..`")
    catevent = await edit_or_reply(event, "`Executing.....`")
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    result = str(stdout.decode().strip()) + str(stderr.decode().strip())
    catuser = await event.client.get_me()
    if catuser.username:
        curruser = catuser.username
    else:
        curruser = "catuserbot"
    uid = os.geteuid()
    if uid == 0:
        cresult = f"`{curruser}:~#` `{cmd}`\n`{result}`"
    else:
        cresult = f"`{curruser}:~$` `{cmd}`\n`{result}`"
    await edit_or_reply(
        catevent,
        text=cresult,
        aslink=True,
        linktext=f"**•  Exec : **\n`{cmd}` \n\n**•  Result : **\n",
    )
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "Terminal command " + cmd + " was executed sucessfully.",
        )


@bot.on(admin_cmd(pattern="eval(?: |$|\n)(.*)", command="eval"))
@bot.on(sudo_cmd(pattern="eval(?: |$|\n)(.*)", command="eval", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    cmd = "".join(event.text.split(maxsplit=1)[1:])
    if not cmd:
        return await edit_delete(event, "`What should i run ?..`")
    catevent = await edit_or_reply(event, "`Running ...`")
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, event)
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
        evaluation = "Success"
    final_output = f"**•  Eval : **\n`{cmd}` \n\n**•  Result : **\n`{evaluation}` \n"
    await edit_or_reply(
        catevent,
        text=final_output,
        aslink=True,
        linktext=f"**•  Eval : **\n`{cmd}` \n\n**•  Result : **\n",
    )
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "eval command " + cmd + " was executed sucessfully.",
        )


async def aexec(code, smessatatus):
    message = event = smessatatus
    p = lambda _x: print(yaml_format(_x))
    reply = await event.get_reply_message()
    exec(
        f"async def __aexec(message, event , reply, client, p, chat): "
        + "".join(f"\n {l}" for l in code.split("\n"))
    )
    return await locals()["__aexec"](
        message, event, reply, message.client, p, message.chat_id
    )


CMD_HELP.update(
    {
        "evaluators": "__**PLUGIN NAME :** Evaluators__\
     \n\n📌** CMD ➥** `.eval` <expr>\
     \n**USAGE   ➥  **Execute Python script.\
     \n\n📌** CMD ➥** `.exec` <command>\
     \n**USAGE   ➥  **Execute a bash command on catuserbot server and shows details.\
     \n\n📌** CMD ➥** `.bash` <command>\
     \n**USAGE   ➥  **Execute a bash command on catuserbot server and  easy to copy output\
     "
    }
)
