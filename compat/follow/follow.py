import asyncio
import logging
import sys
import os
import importlib
import .commands
from userbot import bot
import .strings
import .helper
import config
import .classes
logging.basicConfig(
format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
level=logging.INFO)

clients = logging.getLogger('clients')

async def quick_restart():
	logging.info('Restarting strings')
	importlib.reload(strings)
	logging.info('Restarting classes')
	importlib.reload(classes)
	logging.info('Restarting helper')
	config.dont_cron = True
	res_info = helper.restart[0]
	importlib.reload(helper)
#	async def async_disabled():
#		pass
#	helper.show_restarted = async_disabled
	helper.restart = [*res_info]
	class disabled:
		def __init__(self):
			pass

		def start(self):
			pass
	helper.auto_recover = disabled()
	logging.info('Restarting config')
	importlib.reload(config)
	logging.info('Restarting commands')
	importlib.reload(commands)
	logging.info('Calling main again')
	await main()

async def main():
	helper.auto_recover.start()
	async def new_client(identify):
		identifier = identify[1]
		clients.info('Loading client %s', identifier.name)

		bot.parse_mode = 'html'

		your_trust = identifier.trust
		for handler in helper.raw_handlers:
			if your_trust >= handler[0].__trust__:
				if identifier.flags.compare(handler[0].flags):
					for e in handler[1]:
						client.add_event_handler(handler[0], e)

		me = await client.get_me()
		helper.followers.append(classes.follower(identifier, bot, me, identify[0]))
	await asyncio.wait([
		new_client(i)
		for i in enumerate(config.followers)
	])

	logging.info('Online!')

	messy_followers = [[fwlr.enu, fwlr] for fwlr in helper.followers]
	helper.followers = [i[1] for i in sorted(messy_followers)]
	handlers = []
	for handler in helper.handlers:
		handlers.append(handler.__name__)

	helper.modules.info('Handlers:\n%s', ', '.join(handlers))
	helper.check_db_ver()
	await helper.show_restarted()
	while helper.active:
		await asyncio.sleep(1)

	await asyncio.wait([
		fwlr.disconnect()
		for fwlr in helper.followers
	])

	if helper.restart:
		if len(helper.restart) == 1:
			await quick_restart()
		else:
			os.execl(sys.executable, sys.executable, sys.argv[0],
			*helper.restart)

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	try:
		loop.run_until_complete(main())
	except KeyboardInterrupt:
		print()
