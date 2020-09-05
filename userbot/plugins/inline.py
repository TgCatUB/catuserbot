# thanks to @null7410  for callbackquery code
# created by @sandy1709 and @mrconfused
from telethon import custom, events

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
                u = await event.client.get_entity(user)
            except ValueError:
                u = await event.client.get_entity(int(user))
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
