# imported from pornhub credits to pornhub
import asyncio
import io
from time import time

from coffeehouse.api import API
from coffeehouse.lydia import LydiaAI

from ..utils import admin_cmd, edit_or_reply, sudo_cmd
from . import CMD_HELP
from .sql_helper.lydia_ai_sql import add_s, get_all_s, get_s, remove_s

if Var.LYDIA_API_KEY:
    api_key = Var.LYDIA_API_KEY
    # Create the coffeehouse API
    coffeehouse_api = API(api_key)
    # Create Lydia instance
    lydia = LydiaAI(coffeehouse_api)


@bot.on(admin_cmd(pattern="(en|re|li)ai"))
@bot.on(sudo_cmd(pattern="(en|re|li)ai", allow_sudo=True))
async def lydia_disable_enable(event):
    if event.fwd_from:
        return
    if Var.LYDIA_API_KEY is None:
        await edit_or_reply(event, "Please add required `LYDIA_API_KEY` env var")
        return
    if event.reply_to_msg_id is not None:
        input_str = event.pattern_match.group(1)
        reply_msg = await event.get_reply_message()
        user_id = reply_msg.from_id
        chat_id = event.chat_id
        catevent = await edit_or_reply(event, "Processing...")
        if input_str == "en":
            # Create a new chat session (Like a conversation)
            session = lydia.create_session()
            logger.info(session)
            # logger.info("Session ID: {0}".format(session.id))
            # logger.info("Session Available: {0}".format(str(session.available)))
            # logger.info("Session Language: {0}".format(str(session.language)))
            # logger.info("Session Expires: {0}".format(str(session.expires)))
            logger.info(add_s(user_id, chat_id, session.id, session.expires))
            await catevent.edit(f"Hello")
        elif input_str == "re":
            logger.info(remove_s(user_id, chat_id))
            await catevent.edit(f"[__signal lost__](tg://user?id={user_id})")
        elif input_str == "li":
            lsts = get_all_s()
            if len(lsts) > 0:
                output_str = "AI enabled users:\n\n"
                for lydia_ai in lsts:
                    output_str += f"[User](tg://user?id={lydia_ai.user_id}) in chat `{lydia_ai.chat_id}`\n"
            else:
                output_str = "No Lydia AI enabled users / chats. Start by replying `.enai` to any user in any chat!"
            if len(output_str) > Config.MAX_MESSAGE_SIZE_LIMIT:
                with io.BytesIO(str.encode(output_str)) as out_file:
                    out_file.name = "lydia_ai.text"
                    await event.client.send_file(
                        event.chat_id,
                        out_file,
                        force_document=True,
                        allow_cache=False,
                        caption="Lydia AI enabled users",
                        reply_to=event,
                    )
            else:
                await catevent.edit(output_str)
        else:
            await catevent.edit(
                "Reply To User Message to Add / Delete them from Lydia Auto-Chat."
            )
    else:
        await catevent.edit(
            "Reply To A User's Message to Add / Delete them from Lydia Auto-Chat."
        )


@bot.on(admin_cmd(incoming=True))
async def on_new_message(event):
    if event.chat_id in Config.UB_BLACK_LIST_CHAT:
        return
    if Var.LYDIA_API_KEY is None:
        return
    reply = await event.get_reply_message()
    if reply is not None and reply.from_id != bot.uid:
        return
    if not event.media:
        user_id = event.from_id
        chat_id = event.chat_id
        s = get_s(user_id, chat_id)
        if s is not None:
            session_id = s.session_id
            session_expires = s.session_expires
            query = event.text
            # Check if the session is expired
            # If this method throws an exception at this point,
            # then there's an issue with the API, Auth or Server.
            if session_expires < time():
                # re-generate session
                session = lydia.create_session()
                logger.info(session)
                session_id = session.id
                session_expires = session.expires
                logger.info(add_s(user_id, chat_id, session_id, session_expires))
            # Try to think a thought.
            try:
                async with event.client.action(event.chat_id, "location"):
                    await asyncio.sleep(2)
                    output = lydia.think_thought(session_id, query)
                    await event.reply(output)
            except cf.exception.CoffeeHouseError as e:
                logger.info(str(e))


CMD_HELP.update(
    {
        "lydia": "**Plugin : **`lydia`\
    \n\n**Syntax : **`.enai` reply to a user\
    \n**Usage : **your bot will auto reply to the tagged user until you stops it by `.remcf`\
    \n\n**Syntax : **`.reai` reply to the user\
    \n**Usage : **disables the lydia\
    \n\n**Syntax : **`.liai`\
    \n**Usage : ** to list the users to whom you enabled ai(lydia)\
    \n\n for functioning this plugin you need to set the heroku var\
    \n the key is `LYDIA_API_KEY` and get var from `https://coffeehouse.intellivoid.net/`\
"
    }
)
