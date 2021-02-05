
# CAT USERBOT
[![HitCount](http://hits.dwyl.com/sandy1709/catuser.svg)](http://hits.dwyl.com/sandy1709/catuser)
[![CodeFactor](https://www.codefactor.io/repository/github/sandy1709/catuserbot/badge?&style=flat-square)](https://www.codefactor.io/repository/github/sandy1709/catuserbot)
![Repo Size](https://img.shields.io/github/repo-size/sandy1709/catuserbot?&style=flat-square)
[![GitHub license](https://img.shields.io/github/license/sandy1709/catuserbot?&style=flat-square)](https://github.com/sandy1709/catuserbot/blob/master/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/sandy1709/catuserbot?&style=flat-square)](https://github.com/sandy1709/catuserbot/issues)
[![PR Open](https://img.shields.io/github/issues-pr/sandy1709/catuserbot?&style=flat-square)](https://github.com/sandy1709/catuserbot/pulls)
[![PR Closed](https://img.shields.io/github/issues-pr-closed/sandy1709/catuserbot?&style=flat-square)](https://github.com/sandy1709/catuserbot/pulls?q=is:closed)

[![GitHub forks](https://img.shields.io/github/forks/sandy1709/catuserbot?&style=flat-square)](https://github.com/sandy1709/catuserbot/network)
[![GitHub stars](https://img.shields.io/github/stars/sandy1709/catuserbot?&style=flat-square)](https://github.com/sandy1709/catuserbot/stargazers)

### The Easy Way to deploy the bot
Get APP ID and API HASH from [HERE](https://my.telegram.org) and BOT TOKEN from [Bot Father](https://t.me/botfather) and then Generate stringsession by clicking on run.on.repl.it button below and then click on deploy to heroku . Before clicking on deploy to heroku just click on fork and star just below

[![Get string session](https://repl.it/badge/github/sandy1709/sandeep1709)](https://generatestringsession.sandeep1709.repl.run/)

[![Deploy To Heroku](https://www.herokucdn.com/deploy/button.svg)](https://dashboard.heroku.com/new?button-url=https%3A%2F%2Fgithub.com%2Fsandy1709%2Fcatuserbot%2Ftree%2Fbugs&template=https%3A%2F%2Fgithub.com%2Fsandy1709%2Fcatuserbot)


### Join [here](https://t.me/catuserbot17) for updates and tuts and [here](https://t.me/catuserbot_support) for discussion and bugs

### The Normal Way

An example `local_config.py` file could be:

**Not All of the variables are mandatory**

__The Userbot should work by setting only the first two variables__

```python3
from heroku_config import Var

class Development(Var):
  APP_ID = 6
  API_HASH = "eb06d4abfb49dc3eeb1aeb98ae0f581e"
```

### UniBorg Configuration



**Heroku Configuration**
Simply just leave the Config as it is.

**Local Configuration**

Fortunately there are no Mandatory vars for the UniBorg Support Config.

## Mandatory Vars

- Only two of the environment variables are mandatory.
- This is because of `telethon.errors.rpc_error_list.ApiIdPublishedFloodError`

    - `APP_ID`:   You can get this value from https://my.telegram.org
    - `API_HASH`:   You can get this value from https://my.telegram.org
- The userbot will not work without setting the mandatory vars.
