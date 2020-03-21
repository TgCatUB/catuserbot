""" Userbot module for shortening links using kutt.it """

import requests
from re import findall
from userbot.utils import admin_cmd, parse_arguments

API_ENDPOINT = "https://kutt.it/api/"


@borg.on(admin_cmd(pattern="kutt\s?([\S\s]+)?"))
async def kutt_it(e):
    reply_message = await e.get_reply_message()
    params = e.pattern_match.group(1) or ""
    args, params = parse_arguments(params, ['reuse'])

    urls = extract_urls(params)
    urls.extend(extract_urls(reply_message.text or ""))

    print(urls)

    if not urls:
        k = await e.edit("Need a URL to convert")
        await k.delete()
        await asyncio.sleep(3)
        return

    reuse = args.get('reuse', False)
    await e.edit("`Kutting...`")

    shortened = {}
    for url in urls:
        payload = {'target': url, 'reuse': reuse}
        headers = {'X-API-Key': Config.KUTT_IT_API_KEY}
        resp = requests.post(API_ENDPOINT + "url/submit", json=payload, headers=headers)

        json = resp.json()  
        if resp.status_code == 200:
            shortened[url] = json['shortUrl']
        else:
            shortened[url] = None

    message = ""
    for item in shortened.items():
        message += f"Original URL: {item[0]} \nShortened URL: {item[1]} \n"

    await e.edit(message, link_preview=False)


def extract_urls(message):
    matches = findall(r'(https?://\S+)', str(message))
    return list(matches)    
