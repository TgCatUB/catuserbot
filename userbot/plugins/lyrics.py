# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
#

"""
Copyright (C) 2019 The Raphielscape Company LLC.

Genius lyrics plugin
	get this value from https://genius.com/developers

Add:-  GENIUS_API_TOKEN and token value in heroku app settings
     & GENIUS and token value in heroku app settings

Lyrics Plugin Syntax:
	.lyrics <aritst name, song nane>
"""

from uniborg.util import admin_cmd
import os
from telethon.tl.types import DocumentAttributeFilename, MessageMediaPhoto
from telethon import events
GApi = os.environ.get("GENIUS_API_TOKEN", None)

"""Genius(lyrics) staff"""

import lyricsgenius
genius = lyricsgenius.Genius(GApi)


@borg.on(admin_cmd(pattern='lyrics(?: |$)(.*)'))
async def lyrics(lyr):
	if GApi == 'None':
		await lyr.edit(
			"`Kek provide genius api token to Var.py or Heroku Var first kthxbye!`"
		)
	try:
		args = lyr.text.split()
		artist = lyr.text.split()[1]
		snameinit = lyr.text.split(' ', 2)
		sname = snameinit[2]
	except Exception:
		await lyr.edit("`Lel pls provide artist and song names U Dumb`")
		return

	#Try to search for * in artist string(for multiword artist name)
	try:
		artist = artist.replace('*', ' ')
	except Exception:
		artist = lyr.text.split()[1]
		pass

	if len(args) < 3:
		await lyr.edit("`Please provide artist and song names`")

	await lyr.edit(f"`Searching lyrics for {artist} - {sname}...`")

	try:
		song = genius.search_song(sname, artist)
	except TypeError:
		song = None

	if song is None:
		await lyr.edit(f"Song **{artist} - {sname}** not found!")
		return
	if len(song.lyrics) > 4096:
			await lyr.edit("`Lyrics is too big, view the file to see it.`")
			file = open("lyrics.txt", "w+")
			file.write(f"Search query: \n{artist} - {sname}\n\n{song.lyrics}")
			file.close()
			await lyr.client.send_file(
				lyr.chat_id,
				"lyrics.txt",
				reply_to=lyr.id,
			)
			os.remove("lyrics.txt")
	else:
		await lyr.edit(f"**Search query**: \n`{artist} - {sname}`\n\n```{song.lyrics}```")
	return



@borg.on(admin_cmd(pattern='iff(?: |$)(.*)'))
async def pressf(f):
	"""Pays respects"""
	args = f.text.split()
	arg = (f.text.split(' ', 1))[1] if len(args) > 1 else None
	if len(args) == 1:
		r = random.randint(0, 3)
		logger.info(r)
		if r == 0:
			await f.edit("┏━━━┓\n┃┏━━┛\n┃┗━━┓\n┃┏━━┛\n┃┃\n┗┛")
		elif r == 1:
			await f.edit("╭━━━╮\n┃╭━━╯\n┃╰━━╮\n┃╭━━╯\n┃┃\n╰╯")
		else:
			arg = "F"
	if arg is not None:
		out = ""
		F_LENGTHS = [5, 1, 1, 4, 1, 1, 1]
		for line in F_LENGTHS:
			c = max(round(line / len(arg)), 1)
			out += (arg * c) + "\n"
		await f.edit("`" + out + "`")

