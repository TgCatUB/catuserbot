# 📄 Version 3.2.0

## ✨ Additions

* Added VC support
  * Required Var:
    * `VCMODE = True`
    * `VC_SESSION = New Session` (Optional)
  * Required Buildpack: `heroku-buildpack-nodejs` → [https://github.com/rahulps1000/heroku-buildpack-nodejs](https://github.com/rahulps1000/heroku-buildpack-nodejs)
* Redesigned InlineQuery
  * Added support for Spotify, FileManager, CmdSearch
  * Added multiple user support for Secret & Troll
* Added new chatbot using Kuki
  * Removed `RANDOM_STUFF_API_KEY` var (no longer needed)

## 🛠️ Improvements

* Redesigned and fixed errors in App
* Added flag \[-t] in \[.glist] & post in telegraph for long list in Gdrive
* Added \[.grpstats] in Groupdata
* Added \[.buildpack] in Heroku
* Added flag \[-f] in \[.logo] & added random backgrounds (Do \[.lbg] to get)
* Added flag \[-f] in \[.write] in Notebook
* Added \[.rayso] in Pastebin
* Added flag \[s] in \[.shazam] in Songs
* Added \[.rspam] in Spam
* Added inline query & changed bot to @CatMusicRobot for \[.now] in Spotify
* Added flag \[p] in \[.stat] to get public links & changed to multiple texts for long messages instead of files in Stats
* Added branch switch support, can switch branch like Heroku now on VPS also in VPS
* Added Is\_Premium in Whois

## 🐛 Bug Fixes

* Fixed error on uppercase in \[.device] in Android
* Fixed error on response in \[.mal] in Anilist
* Fixed webdriver error (removed .krb) in Carbon
* Reformatted using API and removed PyDictionary in \[.meaning] in Dictionary
* Fixed error on promote if other than owner in \[.prankpromote] in Fake
* Fixed error on document files in Ffmpeg
* Fixed large gif size in \[.gif / .vtog] in FileConverts
* Fixed error on VPS in Lyrics
* Fixed error on getting image from file in Ocr
* Improved font in \[.q] in Quotly
* Fixed error for premium sticker in \[.spspam] in Spam
* Fixed error on kanging video & animated stickers in Stickers
* Fixed error on getting videos in \[.insta] in Ytdl
