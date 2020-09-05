import re
from telethon import custom, events

if Var.TG_BOT_USER_NAME_BF_HER is not None and tgbot is not None:
    @tgbot.on(events.InlineQuery)
    async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text
        if event.query.user_id == bot.uid and query.startswith("Secret bot"):
            query = query[10:]
            txt = re.findall(r'(\d+) ?(.*)', query)
            buttons = [
                custom.Button.inline(
                    "show message 🔐",
                    data=f"secret_{txt[0][0]}_ {txt[0][1]}")]
            result = builder.article(
                title="secret message",
                text=f"🔒 A whisper message to [user](tg://user?id={txt[0][0]}), Only he / she can open it.",
                buttons=buttons)
            await event.answer([result] if result else None)

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"secret_(.+?)_(.+)")))
    async def on_plug_in_callback_query_handler(event):
        userid = event.pattern_match.group(1)
        if int(userid) != event.query.user_id:
            await event.answer("You are not allowed to see this.", cache_time=0, alert=True)
            return
        encrypted_text = event.pattern_match.group(2)
        reply_pop_up_alert = encrypted_text
        await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
