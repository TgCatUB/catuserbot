---
description: Changelog for Catuserbot Update 3.0.0
---

# Version 3.0.0

✘  Added fast telethon support - Helps in downloading and uploading speed for files download

✘ New help menu \(copied/inspired from userge\). Who can get help for command itself instead of whole plugin help. and check usage and examples for its usage.

✘ After restart or update you will get notified from now on \(turn it on by using _.notify on_\)

✘ Pmpermit can be enabled by .pmguard on/off instead of using `PRIVATE_GROUP_ID`_var But You must set_ `PRIVATE_GROUP_BOT_API_ID`

➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖

✘  **Bot Commands**

☞ /uinfo reply this to user forwarded message to get details of the user who sent that message \(since sticker and emoji forwarded messages doesn't show who sent them\).

☞ /broadcast reply this cmd to any message in the bot pm to send it all users who started your bot.

☞/ban reply to forward message in the bot to ban the user so that the messages sent by him to bot doesn't get forwarded to you.

☞/unban reply to user forwarded message or give his username along with cmd in bot pm to unban him from your bot.

**✘  Bot Controls**

☞ bot\_users - To get list of users who started your bot.

☞ bblist - To get list of banned users in bot.

☞ bot\_antif - to turn on or turn off anti flood in bot pm by default it will be off.

**✘  iytdl**

☞ iytdl to download YouTube videos in specific format. This cmd shows you the list of all formats available and you can download specific format.

➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖

####  Changes in plugins <a id="Changes-in-plugins"></a>

➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖

**✘  Admin**

☞ setgpic is updated as gpic and added two flags newly as \(-s for setting , -d for deleting\)

☞ iundlt and undlt both merged ad undlt - to get recently deleted messages in group, u can also pass integer along with cmd to get no of deleted messages to be showed by default it is 5, use -u to show media.

**✘  Amongus**

☞ Added 2 cmds newly and previous impostor plugin cmds to this and deleted old impostor plugin.

**✘  Anilist**

☞ Added new cmds \(old cmds remain unchanged\)

 •  wanime - \(anime reverse search\)

 •  sanime - to search and get info about that anime

 •  akaizoku - to get link to download anime \(for more info check that cmd\)

 •  upcoming - will show list of upcoming anime

**✘  App** - appr command is removed u have only app cmd in it now

**✘  Archive** - zip, unzip cmds fixed

**✘  Autopfp** Merged with **Autoprofile** plugin and thorpfp and batmanpfp cmd fixed

**✘  Azan** plugin previously known as **ezanvakti** \(fixed and renamed as Azan\)

**✘  Blacklist** - renamed as **blacklistword** and no other changes

**✘  BlacklistChats** - Enable it by _.chatblacklist_ and add the chats to database by _.addblkchat_ cmd. To stop working of userbot in those chats and remove the chat by doing _.rmblkchat_ cmd. You can see list by _.listblkchats_

**✘  Carbon -** rgbk2 cmd removed

**✘  Channel Download -** fixed wrong count shown while downloading

**✘  Chatbot -** New plugin replacement for lydia - for proper working of this plugin You need to set Api, refer channel for api and check help menu of this plugin

**✘ Climate -** fixed sunrise and sunset timings

**✘ Custom -**  To customize pmpermit, check help for more info by _.help -c custom_

**✘ Download -** Added fast telethon support so download takes much less time than before

**✘ Echo -** rewritten code again so it can show list of echoed  users in better way.

**✘  Emoji games -** Added bowl emoji support

**✘ Execmod - .**date is merged with time, fast cmd is removed \(duplicate of speed-test\), qpro added to Quote plugin, except env , suicide and plugins remaining all removed.

**✘ External plugins support is changed so update all old plugins in the new format.**

**✘ Fileconverts**

☞  ****Added new cmds 

•  Spin \(image to round video \) , circle - sticker support added, itog \(image to gif check help for this command you will like it.\), vtog \(video to gif check help to know how to use\)

**✘ Fonts -**  fonts and fonts2 plugins are merged to this plugin

**✘ Gdrive -**

☞ ****Added Folder download support for _.gdown_ cmd \(-u flag doesn't work for it\)

☞ Folder upload by _.ugd_ also fixed

**✘ Git -** Github cmd is changed to new look and commit is added to this plugin \(for future use\)

**✘ Google -** Now you can customize no. of results to be shown and from which page to be showed

**✘ Groupdata -** adminperm cmd is updated as _.uperm_ and transferred to other plugin.

**✘ Help** - New ui help menu u can use -t to get in text format of all plugins

    ☞ Use _.cmds_ to get only command list

     ☞  Info cmd is removed, new help cmd does that info cmd function

**✘ Imgfun -** 

     ****Check this help menu for many new cmds to play with images , like imirror, irotate, iresize, square, dotify 

**✘ Mashup** plugin is removed because bot used for it is dead

**✘ Memify** 

 New cmd pframe \(to frame the replied image \) is added

**✘ Mention -** Fixed user mention by doing this format @username\[text\]

**✘ Pmpermit -** New pmpermit is Added with inline help menu 

**✘ Quotly -** Added new cmd named qpic reply it to user message .

**✘ Reddit -** to get random reddit posts from reddit subcategories

**✘ Rename -** cleaned useless cmds like rename as .mvto cmd have same function

**✘ Songs -** added new audio reverse cmd check _.shazam_ cmd

**✘ Stickerfun -** Added new cmds like honk, twt, glax and doge.

**✘ Stickers -** Added new cmd called .gridpack which converts pic to sticker pack, fixed stickers search cmd also.

**✘ Sudo -** 

  ****Turn on sudo and use this cmds for adding sudo users for your bot and custoize the cmds which are used by your sudo

**✘ Tools -** 

   ****Currency cmd removed will soon add this again

**✘ Translate -** 

    ****use lang cmd for setting default language so same language will be used for chat bot

**✘ Upload -**

    ****fast telethon support added and circle cmd moved to fileconverts

**✘ urltools** 

       dagb  is renamed as this

➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖

I may have forgotten some changes here.

**✘ Credits**

➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖

• iytdl , reddit , bot anti flood ,help ui are taken from userge-x.

• help menu look is inspired from userge/userge-x.

