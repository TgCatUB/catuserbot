import asyncio
import base64
import os
import time
from subprocess import PIPE
from subprocess import run as runapp

from userbot import catub

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import progress
from ..helpers.tools import media_type

plugin_category = "tools"


@catub.cat_cmd(
    pattern="hash ([\s\S]*)",
    command=("hash", plugin_category),
    info={
        "header": "Find the md5, sha1, sha256, sha512 of the string when written into a txt file.",
        "usage": "{tr}hash <text>",
        "examples": "{tr}hash catuserbot",
    },
)
async def gethash(hash_q):
    "Find the md5, sha1, sha256, sha512 of the string when written into a txt file."
    hashtxt_ = "".join(hash_q.text.split(maxsplit=1)[1:])
    with open("hashdis.txt", "w+") as hashtxt:
        hashtxt.write(hashtxt_)
    md5 = runapp(["md5sum", "hashdis.txt"], stdout=PIPE)
    md5 = md5.stdout.decode()
    sha1 = runapp(["sha1sum", "hashdis.txt"], stdout=PIPE)
    sha1 = sha1.stdout.decode()
    sha256 = runapp(["sha256sum", "hashdis.txt"], stdout=PIPE)
    sha256 = sha256.stdout.decode()
    sha512 = runapp(["sha512sum", "hashdis.txt"], stdout=PIPE)
    runapp(["rm", "hashdis.txt"], stdout=PIPE)
    sha512 = sha512.stdout.decode()
    ans = f"**Text : **\
            \n`{hashtxt_}`\
            \n**MD5 : **`\
            \n`{md5}`\
            \n**SHA1 : **`\
            \n`{sha1}`\
            \n**SHA256 : **`\
            \n`{sha256}`\
            \n**SHA512 : **`\
            \n`{sha512[:-1]}`\
         "
    await edit_or_reply(hash_q, ans)


@catub.cat_cmd(
    pattern="hbase (en|de) ([\s\S]*)",
    command=("hbase", plugin_category),
    info={
        "header": "Find the base64 encoding or decoding of the given string.",
        "flags": {
            "en": "Use this to encode the given text.",
            "de": "use this to decode the given text.",
        },
        "usage": ["{tr}hbase en <text to encode>", "{tr}hbase de <encoded text>"],
        "examples": ["{tr}hbase en Catuserbot", "{tr}hbase de Q2F0dXNlcmJvdA=="],
    },
)
async def endecrypt(event):
    "To encode or decode the string using base64"
    string = "".join(event.text.split(maxsplit=2)[2:])
    catevent = event
    if event.pattern_match.group(1) == "en":
        if string:
            result = base64.b64encode(bytes(string, "utf-8")).decode("utf-8")
            result = f"**Shhh! It's Encoded : **\n`{result}`"
        else:
            reply = await event.get_reply_message()
            if not reply:
                return await edit_delete(event, "`What should i encode`")
            mediatype = media_type(reply)
            if mediatype is None:
                result = base64.b64encode(bytes(reply.text, "utf-8")).decode("utf-8")
                result = f"**Shhh! It's Encoded : **\n`{result}`"
            else:
                catevent = await edit_or_reply(event, "`Encoding ...`")
                c_time = time.time()
                downloaded_file_name = await event.client.download_media(
                    reply,
                    Config.TMP_DOWNLOAD_DIRECTORY,
                    progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                        progress(d, t, catevent, c_time, "trying to download")
                    ),
                )
                catevent = await edit_or_reply(event, "`Encoding ...`")
                with open(downloaded_file_name, "rb") as image_file:
                    result = base64.b64encode(image_file.read()).decode("utf-8")
                os.remove(downloaded_file_name)
        await edit_or_reply(
            catevent, result, file_name="encodedfile.txt", caption="It's Encoded"
        )
    else:
        try:
            lething = str(
                base64.b64decode(
                    bytes(event.pattern_match.group(2), "utf-8"), validate=True
                )
            )[2:]
            await edit_or_reply(event, "**Decoded text :**\n`" + lething[:-1] + "`")
        except Exception as e:
            await edit_delete(event, f"**Error:**\n__{e}__")
