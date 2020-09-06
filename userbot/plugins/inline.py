# thanks to @null7410  for callbackquery code
# created by @sandy1709 and @mrconfused
from telethon import custom, events
import re

if Var.TG_BOT_USER_NAME_BF_HER is not None and tgbot is not None:
    @tgbot.on(events.InlineQuery)
    async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text
        hmm = re.compile("secret (.*) (.*)")
        match = re.findall(hmm, query)
        if event.query.user_id == bot.uid and match:
            query = query[7:]
            user, txct = query.split(" ", 1)
            try:
                # ValueError: Could not find the input entity for
                # <telethon.tl.types.PeerUser object at 0x7f96e090dac0>. Please
                # read
                # https://docs.telethon.dev/en/latest/concepts/entities.html to
                # find out more detail
                u = int(user)
                buttons = [custom.Button.inline(
                    "show message 🔐",
                    data=f"secret_{u}_ {txct}")]
                try:
                    u = await event.client.get_entity(user)
                    if:
                        sandy = f"@{u.username}"
                    else:
                        sandy = f"[{u.first_name}](tg://user?id={u.id})"
                except ValueError:
                    sandy = f"[{user}](tg://user?id={u})"
                result = builder.article(
                    title="secret message",
                    text=f"🔒 A whisper message to {sandy}, Only he/she can open it.",
                    buttons=buttons)
                await event.answer([result] if result else None)
            except ValueError:
                u = await event.client.get_entity(user)
                buttons = [custom.Button.inline(
                    "show message 🔐",
                    data=f"secret_{u.id}_ {txct}")]
                if u.username:
                    sandy = f"@{u.username}"
                else:
                    sandy = f"[{u.first_name}](tg://user?id={u.id})"
                result = builder.article(
                    title="secret message",
                    text=f"🔒 A whisper message to {sandy}, Only he/she can open it.",
                    buttons=buttons)
                await event.answer([result] if result else None)
