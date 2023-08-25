# 📄 Version 3.3.0

## ≡ Base Changes

* Changed the docker base image to `catub/catuserbot:latest`. Users can use `catub/base:bullseye` in case of blacklisting by changing the image name in the Dockerfile.
* Added a Docker Compose file with database support. Users can run the bot with a database, and if they don't set `DB_URI` in `config.py`, it will automatically make an SQLite database.
* Added new [Documentation](https://tgcatub.gitbook.io/catuserbot/) .
* Changed the plugin log style in `botlogger` to make it less spammy.
* Added logs support for VPS users (check `.help logs`).

## ≡ Breaking Changes

* Updated `Telethon` to the latest version and added spoiler media support globally. Users can enable it in `config.py` (`SPOILER_MEDIA = True`).
* Removed the old way of managing database var by using `db` (`.setdv`, `.getdv`, `.deldv`). Users can now manage them with var itself (`.set var`, `.get var`, `.del var`). The bot will decide whether to add them in the database or in `config.py`.

## ≡ Plugin Changes

### 〣 Security

* Fixed the issue where sudo users could upload the **config.py** file.
* Fixed issue where sudo users could scrap botlog config with eval.

### 〣 Reformatted

* Reformatted inline and added `vcplayer` there too (check `@your_bot_username`).
* Reformatted the log of `.eval` to make it more readable.
* Dumped `chatbot` for now, as no faster API was found for it.
* Revamped **google**, removed the old way of searching, and added the new way of searching with **Google Lens** (check `.help google`).
* Replaced **ray.so API** with **chromedriver**.

### 〣 Fixed

* Fixed **last.fm** config error on VPS.
* Fixed **autoprofile** error (after setting value, it was asking for the value again).
* Fixed **filesummary** round video error.
* Fixed **sangmata** now it can fetch name/username history.
* Fixed **stcr** giving an error while making a sticker.

### 〣 Added

* Added **musicmix** API with **genius** (fixes lyrics error for VPS users).
* Added **install to path** option in `.install`.
* Added more flags in **logs** (check `.help logs`).
* Added `.inspect` in **evaluators** (check `.help inspect`).
  * **aitools:** AI chatbot works without any API key (check `.help aitools`).
    * `gentxt`: Generate text response from a given text (using `thab` API).
    * `genimg`: Generate an image from a given text (using `somnium`).
  * **openai:** AI chatbot works with OpenAI API key (check `.help openai`).
    * `gpt`: Generate text response from a given text.
    * `dalle`: Generate an image from a given text.
  * **schedule:** Schedule messages with a database to any time (check `.help schedule`).
    * `schedule`: Schedule a message with date and time.
    * `autoschedule`: Schedule a message with day and time and repeat it.

## ≡ VC Player Changes

_We have revamped the VC Player with several new features and improvements to make it more user-friendly and functional._

### 〣 New Features

#### Song Searching by Name

With this update, you can now search for songs by their name and play them directly in the voice chat. This feature eliminates the need to provide the full URL of the song.

#### Stream link Support

The new VC Player now supports streaming. This feature allows users to play songs from YouTube directly in the voice chat without downloading before.

#### Inline Support

The updated VC Player comes with inline support, which allows users to send messages with buttons that control the VC Player. Users can now control the VC Player without having to type commands in the chat.

#### Bot Mode Support

We have added a bot mode feature that allows the bot to send messages instead of the user. This feature is useful when you want to hide the identity of the user controlling the VC Player.

#### Clean Mode Support

The updated VC Player now comes with clean mode support, which automatically deletes the message after the bot leaves the voice chat. This feature helps keep the chat clean and organized.

#### Auth Mode Support

We have added an auth mode feature that filters the users who can use the VC Player. This feature is useful when you want to limit the number of users who can control the VC Player.

#### Vcusers Support

The new VC Player update comes with Vcusers support, which allows users to access the VC Player without sudo access. With this feature, you can grant VC Player access to specific users without giving them full access to the bot.

#### Repeat Option

We have added a repeat option that allows you to repeat the song until you uncheck it. This feature eliminates the need to keep adding the same song repeatedly.

#### Double Linked List

The updated VC Player now uses a double linked list for the playlist. This feature allows you to navigate through the playlist and play the next/previous song.

#### Automatic User Addition

If the `VC_SESSION` string is added and the user is not in the group, the bot will automatically add the user to the group and play the song.

### 〣 Improvements

* The updated VC Player is more user-friendly and functional.
* We have fixed several bugs and improved the performance of the VC Player.
* The VC Player is now more stable and reliable than before.
