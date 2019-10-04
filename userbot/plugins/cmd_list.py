from userbot import CMD_LIST

@command(pattern="^.get_cmd")
async def cmd_list(event):
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        string = ""
        for i in CMD_LIST:
            string += "ℹ️ `" + str(i)
            string += "`\n"
        await event.edit(string)
