""" Google Translate
Available Commands:
.tr LanguageCode as reply to a message
.tr LangaugeCode | text to translate"""

from googletrans import Translator

from .. import CMD_HELP
from ..utils import admin_cmd, edit_or_reply, sudo_cmd
from . import deEmojify


@borg.on(admin_cmd(pattern="tl ?(.*)"))
@borg.on(sudo_cmd(pattern="tl ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if "trim" in event.raw_text:
        # https://t.me/c/1220993104/192075
        return
    input_str = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lan = input_str or "ml"
    elif "|" in input_str:
        lan, text = input_str.split("|")
    else:
        await edit_or_reply(event, "`.tl LanguageCode` as reply to a message")
        return
    text = deEmojify(text.strip())
    lan = lan.strip()
    translator = Translator()
    try:
        translated = translator.translate(text, dest=lan)
        after_tr_text = translated.text
        # TODO: emojify the :
        # either here, or before translation
        output_str = """**TRANSLATED** from {} to {}
{}""".format(
            translated.src, lan, after_tr_text
        )
        await edit_or_reply(event, output_str)
    except Exception as exc:
        await edit_or_reply(event, str(exc))


CMD_HELP.update(
    {
        "translate": "**Plugin :** `translate`\
         \n\nAvailable Commands:\
         \n.tl LanguageCode as reply to a message\
         \n.tl LangaugeCode | text to translate\
        "
    }
)
