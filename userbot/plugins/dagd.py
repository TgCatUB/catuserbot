import requests
from validators.url import url

from ..utils import admin_cmd, edit_or_reply, sudo_cmd
from . import CMD_HELP


@bot.on(admin_cmd(pattern="dns( (.*)|$)"))
@bot.on(sudo_cmd(pattern="dns( (.*)|$)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply = await event.get_reply_message()
    if not input_str and reply:
        input_str = reply.text
    if not input_str:
        return await edit_delete(
            event, "`Either reply to link or give link as input to get data`", 5
        )
    check = url(input_str)
    if not check:
        catstr = "http://" + input_str
        check = url(catstr)
    if not check:
        return await edit_delete(event, "`the given link is not supported`", 5)
    sample_url = f"https://da.gd/dns/{input_str}"
    response_api = requests.get(sample_url).text
    if response_api:
        await edit_or_reply(event, f"DNS records of {input_str} are \n{response_api}")
    else:
        await edit_or_reply(
            event, f"__i can't seem to find `{input_str}` on the internet__"
        )


@bot.on(admin_cmd(pattern="url( (.*)|$)"))
@bot.on(sudo_cmd(pattern="url( (.*)|$)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply = await event.get_reply_message()
    if not input_str and reply:
        input_str = reply.text
    if not input_str:
        return await edit_delete(
            event, "`Either reply to link or give link as input to get data`", 5
        )
    check = url(input_str)
    if not check:
        catstr = f"http://" + input_str
        check = url(catstr)
    if not check:
        return await edit_delete(event, "`the given link is not supported`", 5)
    sample_url = "https://da.gd/s?url={}".format(input_str)
    response_api = requests.get(sample_url).text
    if response_api:
        await edit_or_reply(
            event, "Generated {} for {}.".format(response_api, input_str)
        )
    else:
        await edit_or_reply(event, "something is wrong. please try again later.")


@bot.on(admin_cmd(pattern="unshort( (.*)|$)"))
@bot.on(sudo_cmd(pattern="unshort( (.*)|$)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply = await event.get_reply_message()
    if not input_str and reply:
        input_str = reply.text
    if not input_str:
        return await edit_delete(
            event, "`Either reply to link or give link as input to get data`", 5
        )
    check = url(input_str)
    if not check:
        catstr = "http://" + input_str
        check = url(catstr)
    if not check:
        return await edit_delete(event, "`the given link is not supported`", 5)
    if not input_str.startswith("http"):
        input_str = "http://" + input_str
    r = requests.get(input_str, allow_redirects=False)
    if str(r.status_code).startswith("3"):
        await edit_or_reply(
            event,
            "Input URL: {}\nReDirected URL: {}".format(
                input_str, r.headers["Location"]
            ),
        )
    else:
        await edit_or_reply(
            event,
            "Input URL {} returned status_code {}".format(input_str, r.status_code),
        )


# By Priyam Kalra
@bot.on(admin_cmd(pattern="hl( (.*)|$)"))
@bot.on(sudo_cmd(pattern="hl( (.*)|$)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply = await event.get_reply_message()
    if not input_str and reply:
        input_str = reply.text
    if not input_str:
        return await edit_delete(
            event, "`Either reply to link or give link as input to get data`", 5
        )
    check = url(input_str)
    if not check:
        catstr = "http://" + input_str
        check = url(catstr)
    if not check:
        return await edit_delete(event, "`the given link is not supported`", 5)
    await edit_or_reply(event, "[ㅤㅤㅤㅤㅤㅤㅤ](" + input_str + ")")


CMD_HELP.update(
    {
        "dagd": "**Plugin : **`dagd`\
        \n\n**Syntax :** `.dns link`\
        \n**Function : **__Shows you Domain Name System(dns) of the given link . example `.dns google.com` or `.dns github.cm`__\
        \n\n**Syntax : **`.url link`\
        \n**Function : **__shortens the given link__\
        \n\n**Syntax : **`.unshort link`\
        \n**Function : **__unshortens the given short link__\
        \n\n**Syntax : **`.hl` <link>\
        \n**Function : **__Hide the given link__\
    "
    }
)
