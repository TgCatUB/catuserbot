# SELF HOST

**HOW TO HOST CATUSERBOT ON YOUR OWN?**

1. First of all, update and upgrade apt **:**

> _sudo apt update && sudo apt upgrade -y_

2. And then install the required apt packages:

> _sudo apt install --no-install-recommends -y curl git libffi-dev libjpeg-dev libwebp-dev python3-lxml python3-psycopg2 libpq-dev libcurl4-openssl-dev libxml2-dev libxslt1-dev python3-pip python3-sqlalchemy openssl wget python3 python3-dev libreadline-dev libyaml-dev gcc zlib1g ffmpeg libssl-dev libgconf-2-4 libxi6 unzip libopus0 libopus-dev python3-venv libmagickwand-dev pv tree mediainfo_

If you wanna use local database then follow this steps else skip to step 8

Install requirements for this by

> _sudo apt install postgresql postgresql-contrib_

**3.** Change the user to postgres to change the default ident password:

> _sudo su - postgres_

**4.** And then open the PostgreSQL shell:

> psql

**5.** Set any password you prefer, by running the below SQL:

> _ALTER USER postgres WITH PASSWORD 'yourpasswordhere';_

**6.** Get out of the PostgreSQL shell:

> _\q_

**7.** And go back to your user:

> _exit_

Now, the DB\_URI will be:

> _postgresql://postgres:yourpasswordhere@localhost:5432/catuserbot_

or use [elephantsql](https://www.elephantsql.com/) if you wanna use that

**8. Clone the repository:**for goodcat

> _git clone https://github.com/sandy1709/catuserbot_

for badcat

> _git clone https://github.com/jisan09/catuserbot_

**9. Change dir to the cloned folder:**

> _cd catuserbot_

**10. Create your config.py.**

by renaming the exampleconfig.py

> _mv exampleconfig.py config.py_

you can get string session by running _python3 stringsetup.py_

before running that install telethon by _pip3 install telethon_

**11. Create a new screen:**

Either tmux or screen**for screen**

_sudo apt install screen_

_screen -S catuserbot_**for tmux**

_sudo apt install tmux_

_tmux_

**12. And a virtual environment:**

> _virtualenv venv_

**13. Activate the virtual environment you've just created:**

> _source venv/bin/activate_

**14. And install the Python requirements:**

> _pip3 install -r requirements.txt_

**15. Finally, run the userbot:**

> _python3 -m userbot_

**16. And get out of your screen**

by pressing CTRL+A and after that CTRL+D. \(if you used screen\)

or

CTRL+B and then D \(if you use tmux\)

