---
description: How to deploy catuserbot
---

# Deploy Procedures

## Deploy to Heroku

1. **By Repl**
2. **By Termux**

## 1\) Repl

How to Deploy your UserBot to Heroku using Repl

👉 Create an account on [Github](https://github.com/join) & [Heroku ](https://signup.heroku.com/login)

👉 Open this [repo](https://github.com/sandy1709/catuserbot)

👉 Fork this repo to your Github.

👉 App name,ALIVE\_NAME, APP\_ID, API\_HASH, STRING\_SESSION, TG\_BOT\_TOKEN\_BF\_HER and TG\_BOT\_USER\_NAME\_BF\_HER are mandatory fields. Rest of the fields can be left with the default values.

=======================================================  
 ✍️ You can get your app id and api hash from @cattgorgbot or [http://my.telegram.org](http://my.telegram.org)

✍️  You can generate string season [here](https://generatestringsession.sandeep1709.repl.run/)  
      [**VIDEO GUIDE OF REPL**](https://drive.google.com/open?id=1uT313HBEIuTwjLhVNygbbWEsFuIRdtZM)  
========================================================

👉 Wait for deploy to finish.

👉 After deploy press Manage App then go to Resources

👉 Enable the worker dyno, by toggling the slide-toggle.

👉 Done. Your UserBot is alive. Check with .alive in any chat.

ℹ️ @catuserbot17

## 2\) Termux

How to Deploy your UserBot to Heroku using Termux  
  
👉 Create an account on [Github](https://github.com/join) & [Heroku ](https://signup.heroku.com/login)

👉 Open this [repo](https://github.com/sandy1709/catuserbot)

👉 Fork this repo to your Github.

👉 App name,ALIVE\_NAME, APP\_ID, API\_HASH, STRING\_SESSION, TG\_BOT\_TOKEN\_BF\_HER and TG\_BOT\_USER\_NAME\_BF\_HER are mandatory fields. Rest of the fields can be left with the default values.

=======================================================  
 ✍️ You can get your app id and api hash from @cattgorgbot or [http://my.telegram.org](http://my.telegram.org)  
  
 ✍️ Generate String Session, Follow below steps  
  
[**VIDEO GUIDE FOR BETTER UNDERSTANDING**](https://drive.google.com/open?id=1Qri7T4-hsQnA_urKDjBOoTjoHxkhyjOt)  
**\[ OR \]**  
**Follow steps below**  
Install [termux](https://play.google.com/store/apps/details?id=com.termux) from playstore,   
Then run these 2 codes .

`termux-setup-storage`

Press enter \(on your keyboard\) and then paste

`pkg install python git openssl wget -y && pip install telethon && wget https://raw.githubusercontent.com/sandy1709/catuserbot/master/stringsetup.py && python3 stringsetup.py`

========================================================

👉 Wait for deploy to finish.

👉 After deploy press Manage App then go to Resources

👉 Enable the worker dyno, by toggling the slide-toggle.

👉 Done. Your UserBot is alive. Check with .alive in any chat.

