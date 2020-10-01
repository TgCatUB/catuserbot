"""Get the info your system. Using .neofetch then .sysd"""
from ..utils import admin_cmd, edit_or_reply, sudo_cmd
from . import ALIVE_NAME, CMD_HELP, runcmd

# ================= CONSTANT =================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "cat"
# ============================================


@borg.on(admin_cmd(pattern="cpu$"))
@borg.on(sudo_cmd(pattern="cpu$", allow_sudo=True))
async def _(event):
    cmd = "cat /proc/cpuinfo | grep 'model name'"
    o = (await runcmd(cmd))[0]
    await edit_or_reply(
        event, f"**[Cat's](tg://need_update_for_some_feature/) CPU Model:**\n{o}"
    )


@borg.on(admin_cmd(pattern=f"sysd$", outgoing=True))
@borg.on(sudo_cmd(pattern=f"sysd$", allow_sudo=True))
async def sysdetails(sysd):
    cmd = "git clone https://github.com/dylanaraps/neofetch.git"
    await runcmd(cmd)
    neo = "neofetch/neofetch --off --color_blocks off --bold off --cpu_temp C \
                    --cpu_speed on --cpu_cores physical --kernel_shorthand off --stdout"
    a, b, c, d = await runcmd(neo)
    result = str(a) + str(b)
    await edit_or_reply(sysd, "Neofetch Result: `" + result + "`")


CMD_HELP.update(
    {
        "sysdetails": "**Plugin : **`sysdetails`\
        \n\n**Syntax : **`.sysd`\
        \n**Usage : **Shows system information using neofetch.\
        \n\n**Syntax : **`.cpu`\
        \n**Usage : **shows the cpu information\
    "
    }
)
