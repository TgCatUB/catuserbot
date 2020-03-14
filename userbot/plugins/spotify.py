import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
from asyncio import sleep
from json import loads
from json.decoder import JSONDecodeError
from os import environ
from sys import setrecursionlimit

from requests import get
from telethon import events
from telethon.tl import functions, types
from telethon.tl.functions.account import UpdateProfileRequest


import spotify_token as st
from userbot.uniborgConfig import Config

# =================== CONSTANT ===================
SPO_BIO_ENABLED = "```Spotify Current Music to Bio enabled.```"
SPO_BIO_DISABLED = "```Spotify Current Music to Bio disabled. Bio is default now.```"
SPO_BIO_RUNNING = "```Spotify Current Music to Bio already running.```"
SPO_BIO_CONFIG_ERROR = "```Error.```"
ERROR_MSG = "```Module halted, Unexpected error.```"

USERNAME = Config.SPOTIFY_USERNAME
PASSWORD = Config.SPOTIFY_PASS

ARTIST = 0
SONG = 0

BIOPREFIX = Config.SPOTIFY_BIO_PREFIX

SPOTIFYCHECK = False
RUNNING = False
OLDEXCEPT = False
PARSE = False
# ================================================

async def get_spotify_token():
    sptoken = st.start_session(USERNAME, PASSWORD)
    access_token = sptoken[0]
    environ["spftoken"] = access_token


async def update_spotify_info():
    global ARTIST
    global SONG
    global PARSE
    global SPOTIFYCHECK
    global RUNNING
    global OLDEXCEPT
    oldartist = ""
    oldsong = ""
    while SPOTIFYCHECK:
        try:
            RUNNING = True
            spftoken = environ.get("spftoken", None)
            hed = {'Authorization': 'Bearer ' + spftoken}
            url = 'https://api.spotify.com/v1/me/player/currently-playing'
            response = get(url, headers=hed)
            data = loads(response.content)
            artist = data['item']['album']['artists'][0]['name']
            song = data['item']['name']
            OLDEXCEPT = False
            oldsong = environ.get("oldsong", None)
            if song != oldsong and artist != oldartist:
                oldartist = artist
                environ["oldsong"] = song
                spobio = BIOPREFIX + " 🎧: " + artist + " - " + song
                await borg(UpdateProfileRequest(about=spobio))
                environ["errorcheck"] = "0"
        except KeyError:
            errorcheck = environ.get("errorcheck", None)
            if errorcheck == 0:
                await update_token()
            elif errorcheck == 1:
                SPOTIFYCHECK = False
                await borg(UpdateProfileRequest(about=Config.DEFAULT_BIO))
                print(ERROR_MSG)
                if Config.LOGGER:
                    await borg.send_message(
                        Config.PM_LOGGR_BOT_API_ID,
                        ERROR_MSG)
        except JSONDecodeError:
            OLDEXCEPT = True
            await sleep(6)
            await borg(UpdateProfileRequest(about=Config.DEFAULT_BIO))
        except TypeError:
            await dirtyfix()
        SPOTIFYCHECK = False
        await sleep(2)
        await dirtyfix()
    RUNNING = False


async def update_token():
    sptoken = st.start_session(USERNAME, PASSWORD)
    access_token = sptoken[0]
    environ["spftoken"] = access_token
    environ["errorcheck"] = "1"
    await update_spotify_info()


async def dirtyfix():
    global SPOTIFYCHECK
    SPOTIFYCHECK = True
    await sleep(4)
    await update_spotify_info()

@borg.on(events.NewMessage(pattern=r"\.enablespotify ?(.*)", outgoing=True))
async def set_biostgraph(setstbio):
    setrecursionlimit(700000)
    if not SPOTIFYCHECK:
        environ["errorcheck"] = "0"
        await setstbio.edit(SPO_BIO_ENABLED)
        await get_spotify_token()
        await dirtyfix()
    else:
        await setstbio.edit(SPO_BIO_RUNNING)

@borg.on(events.NewMessage(pattern=r"\.disablespotify ?(.*)", outgoing=True))
async def set_biodgraph(setdbio):
    global SPOTIFYCHECK
    global RUNNING
    SPOTIFYCHECK = False
    RUNNING = False
    await borg(UpdateProfileRequest(about=Config.DEFAULT_BIO))
    await setdbio.edit(SPO_BIO_DISABLED)
