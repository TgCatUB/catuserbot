from sample_config import Config


class Development(Config):
    # get this values from the my.telegram.org
    APP_ID = 9406309
    API_HASH = "38446d78262fab1a64662a3ae149403e"
    # the name to display in your alive message
    ALIVE_NAME = "Amn_hshdh"
    # create any PostgreSQL database (i recommend to use elephantsql) and paste that link here
    DB_URI = "postgres://ucjrevjy:moaXV2VNQSyNd-AwTWGzCoC4gPcdXLVX@berry.db.elephantsql.com/ucjrevjy"
    # After cloning the repo and installing requirements do python3 stringsetup.py an fill that value with this
    STRING_SESSION = "1BJWap1wBuxwb8lx-P8XvqprKZrfgCgVOd_8XBDuMSGV_9xTppmhW4uUMCyIDfVxYZnaG-ubaH-fhSdKTc-VKE3s190Ded6ZpS80RcgPg9lWwpGvmEYprB40GeEcqFPwbl_rlMd9UslwOYRY_8ScGioZ4P50RneO-cE5iMFuAZf-SDixRKDq4afOhg_CpSwxLOlCyd4vvsny3Ehv279N6HqZgq8ydgCnwCc3RWqTN2Yu5lzLhW6Q55iWzTGNMbcHwZ3O6SZ7dVUcs32kidgmDorjSzwePHoQSNjpZiTI-ZSEN2WgsyYnQSdRyyuMKIWnIeCAuJFsmwbieKKGda3J50sWdi0l9aHQ="
    # create a new bot in @botfather and fill the following vales with bottoken
    TG_BOT_TOKEN = "6033162481:AAEcsOSh-7N5mYVepYSP50_0L5JPONSSv0o"
    # create a private group and a rose bot to it and type /id and paste that id here (replace that -100 with that group id)
    PRIVATE_GROUP_BOT_API_ID = -100
    # command handler
    COMMAND_HAND_LER = "."
    # command hanler for sudo
    SUDO_COMMAND_HAND_LER = "."
    # External plugins repo
    EXTERNAL_REPO = "https://github.com/TgCatUB/CatPlugins"
    # if you need badcat plugins set "True"
    BADCAT = "False"
