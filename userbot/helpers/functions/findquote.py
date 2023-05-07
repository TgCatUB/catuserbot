# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import random

import requests
from bs4 import BeautifulSoup


async def extract_quote(url):
    results = []
    request = requests.get(url).text
    soup = BeautifulSoup(request, "html.parser")
    for quote in soup.find_all("div", class_="quote"):
        response = quote.find("div", {"class": "quoteText"}).text
        results.append(response.replace("\n", " ").strip())
    return results


async def random_quote():
    pgno = random.randint(1, 100)
    quoteurl = f"https://www.goodreads.com/quotes?format=html&mobile_xhr=1&page={pgno}"
    results = await extract_quote(quoteurl)
    return random.choice(results)


async def search_quotes(query):
    pgno = random.randint(1, 5)
    quoteurl = f"https://www.goodreads.com/quotes/search?commit=Search&page={pgno}&q={query.replace(' ', '+')}&utf8=%E2%9C%93"
    results = await extract_quote(quoteurl)
    return random.choice(results)
