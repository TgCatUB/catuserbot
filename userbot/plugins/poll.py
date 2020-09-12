import random

from telethon.tl.types import InputMediaPoll, Poll

from ..utils import admin_cmd, edit_or_reply, sudo_cmd
from . import Build_Poll


@borg.on(admin_cmd(pattern="poll( (.*)|$)"))
@borg.on(sudo_cmd(pattern="poll( (.*)|$)", allow_sudo=True))
async def pollcreator(catpoll):
    reply_to_id = None
    if catpoll.reply_to_msg_id:
        reply_to_id = catpoll.reply_to_msg_id
    string = "".join(catpoll.text.split(maxsplit=1)[1:])
    if not string:
        options = Build_Poll(["Yah sure 😊✌️", "Nah 😏😕", "Whatever die sur 🥱🙄"])
        try:
            await catpoll.delete()
            await bot.send_message(
                catpoll.chat_id,
                file=InputMediaPoll(
                    poll=Poll(
                        id=random.getrandbits(32),
                        question="👆👆So do you guys agree with this?",
                        answers=options,
                    )
                ),
                reply_to=reply_to_id,
            )
        except Exception as e:
            await edit_or_reply(catpoll, e)    
    else:
        catinput = string.split(";")
        if len(catinput) > 2 and len(catinput) < 12:
            options = Build_Poll(catinput[1:])
            try:
                await catpoll.delete()
                await bot.send_message(
                    catpoll.chat_id,
                    file=InputMediaPoll(
                        poll=Poll(
                            id=random.getrandbits(32),
                            question=catinput[0],
                            answers=options,
                        )
                    ),
                    reply_to=reply_to_id,
                )
            except Exception as e:
                await edit_or_reply(catpoll, e)
        else:
            await edit_or_reply(
                catpoll,
                "Make sure that you used Correct syntax `.poll question ; option1 ; option2`",
            )
