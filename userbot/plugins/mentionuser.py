"""Mention/Tag Replied Users\n
`.men` <text>
"""
# By: @INF1N17Y

import html
from userbot.utils import admin_cmd


@borg.on(admin_cmd(pattern="men (.*)"))
async def _(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        input_str = event.pattern_match.group(1)
        reply_msg = await event.get_reply_message()
        caption = """<a href='tg://user?id={}'>{}</a>""".format(reply_msg.from_id, input_str)
        await event.delete()
        await borg.send_message(event.chat_id, caption, parse_mode="HTML")
    else:
        await event.edit("Reply to user with `.mention <your text>`")
