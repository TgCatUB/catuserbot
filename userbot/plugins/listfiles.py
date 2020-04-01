"""
List Files plugin for userbot //Simple Module for people who dont wanna use shell executor for listing files.
cmd: .ls // will return files from current working directory
	 .ls path // will return output according to path  

By:- @Zero_cool7870

"""

from uniborg.util import admin_cmd
import asyncio
import os


@borg.on(admin_cmd(pattern="ls ?(.*)", allow_sudo=True))
async def lst(event):
	if event.fwd_from:
		return
	input_str = event.pattern_match.group(1)
	if input_str:
		msg = "**Files in {} :**\n".format(input_str)
		files = os.listdir(input_str)
	else:
		msg = "**Files in Current Directory :**\n"
		files = os.listdir(os.getcwd())
	for file in files:
		msg += "`{}`\n".format(file)
	if len(msg) <= Config.MAX_MESSAGE_SIZE_LIMIT:
		await event.edit(msg)
	else:
		msg = msg.replace("`","")
		out = 'filesList.txt'
		with open(out,'w') as f:
			f.write(f)
		await borg.send_file(
				event.chat_id,
				out,
				force_document=True,
				allow_cache=False,
				caption="`Output is huge. Sending as a file...`"
		)
		await event.delete()	

			

			

				

        
