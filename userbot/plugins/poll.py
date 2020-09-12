import random

from telethon.tl.types import InputMediaPoll, Poll

from ..utils import admin_cmd, sudo_cmd
from . import Build_Poll


@borg.on(admin_cmd(pattern="poll( (.*)|$)"))
@borg.on(sudo_cmd(pattern="poll( (.*)|$)", allow_sudo=True))
async def pollcreator(catpoll):
    reply_to_id = catpoll.message.id
    if catpoll.reply_to_msg_id:
        reply_to_id = catpoll.reply_to_msg_id
    string = "".join(event.text.split(maxsplit=1)[1:])
    if not string:
        options = Build_Poll(["Yah sure😊✌️", "Nah😏😕", "Whatever die sur🥱🙄"])
        await bot.send_message(
            catpoll.chat_id,
            file=InputMediaPoll(
                poll=Poll(
                    id=random.getrandbits(32),
                    question="👆👆So do you guys agree to this?",
                    answers=options,
                )
            ),
            reply_to=reply_to_id,
        )
