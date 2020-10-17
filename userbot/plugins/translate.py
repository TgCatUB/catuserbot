""" Google Translate
Available Commands:
.tr LanguageCode as reply to a message
.tr LangaugeCode | text to translate"""

from googletrans import LANGUAGES, Translator

from .. import CMD_HELP
from ..utils import admin_cmd, edit_or_reply, sudo_cmd
from . import BOTLOG, BOTLOG_CHATID, deEmojify

TTS_LANG = "en"
TRT_LANG = "en"
langi = "en"


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


@bot.on(admin_cmd(outgoing=True, pattern=r"trt(?: |$)([\s\S]*)"))
@bot.on(sudo_cmd(allow_sudo=True, pattern=r"trt(?: |$)([\s\S]*)"))
async def translateme(trans):
    """ For .trt command, translate the given text using Google Translate. """
    translator = Translator()
    textx = await trans.get_reply_message()
    message = trans.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await edit_or_reply(trans, "`Give a text or reply to a message to translate!`")
        return
    try:
        reply_text = translator.translate(deEmojify(message), dest=TRT_LANG)
    except ValueError:
        await edit_or_reply(trans, "Invalid destination language.")
        return
    source_lan = LANGUAGES[f"{reply_text.src.lower()}"]
    transl_lan = LANGUAGES[f"{reply_text.dest.lower()}"]
    reply_text = f"**From** __{source_lan.title()}__\n**To **__{transl_lan.title()}__**:**\n\n`{reply_text.text}``"

    await edit_or_reply(trans, reply_text)
    if BOTLOG:
        await trans.client.send_message(
            BOTLOG_CHATID,
            f"Translated some {source_lan.title()} stuff to {transl_lan.title()} just now.",
        )


@bot.on(admin_cmd(pattern="lang trt (.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="lang trt (.*)", allow_sudo=True))
async def lang(value):
    # For .lang command, change the default langauge of userbot scrapers.
    scraper = "Translator"
    global TRT_LANG
    arg = value.pattern_match.group(1).lower()
    if arg in LANGUAGES:
        TRT_LANG = arg
        LANG = LANGUAGES[arg]
    else:
        await edit_or_reply(
            value,
            f"`Invalid Language code !!`\n`Available language codes for TRT`:\n\n`{LANGUAGES}`",
        )
        return
    await edit_or_reply(value, f"`Language for {scraper} changed to {LANG.title()}.`")
    if BOTLOG:
        await value.client.send_message(
            BOTLOG_CHATID, f"`Language for {scraper} changed to {LANG.title()}.`"
        )


CMD_HELP.update(
    {
        "translate": "**Plugin :** `translate`\
         \n\n**Syntax : **`.tl` LanguageCode as reply to a message\
         \n**Function : **.tl LangaugeCode | text to translate\
         \n**Example :** `.tl hi`\
         \n\n**Syntax : **`.trt Reply to a message`/`.trt message`\
         \n**Function : **__It will translate your messege__\
         \n\n**Syntax : **`.lang trt LanguageCode`\
         \n**Function : **__It will set default langaugeCode for **trt**__\
        "
    }
)
