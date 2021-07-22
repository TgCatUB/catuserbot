# visi.tk/plutoniumx
import calendar

from userbot import catub

plugin_category = "utils"


@catub.cat_cmd(
    pattern="ycal (.*)",
    command=("ycal", plugin_category),
    info={
        "header": "To get calendar of the given year.",
        "usage": "{tr}ycal year",
        "examples": "{tr}ycal 2021\n\nNote: please view this calendar from a pc",
    },
)
async def _(event):
    "To get the calendar of the given year."
    pluto = event.pattern_match.group(1)
    year = pluto
    try:
        cal = calendar.calendar(int(year))
        await edit_or_reply(event, f"`{cal}`")
    except Exception as e:
        await edit_delete(event, f"`{str(e)}`", 15)
