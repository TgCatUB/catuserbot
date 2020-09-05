import re
from telethon import custom, events

if Var.TG_BOT_USER_NAME_BF_HER is not None and tgbot is not None:
    @tgbot.on(events.InlineQuery)  # pylint:disable=E0602
    async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text
        if event.query.user_id == bot.uid and query.startswith("Secret bot"):
            query = query[10:]
            txt = re.findall(r'(\d+) ?(.*)', query)
            text = txt[0][1]
            id = []
            id.append(txt[0][0])
            id.append(bot.uid)
            buttons = [custom.Button.inline("show message 🔐", data="secert")]
            result = builder.article(
                title="secret message",
                text=f"🔒 A whisper message to [user](tg://user?id={txt[0][0]}), Only he / she can open it.",
                buttons=buttons)
            await event.answer([result] if result else None)
