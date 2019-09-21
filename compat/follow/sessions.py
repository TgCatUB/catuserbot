import asyncio
import logging
from userbot import bot
import . config
logging.basicConfig(
format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
level=logging.INFO)

clients = logging.getLogger('clients')

async def main():
	if not config.followers:
		logging.error('Please edit the config')
		exit(1)
	fwlrs = []
	for i in config.followers:
		bot.info('Testing client %s, if it asks for your phone number please login', i.name)
		await bot.start()
		fwlrs.append(bot)
	await asyncio.wait([
		.disconnect()
		for client in fwlrs
	])

