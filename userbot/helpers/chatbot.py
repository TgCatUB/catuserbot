# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import json
import os

import openai
import requests
from fake_useragent import UserAgent

from userbot.Config import Config
from userbot.core.managers import edit_delete, edit_or_reply
from userbot.helpers.functions import format_image, wall_download
from userbot.sql_helper.globals import gvarstatus

openai.api_key = Config.OPENAI_API_KEY
conversations = {}


def generate_gpt_response(input_text, chat_id):
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
        generated_text = f"`Error generating GPT response: {str(e)}`"
    return generated_text


def generate_edited_response(input_text, instructions):
    try:
        response = openai.Edit.create(
            model="text-davinci-edit-001",
            input=input_text,
            instruction=instructions,
        )
        edited_text = response.choices[0].text.strip()
    except Exception as e:
        edited_text = f"__Error generating GPT edited response:__ `{str(e)}`"
    return edited_text


def del_convo(chat_id, checker=False):
    global conversations
    out_text = "__There is no GPT context to delete for this chat.__"
    # Delete the the context of given chat
    if chat_id in conversations:
        del conversations[chat_id]
        out_text = "__GPT context deleted for this chat.__"
    if checker:
        return out_text


async def generate_dalle_image(text, reply, event, flag=None):
    size = gvarstatus("DALLE_SIZE") or "1024"
    limit = int(gvarstatus("DALLE_LIMIT") or "1")
    if not text and reply:
        text = reply.text
    if not text:
        return await edit_delete(event, "**ಠ∀ಠ Gimmi text**")

    catevent = await edit_or_reply(event, "__Generating image...__")
    try:
        if flag:
            filename = "dalle-in.png"
            await event.client.download_media(reply, filename)
            format_image(filename)
            if flag == "e":
                response = openai.Image.create_edit(
                    image=open(filename, "rb"),
                    prompt=text,
                    n=limit,
                    size=f"{size}x{size}",
                )
            elif flag == "v":
                response = openai.Image.create_variation(
                    image=open(filename, "rb"),
                    n=limit,
                    size=f"{size}x{size}",
                )
            os.remove(filename)
        else:
            response = openai.Image.create(
                prompt=text,
                n=limit,
                size=f"{size}x{size}",
            )
    except Exception as e:
        await edit_delete(catevent, f"Error generating image: {str(e)}")
        return None, None

    photos = []
    captions = []
    for i, media in enumerate(response["data"], 1):
        photo = await wall_download(media["url"], "Dall-E")
        photos.append(photo)
        captions.append("")
        await edit_or_reply(catevent, f"__📥 Downloaded : {i}/{limit}__")

    captions[-1] = f"**➥ Query :-** `{text.title()}`"
    await edit_or_reply(catevent, "__Uploading...__")
    return photos, captions


class ThabAi:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            "authority": "chatbot.theb.ai",
            "content-type": "application/json",
            "origin": "https://chatbot.theb.ai",
            "user-agent": UserAgent().random,
        }

    def get_response(self, prompt: str) -> str:
        response = self.session.post(
            "https://chatbot.theb.ai/api/chat-process",
            json={"prompt": prompt, "options": {}},
            stream=True,
        )
        response.raise_for_status()
        response_lines = response.iter_lines()
        response_data = ""
        for line in response_lines:
            if line:
                data = json.loads(line)
                if "utterances" in data:
                    response_data += " ".join(
                        utterance["text"] for utterance in data["utterances"]
                    )
                elif "delta" in data:
                    response_data += data["delta"]
        return response_data
