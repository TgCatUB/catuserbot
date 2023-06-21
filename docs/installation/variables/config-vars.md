# 📕 Config Vars

## ≡ Mandatory Vars

> **To host bot these are must needed, else bot wouldn't start**

### 〣 `APP_ID` & `API_HASH`

<details>

<summary>Generate</summary>

1. Go to [**my.telegram.org**](https://my.telegram.org/)
2. Enter your phone number in international format. Example : `+91987456321`
3. Enter the web login code sent to you by Telegram in app.
4. After successful sign in , Click on `API development tools`
5. Enter `App Title` & `Short name` and create app.

</details>

### 〣 `STRING_SESSION`

<details>

<summary>Generate</summary>

You can generate String several ways:

**➦ Locally**

{% code title="Run this inside catuserbot directory" overflow="wrap" %}
```batch
pip3 install git+https://github.com/jisan09/Telethon && python3 stringsetup.py
```
{% endcode %}

#### **➦ Telegram Bot : **<mark style="color:blue;">**@CatSessionBot**</mark> in telegram: [**https://t.me/CatStringSessionBot**](https://t.me/CatStringSessionBot)

#### **➦ Repl :** [**https://generatestringsession.sandeep1709.repl.run/**](https://generatestringsession.sandeep1709.repl.run/)

</details>

### 〣 `TG_BOT_TOKEN`

<details>

<summary>Generate</summary>

1. Go to <mark style="color:blue;">**@BotFather**</mark> in telegram : [**https://t.me/BotFather**](https://t.me/BotFather)
2. Start the bot then send `/new_bot`
3. Enter name for your bot & username

The bot will send token after that.

**While in botfather turn on inline permission also, for the bot you created**

1. `/mybot`
2. Click on your bot name
3. Bot Settings
4. Inline Mode
5. Turn on

</details>

### 〣 `DB_URI`

{% tabs %}
{% tab title="Local Database" %}
{% code title="First install postgres" overflow="wrap" %}
```batch
sudo apt install postgresql postgresql-contrib
```
{% endcode %}

{% code title="Then run this in terminal" overflow="wrap" %}
```batch
sudo su - postgres bash -c "psql -c \"ALTER USER postgres WITH PASSWORD 'your_password';\" && createdb catuserbot -O postgres"
```
{% endcode %}

{% code title="Your DB_URI will be" overflow="wrap" %}
```batch
postgresql://postgres:your_password@localhost:5432/catuserbot
```
{% endcode %}
{% endtab %}

{% tab title="Elephant Sql" %}
**Visit** [**https://www.elephantsql.com/**](https://www.elephantsql.com/) **and get your DB\_URI**

{% embed url="https://youtu.be/zlPCUzocwHw" %}
Elephant SQL
{% endembed %}
{% endtab %}
{% endtabs %}

## ≡ Extra Plugins Related Variables

### 〣 `BADCAT`

A boolean variable \[ <mark style="color:green;">True</mark> / <mark style="color:green;">False</mark> ] that determines whether the userbot should load "badcat" plugins, which contain offensive or NSFW content.

### 〣 `EXTERNAL_REPO`

A string variable that contains the link to an external repository where additional plugins , modules for the userbot can be found. The default value is [<mark style="color:blue;">https://github.com/TgCatUB/CatPlugins</mark>](https://github.com/TgCatUB/CatPlugins) .

### 〣 `EXTERNAL_REPOBRANCH`

A string value that represents the name of a branch in an external GitHub repository. This variable is used by a plugin to determine which branch to use when fetching code from the external repository. The default value is <mark style="color:blue;">main</mark>.

### 〣 `UPSTREAM_REPO`

A string variable that contains the link to the repository where the userbot's main code is hosted. The default value is [<mark style="color:blue;">https://github.com/TgCatUB/catuserbot</mark>](https://github.com/TgCatUB/catuserbot) .

### 〣 `UPSTREAM_REPO_BRANCH`

A string value that represents the name of a branch in a GitHub repository. This variable is used by a plugin to determine which branch to use when updating the bot. The default value is <mark style="color:blue;">master</mark>.

### 〣 `VCMODE`

A boolean variable \[ <mark style="color:green;">True</mark> / <mark style="color:green;">False</mark> ] that determines whether the userbot should enable voice chat mode.

### 〣 `VC_SESSION`

A string variable that contains the session string for the userbot's voice chat mode. This used for playing music in VC using different account. Make using [<mark style="color:blue;">this tutorial</mark>](config-vars.md#string\_session) .

## ≡ Google Related Variables

### 〣 `CHROME_BIN`

A string value that represents the path to the Google Chrome binary. This variable is used by the Python program to launch a headless Chrome browser. The default value is <mark style="color:green;">/app/.apt/usr/bin/google-chrome</mark>

### 〣 `CHROME_DRIVER`

A string value that represents the path to the ChromeDriver executable. This variable is used by the Python program to control the headless Chrome browser. The default value is <mark style="color:green;">/app/.chromedriver/bin/chromedriver</mark>

### 〣 `G_DRIVE_CLIENT_ID`

A string value that represents the client ID for the Google Drive plugin. This value is used to authenticate and authorize the plugin to access the Google Drive account. You can obtain this value by creating a project on the Google Cloud Console and enabling the Google Drive API.\
Refer [**G-drive tutorial**](../../tutorials/g-drive.md) for getting the values.

### 〣 `G_DRIVE_CLIENT_SECRET`

A string value that represents the client secret for the Google Drive plugin. This value is used in conjunction with the client ID to authenticate and authorize the plugin. You can obtain this value from the same Google Cloud Console project where you obtained the client ID.

### 〣 `G_DRIVE_FOLDER_ID`

A string value that represents the ID of the Google Drive folder that the plugin interacts with. This value is used to specify the folder where the plugin will upload or download files to/from. You can obtain this value from the Google Drive web interface by right-clicking on the desired folder and selecting "Get shareable link". The ID is the string of characters between "id=" and "&" in the link.

## ≡ Music Related Variables

### 〣 `GENIUS_API_TOKEN`

A string value that represents the API key for the Genius API. This API can be used to retrieve lyrics and other information about songs. The API key can be obtained for free from the Genius website.

### 〣 `SPOTIFY_CLIENT_ID`

A string value that represents the client ID for the Spotify API. This value is used to authenticate and authorize the plugin to access the Spotify API. You can obtain this value by creating an app on the Spotify Developer Dashboard and copying the client ID from the app settings.\
Refer [**Spotify tutorial**](../../tutorials/spotify.md) for getting the values.

### 〣 `SPOTIFY_CLIENT_SECRET`

A string value that represents the client secret for the Spotify API. This value is used in conjunction with the client ID to authenticate and authorize the plugin. You can obtain this value from the same app settings where you copied the client ID.

### 〣 `LASTFM_API`

A string value that represents the API key for the Last.fm plugin. This value is used to authenticate and authorize the plugin to access the Last.fm API. You can obtain this value by creating an account on the Last.fm website and generating an API key from the settings page.\
Refer [**LastFM tutorial**](../../tutorials/lastfm.md) for getting the values.

### 〣 `LASTFM_PASSWORD`

A string value that represents the password for the Last.fm account that the plugin interacts with. This value is used to authenticate the plugin to the Last.fm API on behalf of the specified user.

### 〣 `LASTFM_SECRET`

A string value that represents the API secret for the Last.fm plugin. This value is used in conjunction with the API key to authenticate and authorize the plugin. You can obtain this value from the same settings page where you generated the API key.

### 〣 `LASTFM_USERNAME`

A string value that represents the username for the Last.fm account that the plugin interacts with. This value is used to specify the Last.fm user whose scrobbles will be tracked and displayed by the plugin.

### 〣 `IBM_WATSON_CRED_PASSWORD`

A string value that represents the password for the IBM Watson speech-to-text plugin. You can obtain this value from the IBM Watson website. Refer IBM tutorial for getting the values.\
Refer [**IBM Tutorial**](../../tutorials/ibm.md) for getting the values.

### 〣 `IBM_WATSON_CRED_URL`

A string value that represents the URL for the IBM Watson speech-to-text plugin. You can obtain this value from the IBM Watson website.

## ≡ Basic and Main Configuration Variables

### 〣 `ALIVE_NAME`

a string variable that contains the name of the userbot or chatbot to be displayed in the "alive" status message. The value of this variable can be set as an environment variable or manually in the code.

### 〣 `COMMAND_HAND_LER`

A string value that represents the regex pattern for the command handler that should be used for the plugins.

### 〣 `SUDO_COMMAND_HAND_LER`

A string value that represents the regex pattern for the command handler that should be used for the sudo plugins.

### 〣 `PLUGIN_CHANNEL`

An integer value that represents the channel ID of your custom plugins.

### 〣 `PM_LOGGER_GROUP_ID`

An integer value that represents the group ID to which the bot should send notifications about your tagged messages or PMs.

### 〣 `PRIVATE_CHANNEL_BOT_API_ID`

An integer value that represents the channel ID of a private channel that the bot should use. This value is used by the .frwd command.

### 〣 `PRIVATE_GROUP_BOT_API_ID`

An integer value that represents the group ID of a private group that the bot should use.

### 〣 `HEROKU_API_KEY`

A string value that represents the API key for the Heroku plugin. You can obtain this value from the Heroku dashboard.

### 〣 `HEROKU_APP_NAME`

A string value that represents the name of the app that you gave for the Heroku plugin.

### 〣 `NO_LOAD`

A list of string values that represent the names of the plugins that should not be loaded in the userbot.

### 〣 `THUMB_IMAGE`

A string value that represents the URL of the required thumb image for the Telegraph plugin.

### 〣 `TZ`

a string variable that contains the timezone of the user or server running the userbot. This value can be obtained from a timezone conversion website or set as an environment variable.

### 〣 ENV

A boolean variable \[ <mark style="color:green;">True</mark> / <mark style="color:green;">False</mark> ] that determines whether the userbot should lookup for configs in <mark style="color:green;">config.py</mark> or in <mark style="color:green;">app environment</mark>. Default it set to False .

## ≡ Additional Configuration Variables

### 〣 `GITHUB_ACCESS_TOKEN`

A string value that represents an access token for the GitHub API. This token is used to authenticate the Python program with the GitHub API so that it can perform actions like fetching data or creating issues.

Refer [**Github tutorial** ](../../tutorials/github-commit.md)to get the value.

### 〣 `GIT_REPO_NAME`

A string value that represents the name of a GitHub repository. This value is used by the Python program to identify the repository that it will work with. To obtain this value, you need to specify the name of the repository as an environment variable named GIT\_REPO\_NAME.

### 〣 `ANTISPAMBOT_BAN`

A boolean value that indicates whether SpamWatch, CAS, and SpamProtection ban is needed or not.

### 〣 `FBAN_GROUP_ID`

An integer value that represents the ID of the group that the bot should use for working with fban/unfban/superfban/superunfban commands.

### 〣 `SPAMWATCH_API`

A string value that represents the API key for the SpamWatch API. This value is used to authenticate and authorize the plugin to access the SpamWatch API. You can obtain this value by creating an account on the SpamWatch website and generating an API key from the dashboard.

### 〣 `COUNTRY`

A string value that represents the name of a country. This variable is used by the Python program to set the timezone of the system clock. The default value is an empty string, but you can set it to the name of a country by specifying an environment variable named COUNTRY.

### 〣 `TG_2STEP_VERIFICATION_CODE`

A string value that represents the two-step verification code required for accessing the Telegram API. This value is used by the transfer channel plugin to authenticate the user's Telegram account. You can obtain this code by enabling two-step verification on your Telegram account and entering the code when prompted.

### 〣 `TZ_NUMBER`

An integer value that represents the number of hours offset from UTC. This variable is used by the Python program to set the timezone of the system clock. The default value is 1, but you can set it to a different value by specifying an environment variable named TZ\_NUMBER.

### 〣 `WATCH_COUNTRY`

A string value that represents the country for the JustWatch plugin. This value is used to specify the country where the plugin will search for TV shows and movies. The default value is "IN" for India, but you can change it to any other country code supported by JustWatch.

## ≡ Other Api Variables

### 〣 `DEEP_AI`

A string value that represents an API key for the DeepAI service. This key is used to authenticate the Python program with the DeepAI service so that it can perform actions like detecting NSFW text or images. To obtain this value, you need to sign up for a DeepAI account and store your API key as an environment variable named DEEP\_AI.

### 〣 `CURRENCY_API`

A string value that represents the API key for the Currency Converter API. This API can be used to convert currencies. The API key can be obtained for free from the Currency Converter website.

### 〣 `IPDATA_API`

A string value that represents the API key for the ipdata.co API. This API can be used to retrieve geolocation information for an IP address. The API key can be obtained for free from the ipdata.co website.

### 〣 `OCR_SPACE_API_KEY`

A string value that represents the API key for the OCR.Space API. This API can be used to perform Optical Character Recognition (OCR) on images. The API key can be obtained for free from the OCR.Space website. Get your api key from [here](https://ocr.space/ocrapi)

### 〣 `OPENAI_API_KEY`

A string value that represents the API key for the OpenAI API. This value is used to authenticate and authorize the plugin to access the OpenAI API. You can obtain this value by creating an account on the OpenAI website and generating an API key from the dashboard.

### 〣 `OPEN_WEATHER_MAP_APPID`

A string value that represents the APPID for the OpenWeatherMap API. This API can be used to retrieve weather information for a location. The APPID can be obtained for free from the OpenWeatherMap website. Get your api from [openweathermap](https://home.openweathermap.org/api\_keys)

### 〣 `REM_BG_API_KEY`

A string value that represents the API key for the Remove.bg API. This API can be used to remove the background from an image. The API key can be obtained for free from the [Remove.bg](https://www.remove.bg/api) website.

### 〣 `SCREEN_SHOT_LAYER_ACCESS_KEY`

A string value that represents the access key for the screenshot layer API. You can obtain this value from the screenshot layer website.
