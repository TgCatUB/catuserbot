
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K && @INF1N17Y

from telethon import events
from telethon.tl.functions.users import GetFullUserRequest
import os
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location

from userbot import bot

@borg.on(admin_cmd(pattern=r"mention"))
@bot.on(events.MessageEdited(pattern="^.mention ?(.*)", outgoing=True))
async def mention(e):
	if e.fwd_from:
		return	
	input_str = e.pattern_match.group(1)

	if e.reply_to_msg_id:
		previous_message = await e.get_reply_message()
		if previous_message.forward:
			replied_user = await bot(GetFullUserRequest(previous_message.forward.from_id))
		else:
			replied_user = await bot(GetFullUserRequest(previous_message.from_id))
	else:
		if e.message.entities is not None:
			mention_entity = e.message.entities
			probable_user_mention_entity = mention_entity[0]
			if type(probable_user_mention_entity) == MessageEntityMentionName:
				user_id = probable_user_mention_entity.user_id
				replied_user = await bot(GetFullUserRequest(user_id))
		else:
			try:
				user_object = await bot.get_entity(input_str)
				user_id = user_object.id
				replied_user = await bot(GetFullUserRequest(user_id))
			except Exception as e:
				await e.edit(str(e))
				return None

	user_id = replied_user.user.id
	caption = """<a href='tg://user?id={}'>{}</a>""".format(user_id, input_str)
	await bot.send_message(
		e.chat_id,
		caption,
		parse_mode="HTML",        
		force_document=False,
		silent=True
		)
	await e.delete()
