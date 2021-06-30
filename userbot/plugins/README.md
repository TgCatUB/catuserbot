## Mandatory Imports
```python3
from userbot import catub

from ..core.managers import edit_delete, edit_or_reply

plugin_category="extra"
```

### Formation
This below one is Sample format of making plugin
```python3
from userbot import catub

from ..core.managers import edit_delete, edit_or_reply

plugin_category="extra"

@catub.cat_cmd(
    pattern="hibuddy(?:\s|$)([\s\S]*)",
    command=("hibuddy", plugin_category),
    info={
        "header": "Just to say hi to other user.",
        "description": "input string along with cmd will be added to your hi text",
        "usage": "{tr}hibuddy <text>",
        "examples": "{tr}hibuddy how are you doing",
    },
)
async def hi_buddy(event):
    "Just to say hi to other user."
    input_str= event.pattern_match.group(1)
    if not input_str:
        await edit_delete(event,"No input is found. Use proper syntax.")
        return
    outputtext= f"+-+-+-+-+-+\n|h|e|l|l|o|\n+-+-+-+-+-+\n{input_str}"
    await edit_or_reply(event,outputtext)
```

For more information refer this [Docs](https://docs.telethon.dev/en/latest/)


Arguments in cat_cmd are as follows:
```

pattern="Regex for command"
command=("Just command name", plugin_category) use plugin_category name from predefined names (admin,bot,utils,tools,extra,fun,misc)
info={
        "header":string - "intro for command",
        "description": string - "Description for command",
        "flags": dict or string - "Flags u are using in your plugin",
        "options": dict or string - "Options u are using in your plugin",
        "types": list or string - "types u are using in your plugin",
        "usage": "Usage for your command",
        "examples": "Example for the command",
        "your custom name if you want to use other": str or list or dict - "data/information about it",
    },

groups_only=True or False(by default False) - Either your command should work only in group or not
allow_sudo=True or False(by default True) - Should your sudo users need to have access or not,
edited=True or False(by default True) - If suppose you entered wrong command syntax and if you edit it correct should it work or not.
forword=True or False(by deafult False) - Is forword messages should react or not.
disable_errors=True or False(by default False) - if any error occured during the command usage should it log or not.
```
