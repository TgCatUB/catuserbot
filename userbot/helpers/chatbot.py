#  \\   https://github.com/TgCatUB/catuserbot  //
#   \\         Plugin for @catuserbot         //
#     ````````````````````````````````````````

import os
import re

import openai
from PIL import Image, ImageFilter
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest as unblock

from userbot import catub
from userbot.Config import Config
from userbot.core.managers import edit_delete, edit_or_reply
from userbot.helpers.functions import delete_conv, wall_download
from userbot.sql_helper.globals import addgvar, gvarstatus

openai.api_key = Config.OPENAI_API_KEY
conversations = {}


async def generate_gpt_response(input_text, chat_id):
    global conversations
    model = gvarstatus("CHAT_MODEL") or "gpt-3.5-turbo"
    system_message = gvarstatus("SYSTEM_MESSAGE") or None
    messages = conversations.get(chat_id, [])

    # Add system message if it exists
    if system_message and not messages:
        messages.append({"role": "system", "content": system_message})

    # Add the new user message
    messages.append({"role": "user", "content": input_text})
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
        )
        generated_text = response.choices[0].message.content.strip()

        # Save the assistant's response to the conversation history
        messages.append({"role": "assistant", "content": generated_text})
        conversations[chat_id] = messages
    except Exception as e:
        generated_text = f"`Error generating GPT response: {e}`"
    return generated_text


def del_convo(chat_id, checker=False):
    global conversations
    out_text = "__There is no GPT context to delete for this chat.__"
    # Delete the the context of given chat
    if chat_id in conversations:
        del conversations[chat_id]
        out_text = "__GPT context deleted for this chat.__"
    if checker:
        return out_text


def format_image(filename):
    img = Image.open(filename).convert("RGBA")
    w, h = img.size
    if w != h:
        _min, _max = min(w, h), max(w, h)
        bg = img.crop(
            ((w - _min) // 2, (h - _min) // 2, (w + _min) // 2, (h + _min) // 2)
        )
        bg = bg.filter(ImageFilter.GaussianBlur(5))
        bg = bg.resize((_max, _max))
        img_new = Image.new("RGBA", (_max, _max), (255, 255, 255, 0))
        img_new.paste(
            bg, ((img_new.width - bg.width) // 2, (img_new.height - bg.height) // 2)
        )
        img_new.paste(img, ((img_new.width - w) // 2, (img_new.height - h) // 2))
        img = img_new
    img.save(filename)


async def generate_dalle_image(text, reply, event, flag=None):
    size = gvarstatus("DALLE_SIZE") or "1024"
    limit = gvarstatus("DALLE_LIMIT") or "1"
    if not text and reply:
        text = reply.text
    if not text:
        return await edit_delete(event, "**ಠ∀ಠ Gimmi text**")

    await edit_or_reply(event, "__Generating image...__")
    try:
        if flag:
            filename = "dalle-in.png"
            await event.client.download_media(reply, filename)
            format_image(filename)
            if flag == "e":
                response = openai.Image.create_edit(
                    image=open(filename, "rb"),
                    prompt=text,
                    n=int(limit),
                    size=f"{size}x{size}",
                )
            elif flag == "v":
                response = openai.Image.create_variation(
                    image=open(filename, "rb"),
                    n=int(limit),
                    size=f"{size}x{size}",
                )
            os.remove(filename)
        else:
            response = openai.Image.create(
                prompt=text,
                n=int(limit),
                size=f"{size}x{size}",
            )
    except Exception as e:
        return await edit_delete(event, f"Error generating image: {e}")

    photos = []
    captions = []
    for i, media in enumerate(response["data"], 1):
        photo = await wall_download(media["url"], "Dall-E")
        photos.append(photo)
        captions.append("")
        await edit_or_reply(event, f"__📥 Downloaded : {i}/{limit}__")

    captions[-1] = f"**➥ Query :-** `{text.title()}`"
    return photos, captions


async def ai_api(event):
    token = gvarstatus("AI_API_TOKEN") or None
    if not token:
        chat = "@Kukichatbot"
        token = "5381629779-KUKIdn8kLJ5Ln0"
        async with event.client.conversation(chat) as conv:
            try:
                purgeflag = await conv.send_message("/start")
            except YouBlockedUserError:
                await catub(unblock("Kukichatbot"))
                purgeflag = await conv.send_message("/start")
            await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
            await conv.send_message("/token")
            respond = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
            await delete_conv(event, chat, purgeflag)
            if rgxtoken := re.search(r"(?:API: )(.+)(?: Do)", respond.message):
                token = rgxtoken[1]
            addgvar("AI_API_TOKEN", token)
    return token
