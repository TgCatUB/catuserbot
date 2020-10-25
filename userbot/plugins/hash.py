# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.

""" Userbot module containing hash and encode/decode commands. """

from subprocess import PIPE
from subprocess import run as runapp

import pybase64

from .. import CMD_HELP
from ..utils import admin_cmd, edit_or_reply, errors_handler, sudo_cmd


@bot.on(admin_cmd(outgoing=True, pattern="hash (.*)"))
@bot.on(sudo_cmd(allow_sudo=True, pattern="hash (.*)"))
@errors_handler
async def gethash(hash_q):
    """ For .hash command, find the md5, sha1, sha256, sha512 of the string. """
    hashtxt_ = hash_q.pattern_match.group(1)
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
    ans = (
        "**Text : **`"
        + hashtxt_
        + "`\n**MD5 : **`"
        + md5
        + "`**SHA1 : **`"
        + sha1
        + "`**SHA256 : **`"
        + sha256
        + "`**SHA512 : **`"
        + sha512[:-1]
        + "`"
    )
    if len(ans) > 4096:
        with open("hashes.txt", "w+") as hashfile:
            hashfile.write(ans)
        await hash_q.client.send_file(
            hash_q.chat_id,
            "hashes.txt",
            reply_to=hash_q.id,
            caption="`It's too big, sending a text file instead. `",
        )
        runapp(["rm", "hashes.txt"], stdout=PIPE)
    else:
        await edit_or_reply(hash_q, ans)


@bot.on(admin_cmd(outgoing=True, pattern="hbase (en|de) (.*)"))
@bot.on(sudo_cmd(allow_sudo=True, pattern="hbase (en|de) (.*)"))
@errors_handler
async def endecrypt(query):
    """ For .base64 command, find the base64 encoding of the given string. """
    if query.pattern_match.group(1) == "en":
        lething = str(pybase64.b64encode(bytes(query.pattern_match.group(2), "utf-8")))[
            2:
        ]
        await edit_or_reply(query, "Shhh! It's Encoded: `" + lething[:-1] + "`")
    else:
        lething = str(
            pybase64.b64decode(
                bytes(query.pattern_match.group(2), "utf-8"), validate=True
            )
        )[2:]
        await edit_or_reply(query, "Decoded: `" + lething[:-1] + "`")


CMD_HELP.update(
    {
        "hash": "**Plugin : **`hash`\
        \n\n**Syntax : **`.hbase en toencode-text or .hbase de encoded-text`\
        \n**Function : **__Find the base64 encoding of the given string or decoding of string__\
        \n\n**Syntax : **`.hash text`\
        \n**Function : **__Find the md5, sha1, sha256, sha512 of the string when written into a txt file.__"
    }
)
