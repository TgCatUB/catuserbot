# 📄 Version 3.0.0

## New Features

* Added fast telethon support to improve download and upload speeds for files
* New help menu inspired by Userge, allowing users to get help for a specific command rather than the whole plugin
* Notification feature to alert users after a restart or update (enabled with `.notify on`)
* PM permit feature can be enabled with `.pmguard on/off` instead of using `PRIVATE_GROUP_IDvar`. However, users must set `PRIVATE_GROUP_BOT_API_ID`
* Custom PM text and picture variables have been removed; users must now use the `custom` command to set these. A custom block message has also been added.

## New Bot Commands

* `/uinfo`: reply this to a forwarded message to get details about the user who sent it (as stickers and emoji forwarded messages don't show who sent them)
* `/broadcast`: reply to any message in the bot PM to send it to all users who started the bot
* `/ban reason`: reply to a forwarded message in the bot to ban the user so that messages sent by them to the bot don't get forwarded to you
* `/unban reason`: reply to a user's forwarded message or give their username along with the command in the bot PM to unban them from your bot

## Bot Controls

* `bot_users`: to get a list of users who started your bot
* `bblist`: to get a list of banned users in the bot
* `bot_antif`: to turn anti-flood on or off in the bot PM (off by default)

## iytdl

* `iytdl`: to download YouTube videos in a specific format. This command shows you the list of all available formats, and you can download a specific format.

## Changes to Plugins

### Admin

* `setgpic` is now `gpic` and has two new flags (`-s` for setting, `-d` for deleting)
* `iundlt` and `undlt` have been merged into `undlt` to get recently deleted messages in a group. Users can pass an integer along with the command to get the number of deleted messages to show (default is 5). Use `-u` to show media.

### Amongus

* Two new commands have been added, along with previous Impostor plugin commands. The old Impostor plugin has been deleted.

### Anilist

* New commands have been added (old commands remain unchanged):
  * `wanime`: anime reverse search
  * `sanime`: search and get info about an anime
  * `akaizoku`: get link to download anime (see the command for more info)
  * `upcoming`: show list of upcoming anime

### App

* `appr` command has been removed; `app` is the only command in the plugin now.

### Archive

* `zip` and `unzip` commands have been fixed.

### Autopfp

* Merged with Autoprofile plugin; `thorpfp` and `batmanpfp` commands have been fixed.

### Azan

* Previously known as `ezanvakti`, the plugin has been renamed and fixed.

### Blacklist

* Renamed as `blacklistword`; no other changes have been made.

### BlacklistChats

* Enable with `.chatblacklist` and add chats to the database with `.addblkchat` command. To stop the userbot from working in those chats and remove the chat, use `.rmblkchat`. View the list with `.listblkchats`.

### Carbon

* Removed "rgbk2" command

### Channel Download

* Fixed wrong count shown while downloading

### Chatbot

* Added new plugin to replace old Lydia plugin
* Requires setting of API and referring to channel for API usage
* Check help menu of this plugin for more information

### Climate

* Fixed sunrise and sunset timings

### Custom

* To customize pmpermit, check help for more info by `.help -c custom`

### Download

* Added fast telethon support for faster downloads

### Echo

* Rewritten code for better display of list of echoed users

### Emoji games

* Added bowl emoji support

### Execmod

* Merged `.date` with `.time`
* Removed duplicate `fast` command and `suicide` command
* Removed most plugins except `env`
* Added `qpro` command to Quote plugin

### External plugins

* Support changed to new format
* All old plugins must be updated to new format

### Fileconverts

* Added new commands:
  * `Spin` (image to round video)
  * `circle` (sticker support added)
  * `itog` (image to gif, check help for usage)
  * `vtog` (video to gif, check help for usage)

### Fonts

* Merged with `Fonts2` plugin

### Gdrive

* Added folder download support for `.gdown` command (does not support `-u` flag)
* Fixed folder upload with `.ugd` command

### Git

* Changed `Github` command to new format
* Added `commit` command for future use

### Google

* Customization options added for number of results and page

### Groupdata

* Updated `adminperm` command as `.uperm` and transferred to other plugin

### Help

* New UI help menu
* Use `-t` to get text format of all plugins
* Use `.cmds` to get only command list
* Removed `info` command

### Imgfun

* Added new commands to manipulate images:
  * `imirror`
  * `irotate`
  * `iresize`
  * `square`
  * `dotify`

### Memify

* Added `pframe` command to frame replied image

### Mention

* Fixed user mention format to `@username[text]`

### Pmpermit

* New pmpermit added with inline help menu

### Quotly

* Added `qpic` command to reply to user message

### Reddit

* Added command to get random posts from Reddit subcategories

### Rename

* Cleaned up useless commands; `rename` command merged with `.mvto`

### Songs

* Added new audio reverse command; check `.shazam` command

### Stickerfun

* Added new commands:
  * `honk`
  * `twt`
  * `glax`
  * `doge`

### Stickers

* Added `gridpack` command to convert pic to sticker pack
* Fixed stickers search command

### Sudo

* Added support for adding sudo users to bot and customizing commands for sudo users

### Tools

* Removed `currency` command; will add back soon

### Translate

* Use `lang` command to set default language for chat bot

### Upload

* Added fast telethon support for faster uploads
* Moved `circle` command to `Fileconverts` plugin

### Urltools

* Renamed `dagb` to this

Note: Some changes may have been missed in this chang
