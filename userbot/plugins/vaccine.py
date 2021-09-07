# Created by @Jisan7509

import requests

from ..core.managers import edit_delete, edit_or_reply
from . import catub

plugin_category = "fun"


@catub.cat_cmd(
    pattern="vaccine ?([\s\S]*)",
    command=("vaccine", plugin_category),
    info={
        "header": "Get vaccine center details",
        "usage": "{tr}vaccine <pin code> <dd-mm-yyyy>",
        "examples": "{tr}vaccine 682005 29-06-2021",
    },
)
async def cat(event):
    "coruna vaccine"
    input_text = event.pattern_match.group(1)
    if input_text and " " in input_text:
        pin, date = input_text.split()
    else:
        return await edit_delete(event, "Give input values correctly.")
    url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={int(pin)}&date={date}"
    res = requests.get(url)
    a = res.json()
    my_string = "<b>Center No : 1 </b>\n\n"
    if "centers" not in a or not a["centers"]:
        return await edit_delete(event, "Can't find any deatils for this pin code.")
    await edit_or_reply(event, "Processing...")
    i = 0
    for x in a["centers"]:
        for items in a["centers"][i]:
            if type(a["centers"][i][items]) is list:
                for j, s in enumerate(a["centers"][i][items]):
                    for subitem in a["centers"][i][items][j]:
                        val = a["centers"][i][items][j][subitem]
                        if "_" in subitem:
                            subitem = subitem.replace("_", " ")
                        my_string += (
                            f"<b>   • {subitem.title()}  :</b>  <code>{val}</code>\n"
                        )
            else:
                value = a["centers"][i][items]
                if "_" in items:
                    items = items.replace("_", " ")
                my_string += f"<b>✘ {items.title()}   :</b>  <code>{value}</code>\n"
        i += 1
        if i < len(a["centers"]):
            my_string += f"\n\n<b>Center No : {i+1}</b>\n\n"
    cat = (
        my_string.replace("',", "\n       ")
        .replace("['", "• ")
        .replace("']", "")
        .replace("'", "• ")
    )
    await edit_or_reply(event, cat, parse_mode="html")
