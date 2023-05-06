# 📄 Version 3.1.0

## Catuserbot Updates 3.0.1 -> 3.1.0

## Version : 3.1.0

* #### Additions
  * Added External repo support (so you can set `EXTERNAL_REPO` var with `True` or your custom plugins repo link to get custom plugins).
  * From now onwards there is no Badcat or Goodcat, while deploying you only need to set a var `BADCAT = True` in vars to get 18+ plugins.
  * Added Spotify now support (you can check which song you are playing on your spotify account from Telegram).
  * Added fake user quotly support (`.fq username text`).
  * Added `PING_PIC` & `PING_TEMPLATE` support are added newly, similar to `ALIVE_PIC` & `ALIVE_TEMPLATE` (check @CatTemplates for more info).
  * You can save your default profile by using `.setdv DEFAULT_USER`, so that for `.revert` command, spotify and autoprofile plugins, these defaults are used.
  * Added `gis` command for showing google search image with given query.
  * Added spoiler markdown use `||` before and after the spoiler text in your message to get spoiler format.
  * Added strikedown markdown use `~~` before and after the text in your message to get strikedown format.
  * Added new plugin `notebook`.
  * Translate support added for ocr plugin.
  * Temp approve support is added for pmpermit (will approve for 24 hours only or until heroku restarts).
  * `penguin` and `gandhi` commands are added newly in `stickerfun` plugin.
  * Added custom pic support for (`/start` cmd in bot).
  * Added media support for `ibutton`.
  * Video sticker support added for `.gif`.
  * New VPS plugin to edit config and update bot (now you can update your bot hosted in vps from telegram by `.update now`).
* #### Bug Fix
  * Using `yt_dlp` from now onwards instead of `youtube_dl` for `song` and `ytdl` commands.
  * Updated `telethon` to support new telegram features.
  * Updated `anilist` commands (`anime` and `sanime` commands merged to one with flags, `manga` command and `char` command also updated).
  * `.chain` command updated.
  * `CHANGE_TIME` & `DIGITAL_PIC` are newly added to db from heroku vars.
  * `Gdrive` plugin is fixed (`gauth` and the error when folder id is not set).
  * `lmg` command / `letmesearch` plugin is fixed and also added reply support.
  * From now onwards `block` and `unblock` can be used normally no need to turn on pmguard.
  * `q` cmd is fixed for private messages.
  * Video sticker kanging is fixed.
  * `.insta` cmd is fixed.
  * `.dlto` cmd is fixed.
  * `.ctime` command is now `.time` and vice-versa.
  * Fixed sticker kanging to multiple packs.
* #### Removed
  * `specs` command removed from `andriod` plugin.
  * `.gali` removed from `goodcat`.
* #### Plugins moved to External repo
  * amongus, animation1, animation2, animation3, animation4, animation5, animation6, art, azan, covid, cricket, echo, emojify, figlet, fonts, funarts, funnyfonts, funtxts, games, hack, imgmemes, imgfun, mask, memes, memestext, quotes, randomsticker, randomtext,

## Version 3.0.4

* #### Additions
  * Added two new features in inline bot like secret. they are hide and troll
  * Added Custom alive message format is added check @cat\_alive and use ALIVE\_TEMPLATE as var name.
  * Added random anime quote generator , anilist user search , myanilist user search , get filler episodes list of particular anime , sanime result format is changed and finally get scheduled anime's list on particular weekday.
  * Added fban plugin (read .help fedutils to get more info)
  * Added random tasks getter for truth or dare in games plugin.
  * Added a flag to zombies command so that you can clean in banned users list of group.
  * Added logo plugin
  * Added ip details collector but you need an api for this . set IPDATA\_API in your heroku vars
  * Added wallpaper searcher
* #### Bug Fix
  * Fixed help menu error (sometimes back button didn't work and also animation was not showing)
  * Lyrics cmd is fixed but you need to set GENIUS\_API\_TOKEN in heroku
  * Song command is updated so it gets metadata also now.
  * Doge cmd is fixed

## Version 3.0.3

* #### Additions
  * New Pastebins added.
  * New cmd custompfp added.
  * Added when cmd to check when the message posted.
  * Markdown is added to filters.
  * New cmd google cmd added (For google search use gs).
  * Added some flags in purge like purge -f to delete only files, -m to delete only audio files...etc.
  * Added upurge cmd to delete only specific user messages.
  * Gifs search cmd added.
  * New plugin textformat added.
* #### Bug Fix
  * Auto creation of pm logger group removed if you need create group and Set PM\_LOGGER\_GROUP\_ID.
  * Quote cmd fixed.
  * Imdb cmd fixed.
  * Unmute fixed.
  * Fixed pkang.
  * Changed stt cmd output.
  * Minor fixes in tts.
  * Fixed pmpermit pic when pmmenu is disabled.

## Version 3.0.1

* #### Additions
  * Custom start message for TG bot is added you can customize it.for more info check .help -c custom.
  * /help command added in Tg bot to know what commands it have.
  * Multiple alive pic, pmpermit pc support added.
  * Added a new cmd msgto (Like you can message to particular person or particular chat from the chat you are using.)
  * New command .noformat is added - To get text without markdown formatting.
  * New Command .ftt is added - reply to text/pdf/python file to get in text format.
  * Added New plugin game - check (.help game) for more information.
  * Pm permit inline menu can be turned on/off by .pmmenu on/off cmd.
  * Currency exchange value cmd is added, and you need an API for this.
  * Added (set/get/del)dv cmd for more info check docs.
* #### Bug Fix
  * Animated sticker to image error fix (i.e., cmds like mms will now work on animated stickers).
  * From now it stops logging some common errors in botlog group.
  * Error when no search results found in iytdl is fixed.
  * Magsik links are updated.
  * Seconds counter in autobio is removed (shows as this format %HH:%MM).
  * Error in revert cmd is fixed.
  * Super/mega group creation using cmd (.create b group name) is fixed.
  * Wiki command is optimized for better look
  * Imdb cmd is fixed.
  * Error in addsudo and delsudo is fixed.
  * Decode error is fixed.
