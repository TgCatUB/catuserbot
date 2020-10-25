# credits to @mrconfused
import io
import sys
import traceback

from .. import CMD_HELP
from ..utils import admin_cmd, edit_or_reply, sudo_cmd


@bot.on(admin_cmd(pattern="calc (.*)"))
@bot.on(sudo_cmd(pattern="calc (.*)", allow_sudo=True))
async def _(car):
    cmd = car.text.split(" ", maxsplit=1)[1]
    event = await edit_or_reply(car, "Calculating ...")
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    san = f"print({cmd})"
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
        evaluation = "Sorry I cant find result for the given equation"
    final_output = "**EQUATION**: `{}` \n\n **SOLUTION**: \n`{}` \n".format(
        cmd, evaluation
    )
    await event.edit(final_output)


async def aexec(code, event):
    exec(f"async def __aexec(event): " + "".join(f"\n {l}" for l in code.split("\n")))
    return await locals()["__aexec"](event)


CMD_HELP.update(
    {
        "calc": "**Plugin : **`calc`\
        \n\n**Syntax : **`.calc expression` \
        \n**Function : **solves the given maths equation by bodmass rule. "
    }
)
