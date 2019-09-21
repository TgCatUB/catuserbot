import html
import asyncio
import random
from io import BytesIO
from traceback import format_exc
from telethon import utils, events, functions, types, errors
import .follow
try:
	from speedtest import Speedtest
	speedtest_enabled = True
except ImportError:
	speedtest_enabled = False
import . config
import . helper
import . strings
from . classes import flags

@helper.register(strings.cmd_help_text)
async def help_text(e):
	clients = e.pattern_match.group(1)
	if clients:
		clients = helper.give_client(helper.give_id(clients))
	else:
		clients = [e.client]
	for client in clients:
		text = helper.give_help(client)
		if config.help_as_file:
			await e.reply(file=helper.memory_file('help.txt', text))
		else:
			await e.reply(text, link_preview=False)

@helper.register(strings.cmd_deactivate, 10)
async def deactivate(e):
	await e.reply(strings.cmd_deactivate_respond)
	helper.active = False

@helper.register(strings.cmd_followers)
async def followers(e):
	await e.reply(await helper.list_followers())

@helper.register(strings.cmd_send, 20)
async def send(e):
	if e.pattern_match.group(1):
		clients = helper.give_client(helper.give_id(e.pattern_match.group(1)))
		if clients is None:
			await e.reply(strings.follow_who.format(e.pattern_match.group(1)))
			return
	else:
		clients = [e.client]
	chat = e.pattern_match.group(2)
	text = e.pattern_match.group(3)
	chat = helper.give_chat(chat, await e.get_chat())
	for client in clients:
		await client.send_message(chat, text)

@helper.register(strings.cmd_join, 30)
async def join(e):
	if e.pattern_match.group(1):
		clients = helper.give_client(helper.give_id(e.pattern_match.group(1)))
		if clients is None:
			await e.reply(strings.follow_who.format(e.pattern_match.group(1)))
			return
	else:
		clients = [e.client]
	chat = e.pattern_match.group(2)
	chat = helper.give_chat(chat, await e.get_chat())
	try:
		invite_info = utils.resolve_invite_link(chat)
	except Exception:
		invite_info = (None, None, None)
	for client in clients:
		if invite_info[0] is None:
			await client(functions.channels.JoinChannelRequest(chat))
		else:
			await client(functions.messages.ImportChatInviteRequest(chat))
		try:
			await e.reply(strings.cmd_join_respond)
		except Exception:
			pass

@helper.register(strings.cmd_leave, 30)
async def leave(e):
	if e.pattern_match.group(1):
		clients = helper.give_client(helper.give_id(e.pattern_match.group(1)))
		if clients is None:
			await e.reply(strings.follow_who.format(e.pattern_match.group(1)))
			return
	else:
		clients = [e.client]
	chat = e.pattern_match.group(2)
	chat = helper.give_chat(chat, await e.get_chat())
	try:
		invite_info = utils.resolve_invite_link(chat)
	except Exception:
		invite_info = (None, None, None)
	for client in clients:
		if invite_info[0] is None:
			await client(functions.channels.LeaveChannelRequest(chat))
		else:
			await client(functions.channels.LeaveChannelRequest(invite_info[1]))
		try:
			await e.reply(strings.cmd_leave_respond)
		except Exception:
			pass

@helper.register(strings.cmd_speedtest, 10)
async def speedtest(e):
	if not speedtest_enabled:
		await e.reply(strings.speedtest_disabled)
		return
	text = strings.cmd_speedtest_processing
	reply = await e.reply(text)
	speedtester = Speedtest()
	speedtester.download()
	text += strings.cmd_speedtest_upload
	try:
		await reply.edit(text)
	except Exception:
		pass
	speedtester.upload()
	url = speedtester.results.share()
	await reply.delete()
	await e.reply(strings.cmd_speedtest_respond.format(helper.blank_space, url))

@helper.register(strings.cmd_cli, 50)
async def cli(e):
	command = e.pattern_match.group(1)
	output = html.escape(helper.execute_cli(command))
	if output:
		await e.reply('<code>' + output + '</code>')
	else:
		await e.reply(strings.cmd_cli_respond)

@helper.register(strings.cmd_notes_add, 10)
async def notes_add(e):
	note = e.pattern_match.group(1)
	content = e.pattern_match.group(2)
	helper.db['notes'][note] = content
	if await helper.asave_db(e):
		await e.reply(strings.cmd_notes_add_respond)

@helper.register(strings.cmd_notes_remove, 10)
async def notes_remove(e):
	note = e.pattern_match.group(1)
	try:
		helper.db['notes'].pop(note)
	except KeyError:
		await e.reply(strings.cmd_notes_failed.format(note))
	else:
		if await helper.asave_db(e):
			await e.reply(strings.cmd_notes_remove_respond)

@helper.register(strings.cmd_notes)
async def notes(e):
	note = e.pattern_match.group(1)
	try:
		await e.reply(helper.db['notes'][note])
	except KeyError:
		await e.reply(strings.cmd_notes_failed.format(note))

@helper.register(strings.cmd_notes_list)
async def notes_list(e):
	n = ', '.join(helper.db['notes'].keys())
	await e.reply(strings.cmd_notes_list_respond.format(n))

@helper.register(strings.cmd_execnotes_add, 50)
async def execnotes_add(e):
	note = e.pattern_match.group(1)
	content = e.pattern_match.group(2)
	helper.db['execnotes'][note] = content
	if await helper.asave_db(e):
		await e.reply(strings.cmd_execnotes_add_respond)

@helper.register(strings.cmd_execnotes_remove, 50)
async def execnotes_remove(e):
	note = e.pattern_match.group(1)
	try:
		helper.db['execnotes'].pop(note)
	except KeyError:
		await e.reply(strings.cmd_execnotes_failed.format(note))
	else:
		if await helper.asave_db(e):
			await e.reply(strings.cmd_execnotes_remove_respond)

@helper.register(strings.cmd_execnotes)
async def execnotes(e):
	note = e.pattern_match.group(1)
	try:
		code = helper.db['execnotes'][note]
	except KeyError:
		await e.reply(strings.cmd_execnotes_failed.format(note))
	else:
#		This code is stolen from Twittie (https://t.me/twitface)
		exec(
			f'async def __ex(e, r, rr): ' +
			''.join(f'\n {l}'for l in code.split('\n'))
		)
		r = await e.reply(strings.cmd_execnotes_processing)
		ret = await locals()['__ex'](e, await e.get_reply_message(), r)
		text = strings.cmd_execnotes_respond
		if ret is not None:
			text = strings.cmd_execnotes_returned.format(html.escape(str(ret)))
		try:
			await r.edit(text)
		except errors.MessageIdInvalidError:
			pass

@helper.register(strings.cmd_execnotes_show)
async def execnotes_show(e):
	note = e.pattern_match.group(1)
	try:
		await e.reply('<code>' + helper.db['execnotes'][note] + '</code>')
	except KeyError:
		await e.reply(strings.cmd_execnotes_failed.format(note))

@helper.register(strings.cmd_execnotes_list)
async def execnotes_list(e):
	execn = ', '.join(helper.db['execnotes'].keys())
	await e.reply(strings.cmd_execnotes_list_respond.format(execn))

@helper.register(strings.cmd_restart, 10)
async def restart(e):
#	if not e.pattern_match.group(1):
	r = await e.reply(strings.cmd_restart_respond)
#	else:
#		r = await e.reply(strings.cmd_restart_restarted)
	for fwlr in helper.followers:
		if fwlr.client == e.client:
			helper.restart = [str(fwlr.identifier.int_id),
			str(e.chat_id), str(r.id)]
	if e.pattern_match.group(1):
		helper.restart = [['filler data', *helper.restart]]
	follow.mained = True
	helper.active = False

@helper.register(strings.cmd_exec_py, 50)
async def exec_py(e):
	code = e.pattern_match.group(1)
#	This code is stolen from Twittie (https://t.me/twitface)
	exec(
		f'async def __ex(e, r, rr): ' +
		''.join(f'\n {l}'for l in code.split('\n'))
	)
	r = await e.reply(strings.cmd_exec_py_processing)
	ret = await locals()['__ex'](e, await e.get_reply_message(), r)
	text = strings.cmd_exec_py_respond
	if ret is not None:
		text = strings.cmd_exec_py_returned.format(html.escape(str(ret)))
	try:
		await r.edit(text)
	except errors.MessageIdInvalidError:
		pass

@helper.register(strings.cmd_insult)
async def insult(e):
	await e.reply(helper.insult(e.pattern_match.group(1)))

@helper.register(strings.cmd_dcinfo)
async def dcinfo(e):
	if e.pattern_match.group(1):
		clients = helper.give_client(helper.give_id(e.pattern_match.group(1)))
		if not clients:
			await e.reply(strings.follow_who.format(e.pattern_match.group(1)))
			return
	else:
		clients = [e.client]
	for client in clients:
		await e.reply('<code>' +
		(await client(functions.help.GetNearestDcRequest())).stringify() +
		'</code>')

@helper.register(strings.cmd_cas)
async def cas(e):
	r = await e.reply(strings.cmd_cas_processing)
	await r.edit(await helper.check_cas(e.client.loop, e.pattern_match.group(1)))

@helper.register(strings.cmd_afk)
async def afk(e):
	helper.afk = e.pattern_match.group(1)
	await e.reply(strings.cmd_afk_respond)

@helper.register(strings.cmd_unafk)
async def unafk(e):
	helper.afk = None
	helper.afk_responses = dict()
	await e.reply(strings.cmd_unafk_respond)

@helper.register(events.NewMessage(incoming=True))
async def respond_to_afk(e):
	if (e.is_private or e.mentioned) and helper.afk:
		try:
			times = helper.afk_responses[e.chat_id]
		except KeyError:
			times = 0
			helper.afk_responses[e.chat_id] = times
		if not times % 5:
			helper.afk_responses[e.chat_id] += 1
			user = await e.get_sender()
			if user.verified or user.bot:
				return
			await e.reply(strings.im_afk.format(helper.afk))

@helper.register(events.NewMessage(incoming=True), flags=flags(True, crawler=True))
@helper.register(events.MessageEdited(incoming=True), flags=flags(True, crawler=True))
async def crawler(e):
	pattern_match = helper.invite_re.findall(e.text)
	for invite in set(pattern_match):
		inv_info = utils.resolve_invite_link(invite)
		if inv_info[1]:
			try:
				chat_info = await e.client(functions.messages.CheckChatInviteRequest(invite))
				if isinstance(chat_info, (types.ChatInviteAlready, types.ChatInvite)):
					await asyncio.sleep(random.randint(0, 10))
					await e.client(functions.messages.ImportChatInviteRequest(invite))
					await e.client.send_message(config.log_chat, strings.crawler_joined.format(invite=invite,
					user=await e.get_sender(), e=e,
					sanitised_cid=str(e.chat_id)[4:]))
			except errors.UserAlreadyParticipantError:
				pass
			except Exception:
				fyle = BytesIO()
				fyle.name = 'exception.txt'
				fyle.write(bytes(format_exc(), 'utf-8'))
				fyle.seek(0)
				await e.client.send_message(config.log_chat, strings.crawler_failed.format(invite=invite),
				file=fyle)

@helper.register(strings.cmd_json)
async def json(e):
	r = await e.get_reply_message()
	if not r:
		r = e
	js = r.to_json()
	await e.reply('<code>' +
	html.escape(str(helper.traverse_json(js, e.pattern_match.group(1)))) +
	'</code>')

@helper.register(events.NewMessage(incoming=True), flags=flags(True, lydia=True))
async def lydia_respond(e):
	if not e.is_private:
		return
	if e.from_id in helper.db['nolydia']:
		return
	if not helper.coffeehouse_enabled:
		return
	if e.from_id in helper.lydia_rate:
		return
	helper.lydia_rate.add(e.from_id)
	chat = await e.get_sender()
	if chat.verified or chat.bot:
		return
	async with e.client.action(e.chat_id, 'typing'):
		session = await helper.give_lydia_session(e.client.loop, e.chat_id)
		respond = await helper.lydia_think(e.client.loop, session, e.text)
		# If lydia is disabled while it's processing,
		if e.from_id in helper.db['nolydia']:
			helper.lydia_rate.remove(e.from_id)
			return
		await e.respond(html.escape(respond), reply_to=None if not e.is_reply else e.id)
	helper.lydia_rate.remove(e.from_id)

@helper.register(strings.cmd_info)
async def info(e):
	async def afc(fwlr):
		if await fwlr.online():
			afc.fwlr_count += 1
	afc.fwlr_count = 0
	await asyncio.wait([
		afc(fwlr)
		for fwlr in helper.followers
	])
	me = await helper.give_self_id(e)
	for f in helper.followers:
		if f.me.id == me:
			fwlr = f
	await e.reply(strings.cmd_info_respond.format(
	fwlr_count=afc.fwlr_count, fwlr=fwlr, source=strings.source,
	message_count=len(helper.messages)), link_preview=False)

@helper.register(strings.cmd_lydia_enable)
async def lydia_enable(e):
	if not config.lydia_api or not helper.coffeehouse_enabled:
		await e.reply(strings.no_lydia)
		return
	r = await e.get_reply_message()
	if r:
		user = r.from_id
	else:
		user = e.pattern_match.group(1)
		if not user:
			if not e.is_private:
				await e.reply(strings.user_required)
				return
			user = e.chat_id
		else:
			user = await helper.give_user_id(user, e.client)
	if user in helper.db['nolydia']:
		helper.db['nolydia'].remove(user)
		if await helper.asave_db(e):
			await e.reply(strings.cmd_lydia_enable_respond)
	else:
		await e.reply(strings.cmd_lydia_enable_already)

@helper.register(strings.cmd_lydia_disable)
async def lydia_disable(e):
	if not config.lydia_api or not helper.coffeehouse_enabled:
		await e.reply(strings.no_lydia)
		return
	r = await e.get_reply_message()
	if r:
		user = r.from_id
	else:
		user = e.pattern_match.group(1)
		if not user:
			if not e.is_private:
				await e.reply(strings.user_required)
				return
			user = e.chat_id
		else:
			user = await helper.give_user_id(user, e.client)
	if user not in helper.db['nolydia']:
		helper.db['nolydia'].append(user)
		if await helper.asave_db(e):
			await e.reply(strings.cmd_lydia_disable_respond)
	else:
		await e.reply(strings.cmd_lydia_disable_already)

@helper.register(events.NewMessage(pattern=strings.cmd_admin_report, incoming=True),
flags=flags(True, adminreport=True, noerr=True))
@helper.register(events.MessageEdited(pattern=strings.cmd_admin_report, incoming=True),
flags=flags(True, adminreport=True, noerr=True))
async def admin_report(e):
	if e.is_private:
		return
	if e.chat_id == config.log_chat:
#		No recursion please
		return
	reporter = await e.get_sender()
	chat = await e.get_chat()
	if not chat.username:
		unmark_cid = await e.client.get_peer_id(chat.id, False)
		link = f'https://t.me/c/{unmark_cid}/{e.id}'
	else:
		link = f'https://t.me/{chat.username}/{e.id}'
	if e.is_reply:
		r = await e.get_reply_message()
		reportee = await r.get_sender()

		await e.client.send_message(config.log_chat, strings.admin_report.format(
		reporter=reporter, reportee=reportee, chat=chat, e=e, r=r,
		remark=html.escape(str(e.text)), link=link,
		reported_message=html.escape(str(r.text))),
		link_preview=False)
	else:
		await e.client.send_message(config.log_chat, strings.admin_report_no_reportee.format(
		reporter=reporter, chat=chat, e=e, remark=html.escape(str(e.text)),
		link=link), link_preview=False)

@helper.register(strings.cmd_brief)
async def brief(e):
	time = e.pattern_match.group(1)
	time = float(time if time else 1)
	content = e.pattern_match.group(2)
	await e.edit(content)
	await asyncio.sleep(time)
	await e.delete()

@helper.register(events.NewMessage(), flags=flags(True, msgcount=True, noerr=True))
async def message_counter(e):
	helper.messages.add((e.chat_id, e.id))

@helper.register(strings.cmd_ignore_enable)
async def ignore_enable(e):
	r = await e.get_reply_message()
	if r:
		user = r.from_id
	else:
		user = e.pattern_match.group(1)
		if not user:
			if not e.is_private:
				await e.reply(strings.user_required)
				return
			user = e.chat_id
		else:
			user = await helper.give_user_id(user, e.client)
	if user not in helper.db['ignored']:
		helper.db['ignored'].append(user)
		if await helper.asave_db(e):
			await e.reply(strings.cmd_ignore_enable_respond)
	else:
		await e.reply(strings.cmd_ignore_enable_already)

@helper.register(strings.cmd_ignore_disable)
async def ignore_disable(e):
	r = await e.get_reply_message()
	if r:
		user = r.from_id
	else:
		user = e.pattern_match.group(1)
		if not user:
			if not e.is_private:
				await e.reply(strings.user_required)
				return
			user = e.chat_id
		else:
			user = await helper.give_user_id(user, e.client)
	if user in helper.db['ignored']:
		helper.db['ignored'].remove(user)
		if await helper.asave_db(e):
			await e.reply(strings.cmd_ignore_disable_respond)
	else:
		await e.reply(strings.cmd_ignore_disable_already)

@helper.register(events.NewMessage(incoming=True), flags=flags(True, ignore=True))
async def ignore(e):
	if e.is_private or e.mentioned:
		if e.from_id in helper.db['ignored']:
			await e.client.send_read_acknowledge(e.chat_id, e, clear_mentions=True)

@helper.register(events.NewMessage(incoming=True), flags=flags(True, flydia=True))
async def flydia_respond(e):
	if e.is_private or not helper.coffeehouse_enabled or not e.mentioned:
		return
	if e.from_id not in helper.db['flydia']:
		return
	if e.from_id in helper.lydia_rate:
		return
	helper.lydia_rate.add(e.from_id)
	chat = await e.get_sender()
	if chat.verified or chat.bot:
		return
	async with e.client.action(e.chat_id, 'typing'):
		session = await helper.give_lydia_session(e.client.loop, e.chat_id)
		respond = await helper.lydia_think(e.client.loop, session, e.text)
		# If lydia is disabled in groups while it's processing,
		if e.from_id not in helper.db['flydia']:
			helper.lydia_rate.remove(e.from_id)
			return
		await e.respond(html.escape(respond), reply_to=None if not e.is_reply else e.id)
	helper.lydia_rate.remove(e.from_id)

@helper.register(strings.cmd_flydia_enable)
async def flydia_enable(e):
	if not config.lydia_api or not helper.coffeehouse_enabled:
		await e.reply(strings.no_lydia)
		return
	r = await e.get_reply_message()
	if r:
		user = r.from_id
	else:
		user = e.pattern_match.group(1)
		if not user:
			await e.reply(strings.user_required)
			return
		user = await helper.give_user_id(user, e.client)
	if user not in helper.db['flydia']:
		helper.db['flydia'].append(user)
		if await helper.asave_db(e):
			await e.reply(strings.cmd_flydia_enable_respond)
	else:
		await e.reply(strings.cmd_flydia_enable_already)

@helper.register(strings.cmd_flydia_disable)
async def flydia_disable(e):
	if not config.lydia_api or not helper.coffeehouse_enabled:
		await e.reply(strings.no_lydia)
		return
	r = await e.get_reply_message()
	if r:
		user = r.from_id
	else:
		user = e.pattern_match.group(1)
		if not user:
			await e.reply(strings.user_required)
			return
		user = await helper.give_user_id(user, e.client)
	if user in helper.db['flydia']:
		helper.db['flydia'].remove(user)
		if await helper.asave_db(e):
			await e.reply(strings.cmd_flydia_disable_respond)
	else:
		await e.reply(strings.cmd_flydia_disable_already)

@helper.register(strings.cmd_read, 10)
async def read_messages(e):
	quick = e.pattern_match.group(1)
	chat = helper.give_chat(e.pattern_match.group(3), await e.get_chat())
	clients = e.pattern_match.group(2)
	if clients:
		clients = helper.give_client(helper.give_id(clients))
		if not clients:
			await e.reply(strings.follow_who.format(e.pattern_match.group(1)))
			return
	else:
		clients = [e.client]
	async def _read_messages(client, chat):
		await client.send_read_acknowledge(chat, clear_mentions=True)
	if quick:
		await asyncio.wait([
			_read_messages(client, chat)
			for client in clients
		])
		await e.reply(strings.cmd_read_respond)
	else:
		for client in clients:
			await _read_messages(client, chat)
			await e.reply(strings.cmd_read_respond)
