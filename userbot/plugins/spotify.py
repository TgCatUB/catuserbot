"""Module to display Currenty Playing Spotify Songs in your bio"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#  CREDITS:
# [Poolitzer](https://t.me/poolitzer)  (for creating spotify bio plugin)
#
# [Sunny](https://t.me/medevilofxd) and Others for spotify_userbot
# (https://github.com/anilchauhanxda/spotify_userbot/blob/master/bot.py)
#
# Github.com/code-rgb [ TG - @DetetedUser420 ]
#  Ported it to Pyrogram and improved Heroku compatiblilty
#
# tg- @Jisan7509  // Github.com/Jisan09
# Ported back to teletethon.. xD // Added decent thumb & dual mode for now playing song
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import asyncio
import os
import re
import time
import urllib.request

import lyricsgenius
import requests
import ujson
from PIL import Image, ImageEnhance, ImageFilter
from telegraph import Telegraph
from telethon import events
from telethon.errors import AboutTooLongError, FloodWaitError
from telethon.tl.custom import Button
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.users import GetFullUserRequest
from validators.url import url

from userbot.core.logger import logging

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.functions.functions import (
    delete_conv,
    ellipse_create,
    ellipse_layout_create,
    make_inline,
    text_draw,
)
from ..sql_helper import global_collectionjson as glob_db
from . import BOTLOG, BOTLOG_CHATID, Config, catub, reply_id

SPOTIFY_CLIENT_ID = Config.SPOTIFY_CLIENT_ID
SPOTIFY_CLIENT_SECRET = Config.SPOTIFY_CLIENT_SECRET


LOGS = logging.getLogger(__name__)


plugin_category = "misc"


SP_DATABASE = None  # Main DB (Class Database)
# Saves Auth data cuz heroku doesn't have persistent storage
try:
    SPOTIFY_DB = glob_db.get_collection("SP_DATA").json
except AttributeError:
    SPOTIFY_DB = None


USER_INITIAL_BIO = {}  # Saves Users Original Bio
PATH = "userbot/cache/spotify_database.json"

# [---------------------------] Constants [------------------------------]
KEY = "🎶"
BIOS = [
    KEY + " Vibing : {interpret} - {title}",
    KEY + " : {interpret} - {title}",
    KEY + " Vibing : {title}",
    KEY + " : {title}",
]
OFFSET = 1
# reduce the OFFSET from our actual 70 character limit
LIMIT = 70 - OFFSET
# [----------------------------------------------------------------------]
# Errors
no_sp_vars = "Vars `SPOTIFY_CLIENT_ID` & `SPOTIFY_CLIENT_SECRET` are missing, add them first !\n\n[Follow this tutorial](https://telegra.ph/Steps-of-setting-Spotify-Vars-in-Catuserbot-04-24-2)"


class Database:
    def __init__(self):
        if not os.path.exists(PATH):
            if SPOTIFY_DB is None:
                return
            if db_ := SPOTIFY_DB.get("data"):
                access_token = db_.get("access_token")
                refresh_token = db_.get("refresh_token")
                to_create = {
                    "bio": "",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "telegram_spam": False,
                    "spotify_spam": False,
                }
                with open(PATH, "w") as outfile:
                    ujson.dump(to_create, outfile, indent=4)
        with open(PATH) as f:
            self.db = ujson.load(f)
        self.SPOTIFY_MODE = False

    def save_token(self, token):
        self.db["access_token"] = token
        self.save()

    def save_refresh(self, token):
        self.db["refresh_token"] = token
        self.save()

    def save_bio(self, bio):
        self.db["bio"] = bio
        self.save()

    def save_spam(self, which, what):
        self.db[f"{which}_spam"] = what

    def return_token(self):
        return self.db["access_token"]

    def return_refresh(self):
        return self.db["refresh_token"]

    def return_bio(self):
        return self.db["bio"]

    def return_spam(self, which):
        return self.db[f"{which}_spam"]

    def save(self):
        with open(PATH, "w") as outfile:
            ujson.dump(self.db, outfile, indent=4, sort_keys=True)


SP_DATABASE = Database()


def ms_converter(millis):
    millis = int(millis)
    seconds = (millis / 1000) % 60
    seconds = int(seconds)
    if str(seconds) == "0":
        seconds = "00"
    if len(str(seconds)) == 1:
        seconds = f"0{str(seconds)}"
    minutes = (millis / (1000 * 60)) % 60
    minutes = int(minutes)
    return f"{minutes}:{str(seconds)}"


@catub.cat_cmd(
    pattern="spsetup$",
    command=("spsetup", plugin_category),
    info={
        "header": "Setup for Spotify Auth",
        "description": "Login in your spotify account before doing this\nIn BOT Logger Group do .spsetup then follow the instruction.",
        "usage": "{tr}spsetup",
    },
)
async def spotify_setup(event):
    """Setup Spotify Creds"""
    global SP_DATABASE
    if not BOTLOG:
        return await edit_delete(
            event,
            "For authencation you need to set `PRIVATE_GROUP_BOT_API_ID` in heroku",
            7,
        )
    if not (SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET):
        return await edit_delete(event, no_sp_vars, 10)
    if event.chat_id != BOTLOG_CHATID:
        return await edit_delete(
            event, "CHAT INVALID :: Do this in your Log Channel", 7
        )
    authurl = (
        "https://accounts.spotify.com/authorize?client_id={}&response_type=code&redirect_uri="
        "https%3A%2F%2Fexample.com%2Fcallback&scope=user-read-playback-state%20user-read-currently"
        "-playing+user-follow-read+user-read-recently-played+user-top-read+playlist-read-private+playlist"
        "-modify-private+user-follow-modify+user-read-private"
    )
    async with event.client.conversation(BOTLOG_CHATID) as conv:
        msg = await conv.send_message(
            "Go to the following link in "
            f"your browser: {authurl.format(SPOTIFY_CLIENT_ID)} and reply this msg with the Page Url you got after giving authencation."
        )
        res = conv.wait_event(events.NewMessage(outgoing=True, chats=BOTLOG_CHATID))
        res = await res
        await msg.edit("`Processing ...`")
        initial_token = res.text.strip()
    if "code=" in initial_token:
        initial_token = (initial_token.split("code=", 1))[1]
    body = {
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "redirect_uri": "https://example.com/callback",
        "code": initial_token,
    }
    r = requests.post("https://accounts.spotify.com/api/token", data=body)
    save = r.json()
    access_token = save.get("access_token")
    refresh_token = save.get("refresh_token")
    if not (access_token and refresh_token):
        return await edit_delete(
            msg,
            "Auth. Unsuccessful !\ndo .spsetup again and provide a valid URL in reply",
            10,
        )
    to_create = {
        "bio": "",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "telegram_spam": False,
        "spotify_spam": False,
    }
    with open(PATH, "w") as outfile:
        ujson.dump(to_create, outfile, indent=4)
    await edit_delete(msg, "Done! Setup Successfull", 5)
    glob_db.add_collection(
        "SP_DATA",
        {"data": {"access_token": access_token, "refresh_token": refresh_token}},
    )
    SP_DATABASE = Database()


if SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET:
    # to stop unwanted spam, we sent these type of message only once. So we have a variable in our database which we check
    # for in return_info. When we send a message, we set this variable to true. After a successful update
    # (or a closing of spotify), we reset that variable to false.
    def save_spam(which, what):
        # see below why
        # this is if False is inserted, so if spam = False, so if everything is
        # good.
        if not what:
            # if it wasn't normal before, we proceed
            if SP_DATABASE.return_spam(which):
                # we save that it is normal now
                SP_DATABASE.save_spam(which, False)
                # we return True so we can test against it and if it this
                # function returns, we can send a fitting message
                return True
        elif not SP_DATABASE.return_spam(which):
            # we save that it is not normal now
            SP_DATABASE.save_spam(which, True)
            # we return True so we can send a message
            return True
        # if True wasn't returned before, we can return False now so our test
        # fails and we dont send a message
        return False

    async def spotify_bio():  # sourcery no-metrics
        while SP_DATABASE.SPOTIFY_MODE:
            # SPOTIFY
            skip = False
            to_insert = {}
            oauth = {"Authorization": "Bearer " + SP_DATABASE.return_token()}
            r = requests.get(
                "https://api.spotify.com/v1/me/player/currently-playing", headers=oauth
            )
            # 200 means user plays smth
            if r.status_code == 200:
                received = r.json()
                if received["currently_playing_type"] == "track":
                    to_insert["title"] = received["item"]["name"]
                    to_insert["progress"] = ms_converter(received["progress_ms"])
                    to_insert["interpret"] = received["item"]["artists"][0]["name"]
                    to_insert["duration"] = ms_converter(
                        received["item"]["duration_ms"]
                    )
                    to_insert["link"] = received["item"]["external_urls"]["spotify"]
                    to_insert["image"] = received["item"]["album"]["images"][1]["url"]
                    if save_spam("spotify", False):
                        stringy = (
                            "**[INFO]**\n\nEverything returned back to normal, the previous spotify issue has been "
                            "resolved."
                        )
                        await catub.send_message(BOTLOG_CHATID, string)
                else:
                    if save_spam("spotify", True):
                        # currently item is not passed when the user plays a
                        # podcast
                        string = (
                            f"**[INFO]**\n\nThe playback {received['currently_playing_type']}"
                            " didn't gave me any additional information, so I skipped updating the bio."
                        )
                        await catub.send_message(BOTLOG_CHATID, string)
            # 429 means flood limit, we need to wait
            elif r.status_code == 429:
                to_wait = r.headers["Retry-After"]
                LOGS.error(f"Spotify, have to wait for {str(to_wait)}")
                await catub.send_message(
                    BOTLOG_CHATID,
                    "**[WARNING]**\n\nI caught a spotify api limit. I shall sleep for "
                    f"{str(to_wait)} seconds until I refresh again",
                )
                skip = True
                await asyncio.sleep(int(to_wait))
            # 204 means user plays nothing, since to_insert is false, we dont
            # need to change anything
            elif r.status_code == 204:
                if save_spam("spotify", False):
                    stringy = (
                        "**[INFO]**\n\nEverything returned back to normal, the previous spotify issue has been "
                        "resolved."
                    )
                    await catub.send_message(BOTLOG_CHATID, stringy)
            # 401 means our access token is expired, so we need to refresh it
            elif r.status_code == 401:
                data = {
                    "client_id": SPOTIFY_CLIENT_ID,
                    "client_secret": SPOTIFY_CLIENT_SECRET,
                    "grant_type": "refresh_token",
                    "refresh_token": SP_DATABASE.return_refresh(),
                }
                r = requests.post("https://accounts.spotify.com/api/token", data=data)
                received = r.json()
                # if a new refresh is token as well, we save it here
                try:
                    SP_DATABASE.save_refresh(received["refresh_token"])
                except KeyError:
                    pass
                SP_DATABASE.save_token(received["access_token"])
                glob_db.add_collection(
                    "SP_DATA",
                    {
                        "data": {
                            "access_token": SP_DATABASE.return_token(),
                            "refresh_token": SP_DATABASE.return_refresh(),
                        }
                    },
                )
                # since we didnt actually update our status yet, lets do this
                # without the 30 seconds wait
                skip = True
            # 502 means bad gateway, its an issue on spotify site which we can do nothing about. 30 seconds wait shouldn't
            # put too much pressure on the spotify server, so we are just going
            # to notify the user once
            elif r.status_code == 502:
                if save_spam("spotify", True):
                    string = (
                        "**[WARNING]**\n\nSpotify returned a Bad gateway, which means they have a problem on their "
                        "servers. The bot will continue to run but may not update the bio for a short time."
                    )
                    await catub.send_message(BOTLOG_CHATID, string)
            # 503 means service unavailable, its an issue on spotify site which we can do nothing about. 30 seconds wait
            # shouldn't put too much pressure on the spotify server, so we are
            # just going to notify the user once
            elif r.status_code == 503:
                if save_spam("spotify", True):
                    string = (
                        "**[WARNING]**\n\nSpotify said that the service is unavailable, which means they have a "
                        "problem on their servers. The bot will continue to run but may not update the bio for a "
                        "short time."
                    )
                    await catub.send_message(BOTLOG_CHATID, string)
            # 404 is a spotify error which isn't supposed to happen (since our URL is correct). Track the issue here:
            # https://github.com/spotify/web-api/issues/1280
            elif r.status_code == 404:
                if save_spam("spotify", True):
                    string = "**[INFO]**\n\nSpotify returned a 404 error, which is a bug on their side."
                    await catub.send_message(BOTLOG_CHATID, string)
            # catch anything else
            else:
                await catub.send_message(
                    BOTLOG_CHATID,
                    "**[ERROR]**\n\nOK, so something went reeeally wrong with spotify. The bot "
                    "was stopped.\nStatus code: "
                    + str(r.status_code)
                    + "\n\nText: "
                    + r.text,
                )
                LOGS.error(f"Spotify, error {str(r.status_code)}, text: {r.text}")
                # stop the whole program since I dont know what happens here
                # and this is the safest thing we can do
                SP_DATABASE.SPOTIFY_MODE = False
            # TELEGRAM
            try:
                # full needed, since we dont get a bio with the normal request
                full = (await catub(GetFullUserRequest(catub.uid))).full_user
                bio = full.about
                # to_insert means we have a successful playback
                if to_insert:
                    # putting our collected information's into nice variables
                    title = to_insert["title"]
                    interpret = to_insert["interpret"]
                    progress = to_insert["progress"]
                    duration = to_insert["duration"]
                    spotify_bio.interpret = to_insert["interpret"]
                    spotify_bio.progress = to_insert["progress"]
                    spotify_bio.duration = to_insert["duration"]
                    spotify_bio.title = to_insert["title"]
                    spotify_bio.link = to_insert["link"]
                    spotify_bio.image = to_insert["image"]
                    # we need this variable to see if actually one of the BIOS
                    # is below the character limit
                    new_bio = ""
                    for bio in BIOS:
                        temp = bio.format(
                            title=title,
                            interpret=interpret,
                            progress=progress,
                            duration=duration,
                        )
                        # we try to not ignore for telegrams character limit
                        # here
                        if len(temp) < LIMIT:
                            # this is short enough, so we put it in the
                            # variable and break our for loop
                            new_bio = temp
                            break
                    # if we have a bio, one bio was short enough
                    if new_bio:
                        # test if the user changed his bio to blank, we save it
                        # before we override
                        if not bio:
                            SP_DATABASE.save_bio(bio)
                        # test if the user changed his bio in the meantime, if
                        # yes, we save it before we override
                        elif "🎶" not in bio:
                            SP_DATABASE.save_bio(bio)
                        # test if the bio isn't the same, otherwise updating it
                        # would be stupid
                        if not new_bio == bio:
                            try:
                                await catub(UpdateProfileRequest(about=new_bio))
                                spotify_bio.lrt = time.time()
                                if save_spam("telegram", False):
                                    stringy = (
                                        "**[INFO]**\n\nEverything returned back to normal, the previous telegram "
                                        "issue has been resolved."
                                    )
                                    await catub.send_message(BOTLOG_CHATID, stringy)
                            # this can happen if our LIMIT check failed because telegram counts emojis twice and python
                            # doesnt. Refer to the constants file to learn more
                            # about this
                            except AboutTooLongError:
                                if save_spam("telegram", True):
                                    stringy = (
                                        "**[WARNING]**\n\nThe biography I tried to insert was too long. In order "
                                        "to not let that happen again in the future, please read the part about OFFSET "
                                        f"in the constants. Anyway, here is the bio I tried to insert:\n\n{new_bio}"
                                    )
                                    await catub.send_message(BOTLOG_CHATID, stringy)
                    # if we dont have a bio, everything was too long, so we
                    # tell the user that
                    if not new_bio:
                        if save_spam("telegram", True):
                            to_send = (
                                "**[INFO]**\n\nThe current track exceeded the character limit, so the bio wasn't "
                                f"updated.\n\n Track: {title}\nInterpret: {interpret}"
                            )
                            await catub.send_message(BOTLOG_CHATID, to_send)
                # not to_insert means no playback
                else:
                    if save_spam("telegram", False):
                        stringy = (
                            "**[INFO]**\n\nEverything returned back to normal, the previous telegram issue has "
                            "been resolved."
                        )
                        await catub.send_message(BOTLOG_CHATID, stringy)
                    old_bio = SP_DATABASE.return_bio()
                    # this means the bio is blank, so we save that as the new
                    # one
                    if not bio:
                        SP_DATABASE.save_bio(bio)
                    # this means an old playback is in the bio, so we change it
                    # back to the original one
                    elif "🎶" in bio:
                        await catub(UpdateProfileRequest(about=old_bio))
                    # this means a new original is there, lets save it
                    elif not bio == old_bio:
                        SP_DATABASE.save_bio(bio)
                    # this means the original one we saved is still valid
                    else:
                        pass
            except FloodWaitError as e:
                to_wait = e.seconds
                LOGS.error(f"to wait for {str(to_wait)}")
                await catub.send_message(
                    BOTLOG_CHATID,
                    "**[WARNING]**\n\nI caught a telegram api limit. I shall sleep "
                    f"{str(to_wait)} seconds until I refresh again",
                )
                skip = True
                await asyncio.sleep(to_wait)
            # skip means a flood error stopped the whole program, no need to
            # wait another 40 seconds after that
            if not skip:
                await asyncio.sleep(40)


async def sp_var_check(event):
    if not (SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET):
        await event.edit(no_sp_vars)
        return False
    if (SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET) and SP_DATABASE is None:
        await event.edit(
            "ERROR :: No Database was found!\n**Do `.help spsetup` for more info.**\n\n[Follow this tutorial](https://telegra.ph/Steps-of-setting-Spotify-Vars-in-Catuserbot-04-24-2)"
        )
        return False
    return True


@catub.cat_cmd(
    pattern="spbio$",
    command=("spbio", plugin_category),
    info={
        "header": "To Enable or Disable the spotify current playing to bio",
        "usage": "{tr}spbio",
    },
)
async def spotifybio(event):
    "Toggle Spotify Bio"
    if not await sp_var_check(event):
        return
    if SP_DATABASE.SPOTIFY_MODE:
        SP_DATABASE.SPOTIFY_MODE = False
        if USER_INITIAL_BIO:
            await catub(UpdateProfileRequest(about=USER_INITIAL_BIO["bio"]))
            USER_INITIAL_BIO.clear()
        await edit_delete(event, " `Spotify Bio disabled !`")
    else:
        await edit_delete(
            event,
            "✅ `Spotify Bio enabled` \nCurrent Spotify playback will updated in the Bio",
        )
        USER_INITIAL_BIO["bio"] = (
            (await catub(GetFullUserRequest(catub.uid))).full_user
        ).about or ""
        SP_DATABASE.SPOTIFY_MODE = True
        await spotify_bio()


def telegraph_lyrics(tittle, artist):
    telegraph = Telegraph()
    telegraph.create_account(short_name=Config.TELEGRAPH_SHORT_NAME)
    GENIUS = Config.GENIUS_API_TOKEN
    symbol = "❌"
    if GENIUS is None:
        result = "Set <b>GENIUS_API_TOKEN</b> in heroku vars for functioning of this command.<br><br><b>Check out this <a href = https://telegra.ph/How-to-get-Genius-API-Token-04-26>Tutorial</a></b>"
    else:
        genius = lyricsgenius.Genius(GENIUS)
        try:
            songs = genius.search_song(tittle, artist)
            content = songs.lyrics
            content = content.replace("\n", "<br>")
            result = f"<h3>{tittle}</h3><br><b>by {artist}</b><br><br>{content}"
            symbol = "📜"
        except (TypeError, AttributeError):
            result = "<b>Lyrics Not found!</b>"
            symbol = "❌"
    try:
        response = telegraph.create_page(
            "Lyrics",
            html_content=result,
            author_name="CatUserbot",
            author_url="https://t.me/catuserbot17",
        )
    except Exception as e:
        symbol = "❌"
        response = telegraph.create_page(
            "Lyrics",
            html_content=str(e),
            author_name="CatUserbot",
            author_url="https://t.me/catuserbot17",
        )
    return response["url"], symbol


def file_check():
    logo = "temp/cat_music.png"
    font_bold = "temp/ArialUnicodeMS.ttf"
    font_mid = "temp/GoogleSans-Medium.ttf"
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    if not os.path.exists(logo):
        urllib.request.urlretrieve(
            "https://github.com/TgCatUB/CatUserbot-Resources/raw/master/Resources/Spotify/cat.png",
            logo,
        )
    if not os.path.exists(font_mid):
        urllib.request.urlretrieve(
            "https://github.com/TgCatUB/CatUserbot-Resources/blob/master/Resources/Spotify/GoogleSans-Medium.ttf?raw=true",
            font_mid,
        )
    if not os.path.exists(font_bold):
        urllib.request.urlretrieve(
            "https://github.com/TgCatUB/CatUserbot-Resources/blob/master/Resources/Spotify/ArialUnicodeMS.ttf?raw=true",
            font_bold,
        )
    return logo, font_bold, font_mid


def sp_data(API):
    oauth = {"Authorization": "Bearer " + SP_DATABASE.return_token()}
    spdata = requests.get(API, headers=oauth)
    if spdata.status_code == 401:
        data = {
            "client_id": SPOTIFY_CLIENT_ID,
            "client_secret": SPOTIFY_CLIENT_SECRET,
            "grant_type": "refresh_token",
            "refresh_token": SP_DATABASE.return_refresh(),
        }
        r = requests.post("https://accounts.spotify.com/api/token", data=data)
        received = r.json()
        # if a new refresh is token as well, we save it here
        try:
            SP_DATABASE.save_refresh(received["refresh_token"])
        except KeyError:
            pass
        SP_DATABASE.save_token(received["access_token"])
        glob_db.add_collection(
            "SP_DATA",
            {
                "data": {
                    "access_token": SP_DATABASE.return_token(),
                    "refresh_token": SP_DATABASE.return_refresh(),
                }
            },
        )
        spdata = requests.get(API, headers=oauth)
    return spdata


async def make_thumb(url, client, song, artist, now, full):
    pic_name = "./temp/cat.png"
    urllib.request.urlretrieve(url, pic_name)
    background = Image.open(pic_name).resize((1024, 1024))
    background = background.filter(ImageFilter.GaussianBlur(5))
    enhancer = ImageEnhance.Brightness(background)
    background = enhancer.enhance(0.5)
    logo, bfont, mfont = file_check()
    cat = Image.open(logo, "r").resize((int(1024 / 5), int(1024 / 5)))
    thumbmask = Image.new("RGBA", (1024, 1024), 0)
    thumbmask.paste(background, (0, 0))
    thumbmask.paste(cat, (-30, 840), mask=cat)
    thumb_lay = ellipse_layout_create(pic_name, 1.5, 40)
    thumbmask.paste(thumb_lay, (170, 30), thumb_lay)
    thumb, x = ellipse_create(pic_name, 1.6, 0)
    thumbmask.paste(thumb, (191, 52), thumb)
    try:
        photos = await client.get_profile_photos(client.uid)
        myphoto = await client.download_media(photos[0])
    except IndexError:
        myphoto = urllib.request.urlretrieve(
            "https://github.com/TgCatUB/CatUserbot-Resources/raw/master/Resources/Spotify/SwagCat.jpg"
        )
    user_lay = ellipse_layout_create(myphoto, 6, 30)
    thumbmask.paste(user_lay, (700, 450), user_lay)
    user, x = ellipse_create(myphoto, 7.5, 0)
    thumbmask.paste(user, (717, 467), user)
    if len(song) > 18:
        song = f"{song[:18]}..."
    text_draw(mfont, 30, thumbmask, "NOW PLAYING", 745)
    text_draw(bfont, 80, thumbmask, song, 772, stroke_width=1, stroke_fill="white")
    text_draw(
        bfont, 38, thumbmask, f"by {artist}", 870, stroke_width=1, stroke_fill="white"
    )
    text_draw(mfont, 35, thumbmask, f"{now} | {full}", 925)
    thumbmask.save(pic_name)
    os.remove(myphoto)
    return pic_name


@catub.cat_cmd(
    pattern="spnow$",
    command=("spnow", plugin_category),
    info={
        "header": "To fetch scrobble data from spotify",
        "description": "Shows currently playing song. If spbio is on then it send song preview",
        "usage": "{tr}spnow",
    },
)
async def spotify_now(event):
    "Spotify Now Playing"
    if not await sp_var_check(event):
        return
    msg_id = await reply_id(event)
    catevent = await edit_or_reply(event, "🎶 `Fetching...`")
    r = sp_data("https://api.spotify.com/v1/me/player/currently-playing")
    if r.status_code == 204:
        return await edit_delete(
            catevent, "\n**I'm not listening anything right now  ;)**"
        )
    try:
        if SP_DATABASE.SPOTIFY_MODE:
            info = f"🎶 Vibing ; [{spotify_bio.title}]({spotify_bio.link}) - {spotify_bio.interpret}"
            return await edit_or_reply(event, info, link_preview=True)
        dic = {}
        received = r.json()
        if received["currently_playing_type"] == "track":
            dic["title"] = received["item"]["name"]
            dic["progress"] = ms_converter(received["progress_ms"])
            dic["interpret"] = received["item"]["artists"][0]["name"]
            dic["duration"] = ms_converter(received["item"]["duration_ms"])
            dic["link"] = received["item"]["external_urls"]["spotify"]
            dic["image"] = received["item"]["album"]["images"][1]["url"]
            tittle = dic["title"]
            regx = re.search(r"([^(-]+) [(-].*", tittle)
            if regx:
                tittle = regx.group(1)
            thumb = await make_thumb(
                dic["image"],
                catub,
                tittle,
                dic["interpret"],
                dic["progress"],
                dic["duration"],
            )
            lyrics, symbol = telegraph_lyrics(tittle, dic["interpret"])
            await catevent.delete()
        button_format = f'**🎶 Track :- ** `{tittle}`\n**🎤 Artist :- ** `{dic["interpret"]}` <media:{thumb}> [🎧 Spotify]<buttonurl:{dic["link"]}>[{symbol} Lyrics]<buttonurl:{lyrics}:same>'
        await make_inline(button_format, event.client, event.chat_id, msg_id)
        os.remove(thumb)
    except KeyError:
        await edit_delete(
            catevent, "\n**Strange!! Try after restaring Spotify once ;)**", 7
        )


@catub.cat_cmd(
    pattern="spinfo$",
    command=("spinfo", plugin_category),
    info={
        "header": "To fetch Info of current spotify user",
        "description": "Shows user info, if any songs playing then show device also. ",
        "usage": "{tr}spinfo",
    },
)
async def spotify_now(event):
    "Spotify Info"
    if not await sp_var_check(event):
        return
    dic = {}
    x = sp_data("https://api.spotify.com/v1/me")
    y = sp_data("https://api.spotify.com/v1/me/player/devices")
    uinfo = x.json()
    device = y.json()
    if x.status_code == 200:
        dic["id"] = uinfo["id"]
        dic["name"] = uinfo["display_name"]
        try:
            dic["img"] = uinfo["images"][0]["url"]
        except IndexError:
            dic["img"] = None
        dic["url"] = uinfo["external_urls"]["spotify"]
        dic["followers"] = uinfo["followers"]["total"]
        dic["country"] = uinfo["country"]
        result = f'[\u2063]({dic["img"]})**Name :- [{dic["name"]}]({dic["url"]})\nCountry :-** `{dic["country"]}`\n**Followers :-** `{dic["followers"]}`\n**User Id :-** `{dic["id"]}`\n'
    if y.status_code == 200 and device["devices"]:
        for i in device["devices"]:
            if i["is_active"]:
                result += f'**Device :-** `{i["name"]}` (__{i["type"]}__)\n'
    await edit_or_reply(event, result, link_preview=True)


@catub.cat_cmd(
    pattern="sprecent$",
    command=("sprecent", plugin_category),
    info={
        "header": "To fetch list of recently played songs",
        "description": "Shows 15 recently played songs form spotify",
        "usage": "{tr}sprecent",
    },
)
async def spotify_now(event):
    "Spotify recently played songs"
    if not await sp_var_check(event):
        return
    x = sp_data("https://api.spotify.com/v1/me/player/recently-played?limit=15")
    if x.status_code == 200:
        song = "__**Spotify last played songs :-**__\n\n"
        songs = x.json()
        for i in songs["items"]:
            tittle = i["track"]["name"]
            regx = re.search(r"([^(-]+) [(-].*", tittle)
            if regx:
                tittle = regx.group(1)
            song += f"**◉ [{tittle} - {i['track']['artists'][0]['name']}]({i['track']['external_urls']['spotify']})**\n"
    await edit_or_reply(event, song)


@catub.cat_cmd(
    pattern="(i|)now(?:\s|$)([\s\S]*)",
    command=("now", plugin_category),
    info={
        "header": "To get song from spotify",
        "description": "Send the currently playing song of spotify or song from a spotify link.",
        "flags": {
            "i": "To send song song link as button",
        },
        "usage": [
            "{tr}now",
            "{tr}inow",
            "{tr}now <Spotify/Deezer link>",
            "{tr}inow <Spotify/Deezer link>",
        ],
    },
)
async def spotify_now(event):
    "Send spotify song"
    chat = "@DeezerMusicBot"
    msg_id = await reply_id(event)
    cmd = event.pattern_match.group(1).lower()
    link = event.pattern_match.group(2)
    catevent = await edit_or_reply(event, "🎶 `Fetching...`")
    if link:
        cap = f"<b>Spotify :- <a href = {link}>Link</a></b>"
        if not url(link) and "spotify" not in link:
            return await edit_delete(catevent, "**Give me a correct link...**")
    elif not link:
        if not await sp_var_check(event):
            return
        r = sp_data("https://api.spotify.com/v1/me/player/currently-playing")
        if r.status_code == 204:
            return await edit_delete(
                catevent, "\n**I'm not listening anything right now  ;)**"
            )
        try:
            received = r.json()
            if received["currently_playing_type"] == "track":
                title = received["item"]["name"]
                link = received["item"]["external_urls"]["spotify"]
                cap = f"<b>Spotify :- <a href = {link}>{title}</a></b>"
        except KeyError:
            return await edit_delete(
                catevent, "\n**Strange!! Try after restaring Spotify once ;)**"
            )
    async with event.client.conversation(chat) as conv:
        try:
            purgeflag = await conv.send_message("/start")
        except YouBlockedUserError:
            await catub(unblock("DeezerMusicBot"))
            purgeflag = await conv.send_message("/start")
        await conv.get_response()
        await event.client.send_read_acknowledge(conv.chat_id)
        await conv.send_message(link)
        song = await conv.get_response()
        await event.client.send_read_acknowledge(conv.chat_id)
        await catevent.delete()
        if cmd == "i":
            songg = await catub.send_file(BOTLOG_CHATID, song)
            fetch_songg = await catub.tgbot.get_messages(BOTLOG_CHATID, ids=songg.id)
            btn_song = await catub.tgbot.send_file(
                BOTLOG_CHATID, fetch_songg, buttons=Button.url("🎧 Spotify", link)
            )
            fetch_btn_song = await catub.get_messages(BOTLOG_CHATID, ids=btn_song.id)
            await event.client.forward_messages(event.chat_id, fetch_btn_song)
            await songg.delete()
            await btn_song.delete()
        else:
            await event.client.send_file(
                event.chat_id,
                song,
                caption=cap,
                parse_mode="html",
                reply_to=msg_id,
            )
        await delete_conv(event, chat, purgeflag)
