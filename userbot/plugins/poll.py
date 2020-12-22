import random

from telethon.errors.rpcbaseerrors import ForbiddenError
from telethon.errors.rpcerrorlist import PollOptionInvalidError
from telethon.tl.types import InputMediaPoll, Poll

from . import Build_Poll


@bot.on(admin_cmd(pattern="poll( (.*)|$)"))
@bot.on(sudo_cmd(pattern="poll( (.*)|$)", allow_sudo=True))
async def pollcreator(catpoll):
    reply_to_id = None
    if catpoll.reply_to_msg_id:
        reply_to_id = catpoll.reply_to_msg_id
    string = "".join(catpoll.text.split(maxsplit=1)[1:])
    if not string:
        options = Build_Poll(["Yah sure 😊✌️", "Nah 😏😕", "Whatever die sur 🥱🙄"])
        try:
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
            await catpoll.delete()
        except PollOptionInvalidError:
            await edit_or_reply(
                catpoll, "`A poll option used invalid data (the data may be too long).`"
            )
        except ForbiddenError:
            await edit_or_reply(catpoll, "`This chat has forbidden the polls`")
        except exception as e:
            await edit_or_reply(catpoll, str(e))
    else:
        catinput = string.split(";")
        if len(catinput) > 2 and len(catinput) < 12:
            options = Build_Poll(catinput[1:])
            try:
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
                await catpoll.delete()
            except PollOptionInvalidError:
                await edit_or_reply(
                    catpoll,
                    "`A poll option used invalid data (the data may be too long).`",
                )
            except ForbiddenError:
                await edit_or_reply(catpoll, "`This chat has forbidden the polls`")
            except Exception as e:
                await edit_or_reply(catpoll, str(e))
        else:
            await edit_or_reply(
                catpoll,
                "Make sure that you used Correct syntax `.poll question ; option1 ; option2`",
            )


CMD_HELP.update(
    {
        "poll": "**Plugin :**`poll`\
        \n\n**Syntax :** `.poll`\
        \n**Usage : **If you doesnt give any input it sends a default poll. if you like customize it then use this syntax :\
        \n `.poll question ; option 1; option2 ;`\
        \n ';' this seperates the each option and question \
        "
    }
)
