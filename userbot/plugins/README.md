## Mandatory Imports
```python3
from userbot import bot
from config import Config
from userbot.utils import command
from telethon import events
```
This is needed to perform a task using the bot.

## Explanation
```python3
from userbot import bot
```
This is the whole bot itself.

```python3
from config import Config
```
This import Variables that can be used and configured.
If you are running this bot the normal way you will have to read the "The Normal Way" section of the README on the front page.

```python3
from userbot.utils import command
```
This is needed to create an handler when a certain command is run

```python3
from telethon import events
```
This is needed to run the script when the command is said

### Formation
Now I will show a short script to show the formation of the desired script.
```python3
from userbot import bot
from config import Config
from userbot.utils import command
from telethon import events

@command(pattern="^.alive", outgoing=True)
async def hello_world(event):
    if event.fwd_from:
        return
    await event.edit("**HELLO WORLD**")
```
