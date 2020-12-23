from asyncio import sleep


@bot.on(admin_cmd(pattern="sdm (\d*) (.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="sdm (\d*) (.*)", allow_sudo=True))
async def selfdestruct(destroy):
    cat = ("".join(destroy.text.split(maxsplit=1)[1:])).split(" ", 1)
    message = cat[1]
    ttl = int(cat[0])
    try:
        await destroy.delete()
    except:
        pass
    smsg = await destroy.client.send_message(destroy.chat_id, message)
    await sleep(ttl)
    await smsg.delete()


@bot.on(admin_cmd(pattern="selfdm (\d*) (.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="selfdm (\d*) (.*)", allow_sudo=True))
async def selfdestruct(destroy):
    cat = ("".join(destroy.text.split(maxsplit=1)[1:])).split(" ", 1)
    message = cat[1]
    ttl = int(cat[0])
    text = (
        message + f"\n\n`This message shall be self-destructed in {str(ttl)} seconds`"
    )
    try:
        await destroy.delete()
    except:
        pass
    smsg = await destroy.client.send_message(destroy.chat_id, text)
    await sleep(ttl)
    await smsg.delete()


CMD_HELP.update(
    {
        "selfdestruct": "__**PLUGIN NAME :** Selfdestruct__\
\n\n📌** CMD ➥** `.sdm` [number] [text]\
\n**USAGE   ➥  **Self destruct this message in number seconds \
\n\n📌** CMD ➥** `.selfd` [number] [text]\
\n**USAGE   ➥  **Self destruct this message in number seconds with showing that it will destruct. \
"
    }
)
