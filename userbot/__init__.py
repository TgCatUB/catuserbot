import time

import heroku3

from .Config import Config
from .core import logger
from .core.session import catub

__version__ = "3.0.0"
__license__ = "GNU Affero General Public License v3.0"
__author__ = "CatUserBot <https://github.com/sandy1709/catuserbot>"
__copyright__ = "CatUserBot Copyright (C) 2020 - 2021  " + __author__

catub.version = __version__
catub.tgbot.version = __version__
bot = catub

StartTime = time.time()
catversion = "3.0.0"

if Config.UPSTREAM_REPO == "goodcat":
    UPSTREAM_REPO_URL = "https://github.com/sandy1709/catuserbot"
elif Config.UPSTREAM_REPO == "badcat":
    UPSTREAM_REPO_URL = "https://github.com/Jisan09/catuserbot"
else:
    UPSTREAM_REPO_URL = Config.UPSTREAM_REPO

if Config.PRIVATE_GROUP_BOT_API_ID == 0:
    BOTLOG = False
    BOTLOG_CHATID = "me"
else:
    BOTLOG = True
    BOTLOG_CHATID = Config.PRIVATE_GROUP_BOT_API_ID

try:
    if Config.HEROKU_API_KEY is not None or Config.HEROKU_APP_NAME is not None:
        HEROKU_APP = heroku3.from_key(Config.HEROKU_API_KEY).apps()[
            Config.HEROKU_APP_NAME
        ]
    else:
        HEROKU_APP = None
except Exception:
    HEROKU_APP = None


# Global Configiables
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
