import logging
import os
import sys
from pathlib import Path
from telethon.sessions import StringSession
from telethon import TelegramClient

ENV = bool(os.environ.get("ENV", False))
if ENV:
    from heroku_config import Var
else:
    if os.path.exists("config.py"):
        from local_config import Development as Var
    else:
        logging.warning("No local_config.py Found!")
        logging.info("Please run the command, again, after creating local_config.py similar to README.md")
        sys.exit(1)

import userbot.__init__
import userbot.__main__

