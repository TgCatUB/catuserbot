from sample_config import Config


class Development(Config):
    # get this values from the my.telegram.org
    APP_ID = 9406309
    API_HASH = "38446d78262fab1a64662a3ae149403e"
    # the name to display in your alive message
    ALIVE_NAME = "Amnhj"
    # create any PostgreSQL database (i recommend to use elephantsql) and paste that link here
    DB_URI = "postgres://ucjrevjy:moaXV2VNQSyNd-AwTWGzCoC4gPcdXLVX@berry.db.elephantsql.com/ucjrevjy"
    # After cloning the repo and installing requirements do python3 stringsetup.py an fill that value with this
    STRING_SESSION = "1BJWap1sBu65XAhs5zNkzHqcT99PqoWwjWlnX4t6PDTIg1zD5RdOXnFjedhPFPabglZnxs-5oJ8chDLZd9sHkEYRC5LbNIFWcbWSssVtq61wndSZtkjrDobFcJk_qf8yAX4ny_9vd3HweFJenHdaFbtZs2lyw4GVWJFQgiBMPhYz9DNXym5bt49Up7Oab6heSysBPPt_2opa6sgJSlqSd2QnrcPfBgUKqtX8dQgnlW9zNXYZtE20s5_0uLKVGPmPBF6K0vCsLP3pg8ZvurBfY4VidjbJLIljU73HkaSP2iP8PE5omxv9txbhTcPMcmlDl74OZgpF45_qkKxUdUYaWxBtfiYByslI="
    # create a new bot in @botfather and fill the following vales with bottoken
    TG_BOT_TOKEN = "6033162481:AAEcsOSh-7N5mYVepYSP50_0L5JPONSSv0o"
    # create a private group and a rose bot to it and type /id and paste that id here (replace that -100 with that group id)
    PRIVATE_GROUP_BOT_API_ID = -1001772756570
    # command handler
    COMMAND_HAND_LER = "."
    # command hanler for sudo
    SUDO_COMMAND_HAND_LER = "."
    # External plugins repo
    EXTERNAL_REPO = "https://github.com/TgCatUB/CatPlugins"
    # if you need badcat plugins set "True"
    BADCAT = "True"
