from telethon.events import NewMessage
from bwb import bwb
import asyncio

bwb = bwb.bwb(bot.uid)
wrap_users = {
    't': 79316791,   # Tanner
    'j': 172033414,  # Jason
    'o': 358491576,  # Jonas
    'm': 964048273,  # Mini Eule
    'g': 234480941,  # Twit
    'v': 181585055,  # Viktor
}


@command(outgoing=True, pattern='!!+init')
async def init(event):
    await event.respond('000000init ' + bwb.init())


@command(outgoing=True, pattern=r'!!+(e(?:enc)?)?w(?:rap)? (\S+) ([\s\S]+)')
async def wrap(event):
    enc = event.pattern_match.group(1) is not None
    message = event.pattern_match.group(3)

    u = event.pattern_match.group(2).lower()
    if u.isdigit():
        u = int(u)
    else:
        u = wrap_users.get(u, None)

    await event.respond(bwb.wrap(message, target=u, enc=enc), reply_to=event.reply_to_msg_id)


@bot.on(NewMessage())
async def hs(event):
    text = bwb.parse(event.raw_text)
    handshake_auth = False

    if text.startswith('000000'):
        pass
    elif bwb.check_auth(text, handshake=True):
        handshake_auth = True
    elif bwb.check_auth(text):
        auth = True
    else:
        return

    if ' ' in text:
        command, data = text[6:].split(maxsplit=1)
    else:
        command, data = text[6:], None

    if command == 'init' and data:
        await event.respond('000000handshake ' + bwb.handshake(data))
    elif command == 'handshake' and data:
        await event.respond(bwb.wrap('secret ' + bwb.secret(data), handshake=True))
    elif handshake_auth and command == 'secret' and data:
        bwb.set_secret(data)
        await event.respond(bwb.wrap('🤝'))
    elif auth:
        command = command.lower()
        if command == '🤝':
            await asyncio.sleep(1)
            await event.respond('🤝')
        elif command == 'ping':
            await event.reply('Pong!') 
