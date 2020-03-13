"""
SLAP Plugin For Userbot
usage:-.slap in reply to any message, or u gonna slap urself.

"""

import sys
from telethon import events, functions
from uniborg.util import admin_cmd
import random
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName


SLAP_TEMPLATES = [
    "{hits} {victim} with a {item}.",
    "{hits} {victim} in the face with a {item}.",
    "{hits} {victim} around a bit with a {item}.",
    "{throws} a {item} at {victim}.",
    "grabs a {item} and {throws} it at {victim}'s face.",
    "{hits} a {item} at {victim}.",
    "{throws} a few {item} at {victim}.",
    "grabs a {item} and {throws} it in {victim}'s face.",
    "launches a {item} in {victim}'s general direction.",
    "sits on {victim}'s face while slamming a {item} into their crotch.",
    "starts slapping {victim} silly with a {item}.",
    "pins {victim} down and repeatedly {hits} them with a {item}.",
    "grabs up a {item} and {hits} {victim} with it.",
    "starts slapping {victim} silly with a {item}.",
    "holds {victim} down and repeatedly {hits} them with a {item}.",
    "prods {victim} with a {item}.",
    "picks up a {item} and {hits} {victim} with it.",
    "ties {victim} to a chair and {throws} a {item} at them.",
    "{hits} {victim} {where} with a {item}.",
    "ties {victim} to a pole and whips them with a {item}."
    "gave a friendly push to help {victim} learn to swim in lava.",
    "sent {victim} to /dev/null.",
    "sent {victim} down the memory hole.",
    "beheaded {victim}.",
    "threw {victim} off a building.",
    "replaced all of {victim}'s music with Nickelback.",
    "spammed {victim}'s email.",
    "made {victim} a knuckle sandwich.",
    "slapped {victim} with pure nothing.",
    "hit {victim} with a small, interstellar spaceship.",
    "quickscoped {victim}.",
    "put {victim} in check-mate.",
    "RSA-encrypted {victim} and deleted the private key.",
    "put {victim} in the friendzone.",
    "slaps {victim} with a DMCA takedown request!"
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
    "pair of trousers",
    "CRT monitor",
    "diamond sword",
    "baguette",
    "physics textbook",
    "toaster",
    "portrait of Richard Stallman",
    "television",
    "mau5head",
    "five ton truck",
    "roll of duct tape",
    "book",
    "laptop",
    "old television",
    "sack of rocks",
    "rainbow trout",
    "cobblestone block",
    "lava bucket",
    "rubber chicken",
    "spiked bat",
    "gold block",
    "fire extinguisher",
    "heavy rock",
    "chunk of dirt",
    "beehive",
    "piece of rotten meat",
    "bear",
    "ton of bricks",
]

THROW = [
    "throws",
    "flings",
    "chucks",
    "hurls",
]

HIT = [
    "hits",
    "whacks",
    "slaps",
    "smacks",
    "bashes",
]

WHERE = [
      "in the chest",
      "on the head",
      "on the bum",
]


@borg.on(admin_cmd(pattern="slap ?(.*)", allow_sudo=True))
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
        replied_user = await event.client(GetFullUserRequest(previous_message.from_id))
    else:
        user = event.pattern_match.group(1)

        if user.isnumeric():
            user = int(user)

        if not user:
            self_user = await event.client.get_me()
            user = self_user.id

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user
        try:
            user_object = await event.client.get_entity(user)
            replied_user = await event.client(GetFullUserRequest(user_object.id))

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
    where = random.choice(WHERE)

    caption = "@"+borg.me.username+" "+ temp.format(victim=slapped, item=item, hits=hit, throws=throw, where=where)

    return caption
