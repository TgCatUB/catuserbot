import logging
import os
import sys
from heroku_config.Var import STRING_SESSION, APP_ID, API_HASH
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

if STRING_SESSION is not None:
    session_name = str(STRING_SESSION)
    bot = TelegramClient(
        StringSession(session_name),
        APP_ID,
        API_HASH
    )
    import userbot.__main__.py
elif len(sys.argv) == 1:
    session_name = "startup"
    bot = TelegramClient(
        session_name,
        Var.APP_ID,
        Var.API_HASH
    )
    import userbot.__main__.py
else:
    logging.error("USAGE EXAMPLE:\n"
                  "python3 -m startup"
                  "\n 👆👆 Please follow the above format to run your userbot."
                  "\n Bot quitting.")
