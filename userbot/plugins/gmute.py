"""
G-Muter Plugin for userbot. //Needs MongoDB to work.
cmds: .gmute user_id|reply to user messsage	//G-Mutes a User.
	  .ungmute user_id|reply to user messsage //Un-Gmutes a User.
	  .listgmuted //List Currently G-Muted Users.

By:- JaskaranSM ( @Zero_cool7870 )

"""

from telethon import events
import logging
import asyncio
from uniborg.util import admin_cmd
logging.basicConfig(level=logging.INFO)
MONGO_URI = Config.MONGO_URI
try:	
	db = mongo_client['test']
	muted = db.muted
except Exception as e:
	logging.error(str(e))	

@borg.on(admin_cmd(pattern="gmute ?(.*)", allow_sudo=True))
async def gmute_user(event):
	if event.fwd_from:
		return
	input_str = event.pattern_match.group(1)	
	if not event.reply_to_msg_id and not input_str:
		await event.edit("`Give a User id or Reply To a User Message To Mute.`")
		return	
	if event.reply_to_msg_id:
		msg = await event.get_reply_message()
		user_id = msg.from_id	
	else:
		user_id = int(input_str)

	await event.edit("`Getting a duct tape..`")	
	try:
		chat = await event.get_chat()
		is_admin = chat.admin_rights
		is_creator = chat.creator
	except:
		await event.edit("`You Need to Run this command in a Group Chat.`")	
		return
	if is_admin or is_creator:	
		try:
			c = muted.find({})
			for i in c:
				if i['user_id'] == user_id:
					await event.edit("`User is Already G-Muted.`")
					return
			if user_id == borg.me.id:
					await event.edit("`Cant Mute Myself..`")
					return
			else:
				muted.insert_one({'user_id':user_id})
				await event.edit("`G-Muted` [{}](tg://user?id={}).".format(str(user_id),str(user_id)))
				logging.info("G-Muted {}".format(str(user_id)))
		except Exception as e:
			logging.error(str(e))
			await event.edit("Error: "+str(e))
			return
	else:		
		await event.edit("`You are not admin Here.`")	

@borg.on(admin_cmd(pattern="ungmute ?(.*)", allow_sudo=True))
async def un_gmute_user(event):
	if event.fwd_from:
		return
	input_str = event.pattern_match.group(1)	
	if not event.reply_to_msg_id and not input_str:
		await event.edit("`Give a User id or Reply To a User Message To Mute.`")
		return	
	if event.reply_to_msg_id:
		msg = await event.get_reply_message()
		user_id = msg.from_id	
	else:
		user_id = int(input_str)	
	await event.edit("`Removing Duct Tape from User's Mouth.`")	
	try:
		muted.delete_one({'user_id':user_id})
		await event.edit("`Un-Gmuted` [{}](tg://user?id={}).".format(str(user_id),str(user_id)))
		logging.info("Un-Gmuted {}".format(str(user_id)))
	except Exception as e:
		logging.error(str(e))
		await event.edit("Error: "+str(e))

@borg.on(admin_cmd(pattern="listgmuted", allow_sudo=True))
async def list_gmuted(event):
	if event.fwd_from:
		return
	try:
		cur = muted.find({})
		msg = "**G-Muted Users:**\n"
		for c in cur:
			msg += "__User:__ `"+str(c['user_id'])+"`\n"
		await event.edit(msg)
	except Exception as e:
		logging.error(str(e))
		await event.edit("Error: "+str(e))	

@borg.on(events.NewMessage())      
async def gmute_listener(sender):			
	if MONGO_URI is None:
		return
	try:
		curs = muted.find({})
		for c in curs:
			if c['user_id'] == sender.from_id:
				await sender.delete()
	except:
		return 
			





