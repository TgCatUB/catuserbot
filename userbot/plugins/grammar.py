import requests
from userbot import catub

from ..core.managers import edit_delete, edit_or_reply

plugin_category = "extra"


@catub.cat_cmd(
    pattern="gcheck$",
    command=("gcheck", plugin_category),
    info={
        "header": "To Correct The grammar Of A Paragraph If It Has Any Error.",
        "description": "Reply to any English paragraph to correct its grammar",
        "usage": "{tr}gcheck reply",
    },
)
async def grammer(event):
    "To Correct The Grammar Of A Paragraph If It Has Any Error."
    re_message = await event.get_reply_message()
    if not re_message or not re_message.raw_text:
        return await edit_delete(
            event, "__Reply to a message to correct grammar in that message.__", 7
        )
    url = "https://orthographe.reverso.net/api/v1/Spelling"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
    }
    data = {
        "autoReplace": "true",
        "generateRecommendations": "false",
        "generateSynonyms": "false",
        "getCorrectionDetails": "true",
        "interfaceLanguage": "en",
        "language": "eng",
        "locale": "Indifferent",
        "origin": "interactive",
        "text": re_message.raw_text,
    }
    response = requests.get(url, headers=headers, params=data)
    wrongs = response.json()["corrections"]
    result = re_message.raw_text
    for wrong in wrongs[::-1]:
        start = wrong["startIndex"]
        end = wrong["endIndex"] + 1
        correction = wrong["correctionText"]
        result = result[:start] + "**" + correction + "**" + result[end:]
    if result != re_message.raw_text:
        return await edit_or_reply(event, result)
    await edit_delete(event, "__There is no grammer mistake in the replied text.__", 7)
