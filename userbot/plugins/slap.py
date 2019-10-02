"""
SLAP Plugin For Userbot
usage:- .slap in reply to any message, or u gonna slap urself.

"""

import sys
from telethon import events, functions
import random
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName


SLAP_TEMPLATES = [
    "{hits} {user2} with a {item}.",
    "{hits} {user2} in the face with a {item}.",
    "{hits} {user2} around a bit with a {item}.",
    "{throws} a {item} at {user2}.",
    "grab a {item} and {throws} it at {user2}'s face.",
    "launch a {item} in {user2}'s general direction.",
    "start slapping {user2} silly with a {item}.",
    "pin {user2} down and repeatedly {hits} them with a {item}.",
    "grab up a {item} and {hits} {user2} with it.",
    "tie {user2} to a chair and {throws} a {item} at them.",
    "gave a friendly push to help {user2} learn to swim in lava."
]

ITEMS = [
    "cast iron skillet",
    "large trout",
    "baseball bat",
    "cricket bat",
    "wooden cane",
    "nail",
    "printer",
    "shovel",
    "CRT monitor",
    "physics textbook",
    "toaster",
    "portrait of Richard Stallman",
    "television",
    "five ton truck",
    "roll of duct tape",
    "book",
    "laptop",
    "old television",
    "sack of rocks",
    "rainbow trout",
    "rubber chicken",
    "spiked bat",
    "fire extinguisher",
    "heavy rock",
    "chunk of dirt",
    "beehive",
    "piece of rotten meat",
    "bear",
    "ton of bricks",
]

THROW = [
    "throw",
    "fling",
    "chuck",
    "hurl",
]

HIT = [
    "hit",
    "whack",
    "slap",
    "smack",
    "bash",
]


@borg.on(events.NewMessage(pattern=r"\.slap ?(.*)", outgoing=True))
async def who(event):
    if event.fwd_from:
        return
    replied_user = await get_user(event)
    caption = await slap(replied_user, event)
    message_id_to_reply = event.message.reply_to_msg_id

    if not message_id_to_reply:
        message_id_to_reply = None

    try:
        await event.edit(caption)

    except:
        await event.edit("`Can't slap this nibba !!`")

async def get_user(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        replied_user = await borg(GetFullUserRequest(previous_message.from_id))
    else:
        user = event.pattern_match.group(1)

        if user.isnumeric():
            user = int(user)

        if not user:
            self_user = await borg.get_me()
            user = self_user.id

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await borg(GetFullUserRequest(user_id))
                return replied_user
        try:
            user_object = await borg.get_entity(user)
            replied_user = await borg(GetFullUserRequest(user_object.id))

        except (TypeError, ValueError):
            await event.edit("`I don't slap strangers !!`")
            return None

    return replied_user

async def slap(replied_user, event):
    user_id = replied_user.user.id
    first_name = replied_user.user.first_name
    username = replied_user.user.username

    if username:
        slapped = "@{}".format(username)
    else:
        slapped = f"[{first_name}](tg://user?id={user_id})"

    temp = random.choice(SLAP_TEMPLATES)
    item = random.choice(ITEMS)
    hit = random.choice(HIT)
    throw = random.choice(THROW)

    caption = "I " + temp.format(user2=slapped, item=item, hits=hit, throws=throw)

    return caption
