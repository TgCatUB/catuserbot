# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
"""
This module updates the userbot based on chtream revision
"""

from os import remove, execl
import sys

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from userbot import CMD_HELP, bot, HEROKU_API_KEY, HEROKU_APP_NAME, HEROKU_MEMEZ
from userbot.utils import register


async def gen_chlog(repo, diff):
    ch_log = ''
    d_form = "%d/%m/%y"
    for c in repo.iter_commits(diff):
        ch_log += f'•[{c.committed_datetime.strftime(d_form)}]: {c.summary} <{c.author}>\n'
    return ch_log


async def is_off_br(br):
    off_br = ['sql-extended']
    for k in off_br:
        if k == br:
            return 1
    return


@register(outgoing=True, pattern="^.chl(?: |$)(.*)")
async def chtream(ch):
    "For .update command, check if the bot is up to date, update if specified"
    await ch.edit("`Checking for updates, please wait....`")
    conf = ch.pattern_match.group(1).lower()
    off_repo = 'https://github.com/sandy1709/catuserbot.git'

    try:
        txt = "`Oops.. Updater cannot continue due to some problems occured`\n\n**LOGTRACE:**\n"
        repo = Repo()
    except NoSuchPathError as error:
        await ch.edit(f'{txt}\n`directory {error} is not found`')
        return
    except GitCommandError as error:
        await ch.edit(f'{txt}\n`Early failure! {error}`')
        return
    except InvalidGitRepositoryError:
        repo = Repo.init()
        await ch.edit(
            "`Warning: Force-Syncing to the latest stable code from repo.`\
            \nI may lose my downloaded files during this update."
        )
        origin = repo.create_remote('chtream', off_repo)
        origin.fetch()
        repo.create_head('sql-extended', origin.refs.master)
        repo.heads.master.checkout(True)

    ac_br = repo.active_branch.name
    if not await is_off_br(ac_br):
        await ch.edit(
            f'**[UPDATER]:**` Looks like you are using your own custom branch ({ac_br}). \
            in that case, Updater is unable to identify which branch is to be merged. \
            please checkout to any official branch`')
        return

    try:
        repo.create_remote('chtream', off_repo)
    except BaseException:
        pass

    ch_rem = repo.remote('chtream')
    ch_rem.fetch(ac_br)
    changelog = await gen_chlog(repo, f'HEAD..chtream/{ac_br}')

    if not changelog:
        await ch.edit(f'\n`Your BOT is` **up-to-date** `with` **{ac_br}**\n')
        return

    if conf != "w":
        changelog_str = f'**New UPDATE available for [{ac_br}]:\n\nCHANGELOG:**\n`{changelog}`'
        if len(changelog_str) > 4096:
            await ch.edit("`Changelog is too big, sending it as a file.`")
            file = open("output.txt", "w+")
            file.write(changelog_str)
            file.close()
            await ch.client.send_file(
                ch.chat_id,
                "output.txt",
                reply_to=ch.id,
            )
            remove("output.txt")
        else:
            await ch.edit(changelog_str)
        await ch.respond(
            "`do \".update \" to update\nif using Heroku`")
        return

    await ch.edit('`New update found, updating...`')
    ch_rem.fetch(ac_br)
    await ch.edit('`Successfully Updated!\n'
                   'Bot is restarting... Wait for a second!`')
    await install_requirements()
    await bot.disconnect()
    # Spin a new instance of bot
    execl(sys.executable, sys.executable, *sys.argv)
    # Shut the existing one down
    exit()


CMD_HELP.update({
    'update':
    ".chl\
\nUsage: Checks if the main userbot repository has any updates and shows a changelog if so.\
\n\n.update\
\nUsage: Updates your userbot, if there are any updates in the main userbot repository."
})
