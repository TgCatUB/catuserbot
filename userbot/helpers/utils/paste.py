import json

import httpx

try:
    from ...Config import Config
    from ...core.logger import logging
    LOGS = logging.getLogger("CatUserbot")
except Exception:
    import logging
    LOGS = logging.getLogger("CatUserbot")
    class Config:
        BOTLOG_CHATID = 0


async def _post(siteurl, **kwargs):
    async with httpx.AsyncClient(follow_redirects=True, timeout=30) as client:
        return await client.post(siteurl, **kwargs)


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
    "content-type": "application/json",
}


async def p_paste(message, extension=None):
    """
    To Paste the given message/text/code to pasty.lus.pm
    """
    siteurl = "https://pasty.lus.pm/api/v1/pastes"
    data = {"content": message}
    try:
        response = await _post(siteurl, content=json.dumps(data), headers=headers)
    except Exception as e:
        return {"error": str(e)}
    if response.is_success:
        response = response.json()
        purl = f"https://pasty.lus.pm/{response['id']}.{extension}" if extension else f"https://pasty.lus.pm/{response['id']}.txt"
        try:
            from ...core.session import catub

            await catub.send_message(
                Config.BOTLOG_CHATID,
                f"**You have created a new paste in pasty bin.** Link to pasty is [here]({purl}). You can delete that paste by using this token `{response['deletionToken']}`",
            )
        except Exception as e:
            LOGS.info(str(e))
        return {
            "url": purl,
            "raw": f"https://pasty.lus.pm/{response['id']}/raw",
            "bin": "Pasty",
        }
    return {"error": "Unable to reach pasty.lus.pm"}


async def s_paste(message, extension="txt"):
    """
    To Paste the given message/text/code to spaceb.in
    """
    siteurl = "https://spaceb.in/api/"
    try:
        response = await _post(siteurl, json={"content": message, "extension": extension or "txt"})
    except Exception as e:
        return {"error": str(e)}
    if response.is_success:
        response = response.json()
        if response.get("error") and response.get("status", 200) < 400:
            return {"error": response["error"]}
        payload = response.get("payload", {})
        pid = payload.get("id")
        if pid:
            return {
                "url": f"https://spaceb.in/{pid}",
                "raw": f"{siteurl}{pid}/raw",
                "bin": "Spacebin",
            }
    return {"error": "Unable to reach spacebin."}


async def spaste(message, extension="txt"):
    return await s_paste(message, extension)


async def dp_paste(message, extension="txt"):
    """
    To paste text/code to dpaste.org
    """
    siteurl = "https://dpaste.org/api/"
    data = {"content": message, "format": "url", "expiry_days": 14}
    if extension:
        data["syntax"] = extension
    try:
        async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
            resp = await client.post(siteurl, data=data)
            if resp.status_code == 200 and resp.text.startswith("http"):
                url = resp.text.strip().strip('"')
                raw_url = f"{url}/raw"
                return {"url": url, "raw": raw_url, "bin": "Dpaste"}
    except Exception as e:
        return {"error": str(e)}
    return {"error": "Unable to reach dpaste.org"}


async def prs_paste(message, extension=None):
    """
    To paste text/code to paste.rs
    """
    siteurl = "https://paste.rs/"
    try:
        async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
            resp = await client.post(siteurl, content=message)
            if resp.status_code == 201 and resp.text.startswith("http"):
                url = resp.text.strip()
                return {"url": url, "raw": url, "bin": "Paste.rs"}
    except Exception as e:
        return {"error": str(e)}
    return {"error": "Unable to reach paste.rs"}


async def n_paste(message, extension=None):
    """
    To Paste the given message/text/code to nekobin
    """
    siteurl = "https://nekobin.com/api/documents"
    data = {"content": message}
    try:
        response = await _post(siteurl, content=json.dumps(data), headers=headers)
    except Exception as e:
        return {"error": str(e)}
    if response.is_success:
        response = response.json()
        purl = f"https://nekobin.com/{response['result']['key']}.{extension}" if extension else f"https://nekobin.com/{response['result']['key']}"
        return {
            "url": purl,
            "raw": f"https://nekobin.com/raw/{response['result']['key']}",
            "bin": "Neko",
        }
    return {"error": "Unable to reach nekobin."}


async def d_paste(message, extension=None):
    """
    To Paste the given message/text/code to dogbin
    """
    siteurl = "http://catbin.up.railway.app/documents"
    data = {"content": message}
    try:
        response = await _post(siteurl, content=json.dumps(data), headers=headers)
    except Exception as e:
        return {"error": str(e)}
    if response.is_success:
        response = response.json()
        purl = f"http://catbin.up.railway.app/{response['key']}.{extension}" if extension else f"http://catbin.up.railway.app/{response['key']}"
        return {
            "url": purl,
            "raw": f"http://catbin.up.railway.app/raw/{response['key']}",
            "bin": "Dog",
        }
    return {"error": "Unable to reach dogbin."}


async def pastetext(text_to_print, pastetype=None, extension=None):
    response = {"error": "something went wrong"}
    if pastetype is not None:
        if pastetype in ("s", "spacebin"):
            response = await s_paste(text_to_print, extension or "txt")
        elif pastetype in ("dp", "dpaste"):
            response = await dp_paste(text_to_print, extension or "txt")
        elif pastetype in ("rs", "pasters"):
            response = await prs_paste(text_to_print, extension)
        elif pastetype in ("p", "pasty"):
            response = await p_paste(text_to_print, extension)
        elif pastetype in ("n", "neko"):
            response = await n_paste(text_to_print, extension)
        elif pastetype in ("d", "dog"):
            response = await d_paste(text_to_print, extension)

    # Multi-tier fallback chain for guaranteed delivery
    if "error" in response:
        response = await s_paste(text_to_print, extension or "txt")
    if "error" in response:
        response = await dp_paste(text_to_print, extension or "txt")
    if "error" in response:
        response = await prs_paste(text_to_print, extension)
    if "error" in response:
        response = await p_paste(text_to_print, extension)
    if "error" in response:
        response = await n_paste(text_to_print, extension)
    if "error" in response:
        response = await d_paste(text_to_print, extension)
    return response
