# Setup

{% hint style="info" %}
**Good to know:** Storybook canvas embeds don't just work great for live components, you can also embed things like icons, or your color palette or typography tokens just as easily!
{% endhint %}



## 〣 `ALIVE_NAME`:

a string variable that contains the name of the userbot or chatbot to be displayed in the "alive" status message. The value of this variable can be set as an environment variable or manually in the code.

## 〣 `ANTISPAMBOT_BAN`:

A boolean value that indicates whether SpamWatch, CAS, and SpamProtection ban is needed or not.

## 〣 `ANTI_FLOOD_WARN_MODE`:

An instance of ChatBannedRights that represents anti-flood measures. This variable is used to set the rights that a user has when they are temporarily banned for flooding the chat. The ChatBannedRights object is set with until\_date set to None, view\_messages set to None, and send\_messages set to True.

## 〣 `BADCAT`:

a boolean variable that determines whether the userbot should load "badcat" plugins, which may contain offensive or NSFW content. This value can be set as an environment variable or manually in the code.

## 〣 `BADCAT_REPO`:

This variable is used to specify the URL of a GitHub repository that contains some CatPlugins. If the BADCAT\_REPO environment variable is not set or the URL is invalid, then the default value "https\`: //github.com/TgCatUB/CatPlugins" is used.

## 〣 `BADCAT_REPOBRANCH`:

This variable is used to specify the branch of the BADCAT\_REPO repository that should be used. If the BADCAT\_REPOBRANCH environment variable is not set, then the default value "badcat" is used.

## 〣 `CHROME_BIN`:

A string value that represents the path to the Google Chrome binary. This variable is used by the Python program to launch a headless Chrome browser. The default value is /app/.apt/usr/bin/google-chrome, but you can override it by setting an environment variable named CHROME\_BIN.

## 〣 `CHROME_DRIVER`:

A string value that represents the path to the ChromeDriver executable. This variable is used by the Python program to control the headless Chrome browser. The default value is /app/.chromedriver/bin/chromedriver, but you can override it by setting an environment variable named CHROME\_DRIVER.

## 〣 `COMMAND_HAND_LER`:

A string value that represents the regex pattern for the command handler that should be used for the plugins.

## 〣 `COUNTRY`:

A string value that represents the name of a country. This variable is used by the Python program to set the timezone of the system clock. The default value is an empty string, but you can set it to the name of a country by specifying an environment variable named COUNTRY.

## 〣 `CURRENCY_API`:

A string value that represents the API key for the Currency Converter API. This API can be used to convert currencies. The API key can be obtained for free from the Currency Converter website.

## 〣 `DEEP_AI`:

A string value that represents an API key for the DeepAI service. This key is used to authenticate the Python program with the DeepAI service so that it can perform actions like generating text or images. To obtain this value, you need to sign up for a DeepAI account and store your API key as an environment variable named DEEP\_AI.

## 〣 `EXTERNAL_REPO`:

a string variable that contains the link to an external repository where additional plugins or modules for the userbot can be found. This value can be set as an environment variable or left empty.

## 〣 `EXTERNAL_REPOBRANCH`:

A string value that represents the name of a branch in an external GitHub repository. This variable is used by a plugin to determine which branch to use when fetching code from the external repository. The default value is main, but you can set it to a different value by specifying an environment variable named EXTERNAL\_REPOBRANCH.

## 〣 `FBAN_GROUP_ID`:

An integer value that represents the ID of the group that the bot should use for working with fban/unfban/superfban/superunfban commands.

## 〣 `FINISHED_PROGRESS_STR`:

A string value that represents the progress bar progress when it is finished.

## 〣 `GENIUS_API_TOKEN`:

A string value that represents the API key for the Genius API. This API can be used to retrieve lyrics and other information about songs. The API key can be obtained for free from the Genius website.

## 〣 `GITHUB_ACCESS_TOKEN`:

A string value that represents an access token for the GitHub API. This token is used to authenticate the Python program with the GitHub API so that it can perform actions like fetching data or creating issues. To obtain this value, you need to create a personal access token on GitHub and store it as an environment variable named GITHUB\_ACCESS\_TOKEN.

## 〣 `GIT_REPO_NAME`:

A string value that represents the name of a GitHub repository. This value is used by the Python program to identify the repository that it will work with. To obtain this value, you need to specify the name of the repository as an environment variable named GIT\_REPO\_NAME.

## 〣 `G_DRIVE_CLIENT_ID`:

A string value that represents the client ID for the Google Drive plugin. This value is used to authenticate and authorize the plugin to access the Google Drive account. You can obtain this value by creating a project on the Google Cloud Console and enabling the Google Drive API.

## 〣 `G_DRIVE_CLIENT_SECRET`:

A string value that represents the client secret for the Google Drive plugin. This value is used in conjunction with the client ID to authenticate and authorize the plugin. You can obtain this value from the same Google Cloud Console project where you obtained the client ID.

## 〣 `G_DRIVE_FOLDER_ID`:

A string value that represents the ID of the Google Drive folder that the plugin interacts with. This value is used to specify the folder where the plugin will upload or download files to/from. You can obtain this value from the Google Drive web interface by right-clicking on the desired folder and selecting "Get shareable link". The ID is the string of characters between "id=" and "&" in the link.

## 〣 `HEROKU_API_KEY`:

A string value that represents the API key for the Heroku plugin. You can obtain this value from the Heroku dashboard.

## 〣 `HEROKU_APP_NAME`:

A string value that represents the name of the app that you gave for the Heroku plugin.

## 〣 `IBM_WATSON_CRED_PASSWORD`:

A string value that represents the password for the IBM Watson speech-to-text plugin. You can obtain this value from the IBM Watson website.

## 〣 `IBM_WATSON_CRED_URL`:

A string value that represents the URL for the IBM Watson speech-to-text plugin. You can obtain this value from the IBM Watson website.

## 〣 `IPDATA_API`:

A string value that represents the API key for the ipdata.co API. This API can be used to retrieve geolocation information for an IP address. The API key can be obtained for free from the ipdata.co website.

## 〣 `LASTFM_API`:

A string value that represents the API key for the Last.fm plugin. This value is used to authenticate and authorize the plugin to access the Last.fm API. You can obtain this value by creating an account on the Last.fm website and generating an API key from the settings page.

## 〣 `LASTFM_PASSWORD`:

A string value that represents the password for the Last.fm account that the plugin interacts with. This value is used to authenticate the plugin to the Last.fm API on behalf of the specified user.

## 〣 `LASTFM_SECRET`:

A string value that represents the API secret for the Last.fm plugin. This value is used in conjunction with the API key to authenticate and authorize the plugin. You can obtain this value from the same settings page where you generated the API key.

## 〣 `LASTFM_USERNAME`:

A string value that represents the username for the Last.fm account that the plugin interacts with. This value is used to specify the Last.fm user whose scrobbles will be tracked and displayed by the plugin.

## 〣 `NO_LOAD`:

A list of string values that represent the names of the plugins that should not be loaded in the userbot.

## 〣 `OCR_SPACE_API_KEY`:

A string value that represents the API key for the OCR.Space API. This API can be used to perform Optical Character Recognition (OCR) on images. The API key can be obtained for free from the OCR.Space website.

## 〣 `OPENAI_API_KEY`:

A string value that represents the API key for the OpenAI API. This value is used to authenticate and authorize the plugin to access the OpenAI API. You can obtain this value by creating an account on the OpenAI website and generating an API key from the dashboard.

## 〣 `OPEN_WEATHER_MAP_APPID`:

A string value that represents the APPID for the OpenWeatherMap API. This API can be used to retrieve weather information for a location. The APPID can be obtained for free from the OpenWeatherMap website.

## 〣 `OPEN_WEATHER_MAP_APPID`:

A string value that represents the APPID for the OpenWeatherMap API. You can obtain this value from the OpenWeatherMap website.

## 〣 `OWNER_ID`:

An integer value that represents the ID of the owner of the bot. This value is used to show the profile link of the given ID as the owner.

## 〣 `PLUGIN_CHANNEL`:

An integer value that represents the channel ID of your custom plugins.

## 〣 `PM_LOGGER_GROUP_ID`:

An integer value that represents the group ID to which the bot should send notifications about your tagged messages or PMs.

## 〣 `PRIVATE_CHANNEL_BOT_API_ID`:

An integer value that represents the channel ID of a private channel that the bot should use. This value is used by the .frwd command.

## 〣 `PRIVATE_GROUP_BOT_API_ID`:

An integer value that represents the group ID of a private group that the bot should use.

## 〣 `PRIVATE_GROUP_ID`:

An integer value that represents the ID of the private group that the bot should use. This value should be the same as PRIVATE\_GROUP\_BOT\_API\_ID if you need pmguard.

## 〣 `REM_BG_API_KEY`:

A string value that represents the API key for the Remove.bg API. This API can be used to remove the background from an image. The API key can be obtained for free from the Remove.bg website.

## 〣 `SCREEN_SHOT_LAYER_ACCESS_KEY`:

A string value that represents the access key for the screenshot layer API. You can obtain this value from the screenshot layer website.

## 〣 `SPAMWATCH_API`:

A string value that represents the API key for the SpamWatch API. This value is used to authenticate and authorize the plugin to access the SpamWatch API. You can obtain this value by creating an account on the SpamWatch website and generating an API key from the dashboard.

## 〣 `SPOTIFY_CLIENT_ID`:

A string value that represents the client ID for the Spotify API. This value is used to authenticate and authorize the plugin to access the Spotify API. You can obtain this value by creating an app on the Spotify Developer Dashboard and copying the client ID from the app settings.

## 〣 `SPOTIFY_CLIENT_SECRET`:

A string value that represents the client secret for the Spotify API. This value is used in conjunction with the client ID to authenticate and authorize the plugin. You can obtain this value from the same app settings where you copied the client ID.

## 〣 `SUDO_COMMAND_HAND_LER`:

A string value that represents the regex pattern for the command handler that should be used for the sudo plugins.

## 〣 `TELEGRAPH_SHORT_NAME`:

A string value that represents the required name for the Telegraph plugin.

## 〣 `TEMP_DIR`:

A string value that represents the required folder path to act as the temporary folder.

## 〣 `TG_2STEP_VERIFICATION_CODE`:

A string value that represents the two-step verification code required for accessing the Telegram API. This value is used by the transfer channel plugin to authenticate the user's Telegram account. You can obtain this code by enabling two-step verification on your Telegram account and entering the code when prompted.

## 〣 `THUMB_IMAGE`:

A string value that represents the URL of the required thumb image for the Telegraph plugin.

## 〣 `TMP_DOWNLOAD_DIRECTORY`:

A string value that represents the required folder path to act as the download folder.

## 〣 `TZ`:

a string variable that contains the timezone of the user or server running the userbot. This value can be obtained from a timezone conversion website or set as an environment variable.

## 〣 `TZ_NUMBER`:

An integer value that represents the number of hours offset from UTC. This variable is used by the Python program to set the timezone of the system clock. The default value is 1, but you can set it to a different value by specifying an environment variable named TZ\_NUMBER.

## 〣 `UNFINISHED_PROGRESS_STR`:

A string value that represents the progress bar progress when it is unfinished.

## 〣 `UPSTREAM_REPO`:

a string variable that contains the link to the repository where the userbot's main code is hosted. This value can be set as an environment variable or manually in the code.

## 〣 `UPSTREAM_REPO_BRANCH`:

A string value that represents the name of a branch in a GitHub repository. This variable is used by a plugin to determine which branch to use when updating the Python program. The default value is master, but you can set it to a different value by specifying an environment variable named UPSTREAM\_REPO\_BRANCH.

## 〣 `VCMODE`:

a boolean variable that determines whether the userbot should enable voice chat mode. This value can be set as an environment variable or manually in the code.

## 〣 `VC_REPO`:

This variable is used to specify the URL of a GitHub repository that contains some CatVCPlayer. If the VC\_REPO environment variable is not set or the URL is invalid, then the default value "https\`: //github.com/TgCatUB/CatVCPlayer" is used.

## 〣 `VC_REPOBRANCH`:

This variable is used to specify the branch of the VC\_REPO repository that should be used. If the VC\_REPOBRANCH environment variable is not set, then the default value "test" is used.

## 〣 `VC_SESSION`:

a string variable that contains the session string for the userbot's voice chat mode. This value can be set as an environment variable or left empty.

## 〣 `WATCH_COUNTRY`:

A string value that represents the country for the JustWatch plugin. This value is used to specify the country where the plugin will search for TV shows and movies. The default value is "IN" for India, but you can change it to any other country code supported by JustWatch.













![Design byJoanne Macon Dribbble](https://dribbble.com/shots/9515799-Personal-Brand-Logo?utm\_source=Clipboard\_Shot\&utm\_campaign=jmvc\&utm\_content=Personal%20Brand%20Logo\&utm\_medium=Social\_Share\&utm\_source=Clipboard\_Shot\&utm\_campaign=jmvc\&utm\_content=Personal%20Brand%20Logo\&utm\_medium=Social\_Share)
