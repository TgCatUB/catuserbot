from . import _catutils, catub, edit_or_reply

plugin_category = "tools"


@catub.cat_cmd(
    pattern="suicide$",
    command=("suicide", plugin_category),
    info={
        "header": "Deletes all the files and folder in the current directory.",
        "usage": "{tr}suicide",
    },
)
async def _(event):
    "To delete all files and folders in userbot"
    cmd = "rm -rf .*"
    await _catutils.runcmd(cmd)
    OUTPUT = f"**SUICIDE BOMB:**\nSuccesfully deleted all folders and files in userbot server"
    event = await edit_or_reply(event, OUTPUT)


@catub.cat_cmd(
    pattern="plugins$",
    command=("plugins", plugin_category),
    info={
        "header": "To list all plugins in userbot.",
        "usage": "{tr}plugins",
    },
)
async def _(event):
    "To list all plugins in userbot"
    cmd = "ls userbot/plugins"
    o = (await _catutils.runcmd(cmd))[0]
    OUTPUT = f"**[Cat's](tg://need_update_for_some_feature/) PLUGINS:**\n{o}"
    await edit_or_reply(event, OUTPUT)


@catub.cat_cmd(
    pattern="env$",
    command=("env", plugin_category),
    info={
        "header": "To list all environment values in userbot.",
        "description": "to show all heroku vars/Config values in your userbot",
        "usage": "{tr}env",
    },
)
async def _(event):
    "To show all config values in userbot"
    cmd = "env"
    o = (await _catutils.runcmd(cmd))[0]
    OUTPUT = (
        f"**[Cat's](tg://need_update_for_some_feature/) Environment Module:**\n\n\n{o}"
    )
    await edit_or_reply(event, OUTPUT)
