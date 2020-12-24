# imported from pornhub credits to pornhub
import asyncio
import io
from datetime import datetime
from time import time

from coffeehouse.api import API
from coffeehouse.lydia import LydiaAI

from . import BOTLOG, BOTLOG_CHATID
from .sql_helper.lydia_ai_sql import add_s, get_all_s, get_s, remove_s

if Config.LYDIA_API_KEY:
    api_key = Config.LYDIA_API_KEY
    # Create the coffeehouse API
    coffeehouse_api = API(api_key)
    # Create Lydia instance
    lydia = LydiaAI(coffeehouse_api)


@bot.on(admin_cmd(pattern="(en|re|li)ai$", outgoing=True))
@bot.on(sudo_cmd(pattern="(en|re|li)ai$", allow_sudo=True))
async def lydia_disable_enable(event):
    if event.fwd_from:
        return
    if Config.LYDIA_API_KEY is None:
        await edit_delete(event, "`Please add required LYDIA_API_KEY env var`", 10)
        return
    catevent = await edit_or_reply(event, "`.....`")
    input_str = event.pattern_match.group(1)
    if event.reply_to_msg_id is not None:
        reply_msg = await event.get_reply_message()
        user_id = reply_msg.sender_id
        chat_id = event.chat_id
        if input_str == "en":
            # Create a new chat session (Like a conversation)
            session = lydia.create_session()
            if BOTLOG:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    f"**Session ID: **`{session.id}`\
                                   \n**Session Available: **`{str(session.available)}`\
                                   \n**Session Language: **`{str(session.language)}`\
                                   \n**Session Expires : **`{datetime.fromtimestamp(session.expires).strftime('%Y-%m-%d %H:%M:%S')}`\
                    ",
                )
            add_s(user_id, chat_id, session.id, session.expires)
            await catevent.edit(f"Hello")
        elif input_str == "re":
            remove_s(user_id, chat_id)
            await catevent.edit(f"__[signal lost](tg://user?id={user_id})__")
        else:
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
        if input_str == "li":
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
            await edit_delete(
                catevent,
                "`Reply To A User's Message to Add / Remove them from Lydia Auto-Chat.`",
                5,
            )


@bot.on(admin_cmd(incoming=True))
async def on_new_message(event):
    if event.chat_id in Config.UB_BLACK_LIST_CHAT:
        return
    if Config.LYDIA_API_KEY is None:
        return
    reply = await event.get_reply_message()
    if reply is not None and reply.sender_id != bot.uid:
        return
    if not event.media:
        user_id = event.sender_id
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
    \n\n  •  **Syntax : **`.enai reply`\
    \n  •  **Function : **your bot will auto reply to the tagged user until you stop it by `.remcf`\
    \n\n  •  **Syntax : **`.reai reply`\
    \n  •  **Function : **disables the lydia( auto reply )\
    \n\n  •  **Syntax : **`.liai`\
    \n  •  **Function : **to list the users to whom you enabled ai( lydia )\
    \n\n  •  **NOTE : **for functioning this plugin you need to set the heroku var\
    \n the key is `LYDIA_API_KEY` and get var from `https://coffeehouse.intellivoid.net/`\
"
    }
)
