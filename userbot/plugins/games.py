import asyncio
import json
import random

import requests

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import reply_id

plugin_category = "fun"

game_code = ["ttt", "ttf", "ex" "cf", "rps", "rpsls", "rr", "c", "pc"]
button = ["0", "1", "2", "3", "4", "5", "6", "7", "8"]
game_name = [
    "Tic-Tac-Toe",
    "Tic-Tac-Four",
    "Elephant XO",
    "Connect Four",
    "Rock-Paper-Scissors",
    "Rock-Paper-Scissors-Lizard-Spock",
    "Russian Roulette",
    "Checkers",
    "Pool Checkers",
]

game_list = """1.`ttt` :- Tic-Tac-Toe
2.`ttf` :- Tic-Tac-Four
3.`ex` :- Elephant XO
4.`cf` :- Connect Four
5.`rps` :- Rock-Paper-Scissors
6.`rpsls` :- Rock-Paper-Scissors-Lizard-Spock
7.`rr` :- Russian Roulette
8.`c` :- Checkers
9.`pc` :- Pool Checkers"""

category = ["classic", "kids", "party", "hot", "mixed"]


async def get_task(mode, choice):
    url = "https://psycatgames.com/api/tod-v2/"
    data = {
        "id": "truth-or-dare",
        "language": "en",
        "category": category[choice],
        "type": mode,
    }
    headers = {
        "referer": "https://psycatgames.com/app/truth-or-dare/?utm_campaign=tod_website&utm_source=tod_en&utm_medium=website"
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    result = response.json()["results"]
    return random.choice(result)


@catub.cat_cmd(
    pattern="(task|truth|dare)(?: |$)([1-5]+)?$",
    command=("task", plugin_category),
    info={
        "header": "Get a random truth or dare task.",
        "description": "if no input is given then task will be from classic or kids category. if you want specific category then give input.",
        "note": "U need to give input as 1 for classic , 2 for kids , 3 for party , 4 for hot and 5 for mixed. if you want to give multiple catgories then use numbers without space like 12",
        "example": [
            "{tr}task",
            "{tr}task 2",
            "{tr}task 123",
        ],
    },
)
async def truth_dare_task(event):
    "Get a random task either truth or dare."
    taskmode = event.pattern_match.group(1)
    if taskmode == "task":
        catevent = await edit_or_reply(event, "Getting a random task for you.....")
        taskmode = random.choice(["truth", "dare"])
    else:
        catevent = await edit_or_reply(
            event, f"Getting a random {taskmode} task for you....."
        )
    category = event.pattern_match.group(2)
    category = int(random.choice(category)) if category else random.choice([1, 2])
    try:
        task = await get_task(taskmode, category)
        if taskmode == "truth":
            await catevent.edit(f"**The truth task for you is**\n`{task}`")
        else:
            await catevent.edit(f"**The dare task for you is**\n`{task}`")
    except Exception as e:
        await edit_delete(catevent, f"**Error while getting task**\n`{str(e)}`", 7)


@catub.cat_cmd(
    command=("truth", plugin_category),
    info={
        "header": "Get a random truth task.",
        "description": "if no input is given then task will be from classic or kids category. if you want specific category then give input.",
        "note": "U need to give input as 1 for classic , 2 for kids , 3 for party , 4 for hot and 5 for mixed. if you want to give multiple catgories then use numbers without space like 12",
        "example": [
            "{tr}truth",
            "{tr}truth 2",
            "{tr}truth 123",
        ],
    },
)
async def truth_task(event):
    "Get a random truth task."
    # just to show in help menu as seperate


@catub.cat_cmd(
    command=("dare", plugin_category),
    info={
        "header": "Get a random dare task.",
        "description": "if no input is given then task will be from classic or kids category. if you want specific category then give input.",
        "note": "U need to give input as 1 for classic , 2 for kids , 3 for party , 4 for hot and 5 for mixed. if you want to give multiple catgories then use numbers without space like 12",
        "example": [
            "{tr}dare",
            "{tr}dare 2",
            "{tr}dare 123",
        ],
    },
)
async def dare_task(event):
    "Get a random dare task."
    # just to show in help menu as seperate


@catub.cat_cmd(
    pattern="game(?:\s|$)([\s\S]*)",
    command=("game", plugin_category),
    info={
        "header": "Play inline games",
        "description": "Start an inline game by inlinegamebot",
        "Game code & Name": {
            "ttt": "Tic-Tac-Toe",
            "ttf": "Tic-Tac-Four",
            "cf": "Connect Four",
            "rps": "Rock-Paper-Scissors",
            "rpsls": "Rock-Paper-Scissors-Lizard-Spock",
            "rr": "Russian Roulette",
            "c": "Checkers",
            "pc": "Pool Checkers",
        },
        "usage": "{tr}game <game code>",
        "examples": "{tr}game ttt ",
    },
)
async def igame(event):
    "Fun game by inline"
    reply_to_id = await reply_id(event)
    input_str = event.pattern_match.group(1)
    data = dict(zip(game_code, button))
    name = dict(zip(game_code, game_name))
    if not input_str:
        await edit_delete(
            event, f"**Available Game Codes & Names :-**\n\n{game_list}", time=60
        )
        return
    if input_str not in game_code:
        catevent = await edit_or_reply(event, "`Give me a correct game code...`")
        await asyncio.sleep(1)
        await edit_delete(
            catevent, f"**Available Game Codes & Names :-**\n\n{game_list}", time=60
        )
    else:
        game = data[input_str]
        gname = name[input_str]
        await edit_or_reply(
            event, f"**Game code `{input_str}` is selected for game:-** __{gname}__"
        )
        await asyncio.sleep(1)
        bot = "@inlinegamesbot"
        results = await event.client.inline_query(bot, gname)
        await results[int(game)].click(event.chat_id, reply_to=reply_to_id)
        await event.delete()
