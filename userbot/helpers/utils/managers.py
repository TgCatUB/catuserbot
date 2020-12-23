import asyncio
import functools
import re

import requests


def paste_text(text):
    asciich = ["*", "`", "_"]
    for i in asciich:
        text = re.sub(rf"\{i}", "", text)
    try:
        key = (
            requests.post("https://nekobin.com/api/documents", json={"content": text})
            .json()
            .get("result")
            .get("key")
        )
        link = f"https://nekobin.com/{key}"
    except:
        text = re.sub(r"•", ">>", text)
        kresult = requests.post(
            "https://del.dog/documents", data=text.encode("UTF-8")
        ).json()
        link = f"https://del.dog/{kresult['key']}"
    return link


def run_sync(func, *args, **kwargs):
    return asyncio.get_event_loop().run_in_executor(
        None, functools.partial(func, *args, **kwargs)
    )


def run_async(loop, coro):
    return asyncio.run_coroutine_threadsafe(coro, loop).result()
