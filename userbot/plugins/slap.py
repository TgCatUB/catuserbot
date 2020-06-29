"""
SLAP Plugin For Userbot
usage:- .slap in reply to any message, or u gonna slap urself.
"""

import sys
from telethon import events, functions
from uniborg.util import admin_cmd
import random
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from userbot import ALIVE_NAME
from userbot import CMD_HELP

SLAP_TEMPLATES = [
    "{user1} {hits} {victim} with a {item}.",
    "{user1} {hits} {victim} in the face with a {item}.",
    "{user1} {hits} {victim} around a bit with a {item}.",
    "{user1} {throws} a {item} at {victim}.",
    "{user1} grabs a {item} and {throws} it at {victim}'s face.",
    "{user1} {hits} a {item} at {victim}.",
    "{user1} {throws} a few {item} at {victim}.",
    "{user1} grabs a {item} and {throws} it in {victim}'s face.",
    "{user1} launches a {item} in {victim}'s general direction.",
    "{user1} sits on {victim}'s face while slamming a {item} {where}.",
    "{user1} starts slapping {victim} silly with a {item}.",
    "{user1} pins {victim} down and repeatedly {hits} them with a {item}.",
    "{user1} grabs up a {item} and {hits} {victim} with it.",
    "{user1} starts slapping {victim} silly with a {item}.",
    "{user1} holds {victim} down and repeatedly {hits} them with a {item}.",
    "{user1} prods {victim} with a {item}.",
    "{user1} picks up a {item} and {hits} {victim} with it.",
    "{user1} ties {victim} to a chair and {throws} a {item} at them.",
    "{user1} {hits} {victim} {where} with a {item}.",
    "{user1} ties {victim} to a pole and whips them {where} with a {item}."
    "{user1} gave a friendly push to help {victim} learn to swim in lava.",
    "{user1} sent {victim} to /dev/null.",
    "{user1} sent {victim} down the memory hole.",
    "{user1} beheaded {victim}.",
    "{user1} threw {victim} off a building.",
    "{user1} replaced all of {victim}'s music with Nickelback.",
    "{user1} spammed {victim}'s email.",
    "{user1} made {victim} a knuckle sandwich.",
    "{user1} slapped {victim} with pure nothing.",
    "{user1} hit {victim} with a small, interstellar spaceship.",
    "{user1} quickscoped {victim}.",
    "{user1} put {victim} in check-mate.",
    "{user1} RSA-encrypted {victim} and deleted the private key.",
    "{user1} put {victim} in the friendzone.",
    "{user1} slaps {victim} with a DMCA takedown request!"
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

WHERE = ["in the chest", "on the head", "on the butt", "on the crotch"]

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "@Sur_vivor"

@borg.on(admin_cmd(pattern="slap ?(.*)"))
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

        if event.message.entities:
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

    caption = temp.format(user1=DEFAULTUSER, victim=slapped, item=item, hits=hit, throws=throw, where=where)

    return caption



CMD_HELP.update({
    "slap":
    ".slap reply to someones text with .slap\
    \nUsage: reply to slap them with random objects !!"
})
