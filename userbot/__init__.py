import os
import sys
from telethon.sessions import StringSession
from telethon import TelegramClient
from var import Var
from pylast import LastFMNetwork, md5
from logging import basicConfig, getLogger, INFO, DEBUG
from distutils.util import strtobool as sb
from pySmartDL import SmartDL
from dotenv import load_dotenv
from requests import get
import time
from userbot.helpers import fonts as fonts
from userbot.helpers import functions as catdef
from userbot.helpers import memeshelper as memes

StartTime = time.time()
catversion = "2.5.0"

if Var.STRING_SESSION:
    session_name = str(Var.STRING_SESSION)
    bot = TelegramClient(StringSession(session_name), Var.APP_ID, Var.API_HASH)
else:
    session_name = "startup"
    bot = TelegramClient(session_name, Var.APP_ID, Var.API_HASH)
    
UPSTREAM_REPO_URL = os.environ.get("UPSTREAM_REPO_URL","https://github.com/sandy1709/catuserbot.git")
ALIVE_NAME = os.environ.get("ALIVE_NAME", None)
AUTONAME = os.environ.get("AUTONAME", None)
DEFAULT_BIO = os.environ.get("DEFAULT_BIO", None)
LASTFM_API = os.environ.get("LASTFM_API", None)
LASTFM_SECRET = os.environ.get("LASTFM_SECRET", None)
LASTFM_USERNAME = os.environ.get("LASTFM_USERNAME", None)
LASTFM_PASSWORD_PLAIN = os.environ.get("LASTFM_PASSWORD", None)
LASTFM_PASS = md5(LASTFM_PASSWORD_PLAIN)
if LASTFM_API and LASTFM_SECRET and LASTFM_USERNAME and LASTFM_PASS:
        lastfm = LastFMNetwork(api_key=LASTFM_API,
                               api_secret=LASTFM_SECRET,
                               username=LASTFM_USERNAME,
                               password_hash=LASTFM_PASS)
else:
        lastfm = None


# Setting Up CloudMail.ru and MEGA.nz extractor binaries,
# and giving them correct perms to work properly.
if not os.path.exists('bin'):
    os.mkdir('bin')
    
binaries = {
    "https://raw.githubusercontent.com/yshalsager/megadown/master/megadown":
    "bin/megadown",
    "https://raw.githubusercontent.com/yshalsager/cmrudl.py/master/cmrudl.py":
    "bin/cmrudl"
}

for binary, path in binaries.items():
    downloader = SmartDL(binary, path, progress_bar=False)
    downloader.start()
    os.chmod(path, 0o755)


# Global Variables
COUNT_MSG = 0
USERS = {}
COUNT_PM = {}
LASTMSG = {}
CMD_HELP = {}
ISAFK = False
AFKREASON = None
CMD_LIST = {}
SUDO_LIST = {}
# for later purposes
INT_PLUG = ""
LOAD_PLUG = {}
