#    Haruka Aya (A telegram bot project)
#    Copyright (C) 2017-2019 Paul Larsen
#    Copyright (C) 2019-2020 Akito Mizukito (Haruka Network Development)

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import random, re, io, asyncio
from PIL import Image
from io import BytesIO
from spongemock import spongemock
from zalgo_text import zalgo
from deeppyer import deepfry
import os
from pathlib import Path
import glob

from typing import List
from telegram import Update, Bot, ParseMode, Message
from telegram.ext import run_async

from haruka import dispatcher, DEEPFRY_TOKEN, LOGGER
from haruka.modules.disable import DisableAbleCommandHandler
from telegram.utils.helpers import escape_markdown
from haruka.modules.helper_funcs.extraction import extract_user
from haruka.modules.tr_engine.strings import tld, tld_list

WIDE_MAP = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
WIDE_MAP[0x20] = 0x3000

# D A N K modules by @deletescape vvv


@run_async
def owo(bot: Bot, update: Update, args: List[str]):
    chat = update.effective_chat
    message = update.effective_message

    noreply = False
    if message.reply_to_message:
        data = message.reply_to_message.text
    elif args:
        noreply = True
        data = message.text.split(None, 1)[1]
    else:
        noreply = True
        data = tld(chat.id, "memes_no_message")

    faces = [
        '(・`ω´・)', ';;w;;', 'owo', 'UwU', '>w<', '^w^', '\(^o\) (/o^)/',
        '( ^ _ ^)∠☆', '(ô_ô)', '~:o', ';____;', '(*^*)', '(>_', '(♥_♥)',
        '*(^O^)*', '((+_+))'
    ]
    reply_text = re.sub(r'[rl]', "w", data)
    reply_text = re.sub(r'[ｒｌ]', "ｗ", data)
    reply_text = re.sub(r'[RL]', 'W', reply_text)
    reply_text = re.sub(r'[ＲＬ]', 'Ｗ', reply_text)
    reply_text = re.sub(r'n([aeiouａｅｉｏｕ])', r'ny\1', reply_text)
    reply_text = re.sub(r'ｎ([ａｅｉｏｕ])', r'ｎｙ\1', reply_text)
    reply_text = re.sub(r'N([aeiouAEIOU])', r'Ny\1', reply_text)
    reply_text = re.sub(r'Ｎ([ａｅｉｏｕＡＥＩＯＵ])', r'Ｎｙ\1', reply_text)
    reply_text = re.sub(r'\!+', ' ' + random.choice(faces), reply_text)
    reply_text = re.sub(r'！+', ' ' + random.choice(faces), reply_text)
    reply_text = reply_text.replace("ove", "uv")
    reply_text = reply_text.replace("ｏｖｅ", "ｕｖ")
    reply_text += ' ' + random.choice(faces)

    if noreply:
        message.reply_text(reply_text)
    else:
        message.reply_to_message.reply_text(reply_text)


@run_async
def stretch(bot: Bot, update: Update, args: List[str]):
    chat = update.effective_chat
    message = update.effective_message

    noreply = False
    if message.reply_to_message:
        data = message.reply_to_message.text
    elif args:
        noreply = True
        data = message.text.split(None, 1)[1]
    else:
        noreply = True
        data = tld(chat.id, "memes_no_message")

    count = random.randint(3, 10)
    reply_text = re.sub(r'([aeiouAEIOUａｅｉｏｕＡＥＩＯＵ])', (r'\1' * count), data)

    if noreply:
        message.reply_text(reply_text)
    else:
        message.reply_to_message.reply_text(reply_text)


@run_async
def vapor(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    chat = update.effective_chat

    noreply = False
    if message.reply_to_message:
        data = message.reply_to_message.text
    elif args:
        noreply = True
        data = message.text.split(None, 1)[1]
    else:
        noreply = True
        data = tld(chat.id, "memes_no_message")

    reply_text = str(data).translate(WIDE_MAP)

    if noreply:
        message.reply_text(reply_text)
    else:
        message.reply_to_message.reply_text(reply_text)


# D A N K modules by @deletescape ^^^
# Less D A N K modules by @skittles9823 # holi fugg I did some maymays vvv


@run_async
def mafiatext(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    chat = update.effective_chat

    noreply = False
    if message.reply_to_message:
        data = message.reply_to_message.text
    elif args:
        noreply = True
        data = message.text.split(None, 1)[1]
    else:
        noreply = True
        data = tld(chat.id, "memes_no_message")

    if not Path('images/mafia.jpg').is_file():
        LOGGER.warning(
            "images/mafia.jpg not found! Mafia memes module is turned off!")
        return

    for mocked in glob.glob("images/mafiaed*"):
        os.remove(mocked)
    reply_text = spongemock.mock(data)

    randint = random.randint(1, 699)
    magick = """convert images/mafia.jpg -font Impact -pointsize 50 -size 1280x720 -stroke white -strokewidth 1 -fill black -background none -gravity north caption:"{}" -flatten images/mafiaed{}.jpg""".format(
        reply_text, randint)
    os.system(magick)
    with open('images/mafiaed{}.jpg'.format(randint), 'rb') as mockedphoto:
        if noreply:
            message.reply_photo(photo=mockedphoto,
                                reply=message.reply_to_message)
        else:
            message.reply_to_message.reply_photo(
                photo=mockedphoto, reply=message.reply_to_message)
    os.remove('images/mafiaed{}.jpg'.format(randint))


@run_async
def pidortext(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    chat = update.effective_chat

    noreply = False
    if message.reply_to_message:
        data = message.reply_to_message.text
    elif args:
        noreply = True
        data = message.text.split(None, 1)[1]
    else:
        noreply = True
        data = tld(chat.id, "memes_no_message")

    if not Path('images/4pda.jpg').is_file():
        LOGGER.warning(
            "images/4pda.jpg not found! Pidor memes module is turned off!")
        return
    for mocked in glob.glob("images/4pdaed*"):
        os.remove(mocked)
    reply_text = spongemock.mock(data)

    randint = random.randint(1, 699)
    magick = """convert images/4pda.jpg -font Impact -pointsize 50 -size 400x300 -stroke black -strokewidth 1 -fill white -background none -gravity north caption:"{}" -flatten images/4pdaed{}.jpg""".format(
        reply_text, randint)
    os.system(magick)
    with open('images/4pdaed{}.jpg'.format(randint), 'rb') as mockedphoto:
        if noreply:
            message.reply_photo(photo=mockedphoto,
                                reply=message.reply_to_message)
        else:
            message.reply_to_message.reply_photo(
                photo=mockedphoto, reply=message.reply_to_message)
    os.remove('images/4pdaed{}.jpg'.format(randint))


@run_async
def kimtext(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    chat = update.effective_chat

    noreply = False
    if message.reply_to_message:
        data = message.reply_to_message.text
    elif args:
        noreply = True
        data = message.text.split(None, 1)[1]
    else:
        noreply = True
        data = tld(chat.id, "memes_no_message")

    if not Path('images/kim.jpg').is_file():
        LOGGER.warning(
            "images/kim.jpg not found! Kim memes module is turned off!")
        return
    for mocked in glob.glob("kimed*"):
        os.remove(mocked)
    reply_text = spongemock.mock(data)

    randint = random.randint(1, 699)
    magick = """convert images/kim.jpg -font Impact -pointsize 50 -size 480x360 -stroke black -strokewidth 1 -fill white -background none -gravity north caption:"{}" -flatten images/kimed{}.jpg""".format(
        reply_text, randint)
    os.system(magick)
    with open('images/kimed{}.jpg'.format(randint), 'rb') as mockedphoto:
        if noreply:
            message.reply_photo(photo=mockedphoto,
                                reply=message.reply_to_message)
        else:
            message.reply_to_message.reply_photo(
                photo=mockedphoto, reply=message.reply_to_message)
    os.remove('images/kimed{}.jpg'.format(randint))


@run_async
def hitlertext(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    chat = update.effective_chat

    noreply = False
    if message.reply_to_message:
        data = message.reply_to_message.text
    elif args:
        noreply = True
        data = message.text.split(None, 1)[1]
    else:
        noreply = True
        data = tld(chat.id, "memes_no_message")

    if not Path('images/hitler.jpg').is_file():
        LOGGER.warning(
            "images/hitler.jpg not found! Hitler memes module is turned off!")
        return
    for mocked in glob.glob("images/hitlered*"):
        os.remove(mocked)
    reply_text = spongemock.mock(data)

    randint = random.randint(1, 699)
    magick = """convert images/hitler.jpg -font Impact -pointsize 50 -size 615x409 -stroke black -strokewidth 1 -fill white -background none -gravity north caption:"{}" -flatten images/hitlered{}.jpg""".format(
        reply_text, randint)
    os.system(magick)
    with open('images/hitlered{}.jpg'.format(randint), 'rb') as mockedphoto:
        if noreply:
            message.reply_photo(photo=mockedphoto,
                                reply=message.reply_to_message)
        else:
            message.reply_to_message.reply_photo(
                photo=mockedphoto, reply=message.reply_to_message)
    os.remove('images/hitlered{}.jpg'.format(randint))


@run_async
def spongemocktext(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    chat = update.effective_chat

    noreply = False
    if message.reply_to_message:
        data = message.reply_to_message.text
    elif args:
        noreply = True
        data = message.text.split(None, 1)[1]
    else:
        noreply = True
        data = tld(chat.id, "memes_no_message")

    if not Path('images/bob.jpg').is_file():
        LOGGER.warning(
            "images/bob.jpg not found! Spongemock memes module is turned off!")
        return
    for mocked in glob.glob("images/mocked*"):
        os.remove(mocked)
    reply_text = spongemock.mock(data)

    randint = random.randint(1, 699)
    magick = """convert images/bob.jpg -font Impact -pointsize 30 -size 512x300 -stroke black -strokewidth 1 -fill white -background none -gravity north caption:"{}" -flatten images/mocked{}.jpg""".format(
        reply_text, randint)
    os.system(magick)
    with open('images/mocked{}.jpg'.format(randint), 'rb') as mockedphoto:
        if noreply:
            message.reply_photo(photo=mockedphoto,
                                reply=message.reply_to_message)
        else:
            message.reply_to_message.reply_photo(
                photo=mockedphoto, reply=message.reply_to_message)
    os.remove('images/mocked{}.jpg'.format(randint))


@run_async
def zalgotext(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    chat = update.effective_chat

    noreply = False
    if message.reply_to_message:
        data = message.reply_to_message.text
    elif args:
        noreply = True
        data = message.text.split(None, 1)[1]
    else:
        noreply = True
        data = tld(chat.id, "memes_no_message")

    reply_text = zalgo.zalgo().zalgofy(data)
    if noreply:
        message.reply_text(reply_text)
    else:
        message.reply_to_message.reply_text(reply_text)


# Less D A N K modules by @skittles9823 # holi fugg I did some maymays ^^^
# shitty maymay modules made by @divadsn vvv


@run_async
def deepfryer(bot: Bot, update: Update):
    message = update.effective_message
    chat = update.effective_chat
    if message.reply_to_message:
        data = message.reply_to_message.photo
        data2 = message.reply_to_message.sticker
    else:
        data = []
        data2 = []

    # check if message does contain media and cancel when not
    if not data and not data2:
        message.reply_text(tld(chat.id, "memes_deepfry_nothing"))
        return

    # download last photo (highres) as byte array
    if data:
        photodata = data[len(data) - 1].get_file().download_as_bytearray()
        image = Image.open(io.BytesIO(photodata))
    elif data2:
        sticker = bot.get_file(data2.file_id)
        sticker.download('sticker.png')
        image = Image.open("sticker.png")

    # the following needs to be executed async (because dumb lib)
    loop = asyncio.new_event_loop()
    loop.run_until_complete(
        process_deepfry(image, message.reply_to_message, bot))
    loop.close()


async def process_deepfry(image: Image, reply: Message, bot: Bot):
    # DEEPFRY IT
    image = await deepfry(img=image,
                          token=DEEPFRY_TOKEN,
                          url_base='westeurope')

    bio = BytesIO()
    bio.name = 'image.jpeg'
    image.save(bio, 'JPEG')

    # send it back
    bio.seek(0)
    reply.reply_photo(bio)
    if Path("sticker.png").is_file():
        os.remove("sticker.png")


# shitty maymay modules made by @divadsn ^^^


@run_async
def shout(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    chat = update.effective_chat

    if message.reply_to_message:
        data = message.reply_to_message.text
    elif args:
        data = " ".join(args)
    else:
        data = tld(chat.id, "memes_no_message")

    msg = "```"
    result = []
    result.append(' '.join([s for s in data]))
    for pos, symbol in enumerate(data[1:]):
        result.append(symbol + ' ' + '  ' * pos + symbol)
    result = list("\n".join(result))
    result[0] = data[0]
    result = "".join(result)
    msg = "```\n" + result + "```"
    return update.effective_message.reply_text(msg, parse_mode="MARKDOWN")


@run_async
def insults(bot: Bot, update: Update):
    message = update.effective_message
    chat = update.effective_chat
    text = random.choice(tld_list(chat.id, "memes_insults_list"))

    if message.reply_to_message:
        message.reply_to_message.reply_text(text)
    else:
        message.reply_text(text)


@run_async
def runs(bot: Bot, update: Update):
    chat = update.effective_chat
    update.effective_message.reply_text(
        random.choice(tld_list(chat.id, "memes_runs_list")))


@run_async
def slap(bot: Bot, update: Update, args: List[str]):
    chat = update.effective_chat
    msg = update.effective_message

    # reply to correct message
    reply_text = msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text

    # get user who sent message
    if msg.from_user.username:
        curr_user = "@" + escape_markdown(msg.from_user.username)
    else:
        curr_user = "[{}](tg://user?id={})".format(msg.from_user.first_name,
                                                   msg.from_user.id)

    user_id = extract_user(update.effective_message, args)
    if user_id:
        slapped_user = bot.get_chat(user_id)
        user1 = curr_user
        if slapped_user.username == "RealAkito":
            reply_text(tld(chat.id, "memes_not_doing_that"))
            return
        if slapped_user.username:
            user2 = "@" + escape_markdown(slapped_user.username)
        else:
            user2 = "[{}](tg://user?id={})".format(slapped_user.first_name,
                                                   slapped_user.id)

    # if no target found, bot targets the sender
    else:
        user1 = "[{}](tg://user?id={})".format(bot.first_name, bot.id)
        user2 = curr_user

    temp = random.choice(tld_list(chat.id, "memes_slaps_templates_list"))
    item = random.choice(tld_list(chat.id, "memes_items_list"))
    hit = random.choice(tld_list(chat.id, "memes_hit_list"))
    throw = random.choice(tld_list(chat.id, "memes_throw_list"))
    itemp = random.choice(tld_list(chat.id, "memes_items_list"))
    itemr = random.choice(tld_list(chat.id, "memes_items_list"))

    repl = temp.format(user1=user1,
                       user2=user2,
                       item=item,
                       hits=hit,
                       throws=throw,
                       itemp=itemp,
                       itemr=itemr)

    reply_text(repl, parse_mode=ParseMode.MARKDOWN)


__help__ = True

OWO_HANDLER = DisableAbleCommandHandler("owo",
                                        owo,
                                        admin_ok=True,
                                        pass_args=True)
STRETCH_HANDLER = DisableAbleCommandHandler("stretch", stretch, pass_args=True)
VAPOR_HANDLER = DisableAbleCommandHandler("vapor",
                                          vapor,
                                          pass_args=True,
                                          admin_ok=True)
MOCK_HANDLER = DisableAbleCommandHandler("mock",
                                         spongemocktext,
                                         admin_ok=True,
                                         pass_args=True)
KIM_HANDLER = DisableAbleCommandHandler("kim",
                                        kimtext,
                                        admin_ok=True,
                                        pass_args=True)
MAFIA_HANDLER = DisableAbleCommandHandler("mafia",
                                          mafiatext,
                                          admin_ok=True,
                                          pass_args=True)
PIDOR_HANDLER = DisableAbleCommandHandler("pidor",
                                          pidortext,
                                          admin_ok=True,
                                          pass_args=True)
HITLER_HANDLER = DisableAbleCommandHandler("hitler",
                                           hitlertext,
                                           admin_ok=True,
                                           pass_args=True)
ZALGO_HANDLER = DisableAbleCommandHandler("zalgofy", zalgotext, pass_args=True)
DEEPFRY_HANDLER = DisableAbleCommandHandler("deepfry",
                                            deepfryer,
                                            admin_ok=True)
SHOUT_HANDLER = DisableAbleCommandHandler("shout", shout, pass_args=True)
INSULTS_HANDLER = DisableAbleCommandHandler("insults", insults, admin_ok=True)
RUNS_HANDLER = DisableAbleCommandHandler("runs", runs, admin_ok=True)
SLAP_HANDLER = DisableAbleCommandHandler("slap",
                                         slap,
                                         pass_args=True,
                                         admin_ok=True)

dispatcher.add_handler(MAFIA_HANDLER)
dispatcher.add_handler(PIDOR_HANDLER)
dispatcher.add_handler(SHOUT_HANDLER)
dispatcher.add_handler(OWO_HANDLER)
dispatcher.add_handler(STRETCH_HANDLER)
dispatcher.add_handler(VAPOR_HANDLER)
dispatcher.add_handler(MOCK_HANDLER)
dispatcher.add_handler(ZALGO_HANDLER)
dispatcher.add_handler(DEEPFRY_HANDLER)
dispatcher.add_handler(KIM_HANDLER)
dispatcher.add_handler(HITLER_HANDLER)
dispatcher.add_handler(INSULTS_HANDLER)
dispatcher.add_handler(RUNS_HANDLER)
dispatcher.add_handler(SLAP_HANDLER)
