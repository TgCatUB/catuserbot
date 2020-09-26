import heroku3

from userbot.Config import Config

try:
    if Config.HEROKU_APP_NAME not in heroku3.from_key(Config.HEROKU_API_KEY).apps():
        raise Exception(f"Invalid HEROKU_APP_NAME  {Config.HEROKU_APP_NAME}")
except Exception as e:
    print(str(e))
