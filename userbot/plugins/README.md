## Mandatory Imports
```python3
None
```
There is None Mandatory Imports. Because Config, bot, command are already automatically imported.

## Explanation
The Mandatory Import are now automatically imported.

### Formation
Now I will show a short script to show the formation of the desired script.
```python3
@command(pattern="^.alive", outgoing=True)
async def hello_world(event):
    if event.fwd_from:
        return
    await event.edit("**HELLO WORLD**\n\nThe following is controlling me too!\n" + Var.SUDO_USERS)
```
