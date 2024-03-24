from sample_config import Config


class Development(Config):
    # get this values from the my.telegram.org
    APP_ID = 14483301
    API_HASH = "b2c60a18d2d213a9056a3658ea684bf9"
    # the name to display in your alive message
    ALIVE_NAME = "mobiini"
    # create any PostgreSQL database (i recommend to use elephantsql) and paste that link here
    DB_URI = "postgres://xvlrbysq:KDq6uWKnqe-xn7G4tnWBaXKWNAXxU73z@castor.db.elephantsql.com/xvlrbysq"
    # After cloning the repo and installing requirements do python3 stringsetup.py an fill that value with this
    STRING_SESSION = "1BJWap1wBu7W-TidkNqVdD3Vb2CD3IMEe1fpWLhK_5xJXnyNnjvgo80uE3_9GX1W40HDXWsAPm6KjE7AmazKRFEUFNm-DR3MpGEW45rwoNA-WYRrOX6Xf8xZ39a6RaduvtBsWYfmkHa-uNuKVrOivD6UL7T8rhk_sD26yUYl6K_j5ij9SMgLOlFqLPnuG8MorlqQX8MLlAqW9AGuds9ixMk0ZZhSP0BTHAEDI4EVDvfo9K6gsS48sHp9fZwuNlRgWRxtVQFDHf9U5DHYzWGhDmpMhuhIaJDAF28j10PubcA4dtVStW2xyc2ATYfuKrCDE2gnwkdHzoW4Kenc_qqO_mBWl6CQo4Zk="
    # create a new bot in @botfather and fill the following vales with bottoken
    TG_BOT_TOKEN = "6883054061:AAGch0eOZfDMjko89MKVVh9gaJHz1sZbh_E"
    # create a private group and a rose bot to it and type /id and paste that id here (replace that -100 with that group id)
    PRIVATE_GROUP_BOT_API_ID = -1002103184784
    # command handler
    COMMAND_HAND_LER = "."
    # command hanler for sudo
    SUDO_COMMAND_HAND_LER = "."
    # External plugins repo
    EXTERNAL_REPO = "https://github.com/TgCatUB/CatPlugins"
    # if you need badcat plugins set "True"
    BADCAT = "true"
