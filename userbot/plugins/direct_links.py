import asyncio
import json
import re
import urllib.parse
from random import choice

import httpx
from bs4 import BeautifulSoup
from humanize import naturalsize

from userbot import catub

from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply

LOGS = logging.getLogger(__name__)
plugin_category = "misc"


def _client():
    return httpx.AsyncClient(follow_redirects=True, timeout=30)


async def _popen_read(command):
    process = await asyncio.create_subprocess_shell(command, stdout=asyncio.subprocess.PIPE)
    stdout, _ = await process.communicate()
    return stdout.decode()


@catub.cat_cmd(
    pattern=r"direct(?: |$)([\s\S]*)",
    command=("direct", plugin_category),
    info={
        "header": "To generate a direct download link from a URL.",
        "description": "Reply to a link or paste a URL to generate a direct download link.",
        "supported links": [
            "Google Drive",
            "Cloud Mail",
            "Yandex.Disk",
            "AFH",
            "ZippyShare",
            "MediaFire",
            "SourceForge",
            "OSDN",
            "GitHub",
        ],
        "usage": "{tr}direct <url>",
    },
)
async def direct_link_generator(event):
    """To generate a direct download link from a URL."""
    textx = await event.get_reply_message()
    message = event.pattern_match.group(1)
    if not message:
        if textx:
            message = textx.text
        else:
            return await edit_delete(event, "`Usage: .direct <url>`")
    catevent = await edit_or_reply(event, "`Processing...`")
    reply = ""
    links = re.findall(r"\bhttps?://.*\.\S+", message)
    if not links:
        reply = "`No links found!`"
        await catevent.edit(reply)
    for link in links:
        if "drive.google.com" in link:
            reply += await gdrive(link)
        elif "zippyshare.com" in link:
            reply += await zippy_share(link)
        elif "mega." in link:
            reply += await mega_dl(link)
        elif "yadi.sk" in link:
            reply += await yandex_disk(link)
        elif "cloud.mail.ru" in link:
            reply += await cm_ru(link)
        elif "mediafire.com" in link:
            reply += await mediafire(link)
        elif "sourceforge.net" in link:
            reply += await sourceforge(link)
        elif "osdn.net" in link:
            reply += await osdn(link)
        elif "github.com" in link:
            reply += await github(link)
        elif "androidfilehost.com" in link:
            reply += await androidfilehost(link)
        else:
            reply += re.findall(r"\bhttps?://(.*?[^/]+)", link)[0] + "is not supported"
    await catevent.edit(reply)


async def gdrive(url: str) -> str:
    """GDrive direct links generator"""
    drive = "https://drive.google.com"
    try:
        link = re.findall(r"\bhttps?://drive\.google\.com\S+", url)[0]
    except IndexError:
        return "`No Google drive links found`\n"
    file_id = ""
    reply = ""
    if link.find("view") != -1:
        file_id = link.split("/")[-2]
    elif link.find("open?id=") != -1:
        file_id = link.split("open?id=")[1].strip()
    elif link.find("uc?id=") != -1:
        file_id = link.split("uc?id=")[1].strip()
    url = f"{drive}/uc?export=download&id={file_id}"
    async with _client() as client:
        download = await client.get(url, follow_redirects=False)
        try:
            # In case of small file size, Google downloads directly
            dl_url = download.headers["location"]
            if "accounts.google.com" in dl_url:  # non-public file
                reply += "`Link is not public!`\n"
                return reply
            name = "Direct Download Link"
        except KeyError:
            # In case of download warning page
            page = BeautifulSoup(download.content, "lxml")
            export = drive + page.find("a", {"id": "uc-download-link"}).get("href")
            name = page.find("span", {"class": "uc-name-size"}).text
            response = await client.get(export, follow_redirects=False)
            dl_url = response.headers["location"]
            if "accounts.google.com" in dl_url:
                reply += "Link is not public!"
                return reply
    reply += f"[{name}]({dl_url})\n"
    return reply


async def zippy_share(url: str) -> str:
    """ZippyShare direct links generator
    Based on https://github.com/LameLemon/ziggy"""
    reply = ""
    dl_url = ""
    try:
        link = re.findall(r"\bhttps?://.*zippyshare\.com\S+", url)[0]
    except IndexError:
        return "`No ZippyShare links found`\n"
    base_url = re.search("http.+.com", link).group()
    async with _client() as client:
        response = await client.get(link)
    page_soup = BeautifulSoup(response.content, "lxml")
    scripts = page_soup.find_all("script", {"type": "text/javascript"})
    for script in scripts:
        if "getElementById('dlbutton')" in script.text:
            url_raw = re.search(r"= (?P<url>\".+\" \+ (?P<math>\(.+\)) .+);", script.text)["url"]

            math = re.search(r"= (?P<url>\".+\" \+ (?P<math>\(.+\)) .+);", script.text)["math"]

            dl_url = url_raw.replace(math, f'"{str(eval(math))}"')
            break
    dl_url = base_url + eval(dl_url)
    name = urllib.parse.unquote(dl_url.split("/")[-1])
    reply += f"[{name}]({dl_url})\n"
    return reply


async def yandex_disk(url: str) -> str:
    """Yandex.Disk direct links generator
    Based on https://github.com/wldhx/yadisk-direct"""
    reply = ""
    try:
        link = re.findall(r"\bhttps?://.*yadi\.sk\S+", url)[0]
    except IndexError:
        return "`No Yandex.Disk links found`\n"
    api = "https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={}"
    try:
        async with _client() as client:
            dl_url = (await client.get(api.format(link))).json()["href"]
        name = dl_url.split("filename=")[1].split("&disposition")[0]
        reply += f"[{name}]({dl_url})\n"
    except KeyError:
        reply += "`Error: File not found / Download limit reached`\n"
        return reply
    return reply


async def mega_dl(url: str) -> str:
    """MEGA.nz direct links generator
    Using https://github.com/tonikelope/megadown"""
    reply = ""
    try:
        link = re.findall(r"\bhttps?://.*mega.*\.nz\S+", url)[0]
    except IndexError:
        return "`No MEGA.nz links found`\n"
    command = f"bin/megadown -q -m {link}"
    result = await _popen_read(command)
    try:
        data = json.loads(result)
        LOGS.info(data)
    except json.JSONDecodeError:
        reply += "`Error: Can't extract the link`\n"
        return reply
    dl_url = data["url"]
    name = data["file_name"]
    size = naturalsize(int(data["file_size"]))
    reply += f"[{name} ({size})]({dl_url})\n"
    return reply


async def cm_ru(url: str) -> str:
    """cloud.mail.ru direct links generator
    Using https://github.com/JrMasterModelBuilder/cmrudl.py"""
    reply = ""
    try:
        link = re.findall(r"\bhttps?://.*cloud\.mail\.ru\S+", url)[0]
    except IndexError:
        return "`No cloud.mail.ru links found`\n"
    command = f"bin/cmrudl -s {link}"
    result = await _popen_read(command)
    result = result.splitlines()[-1]
    try:
        data = json.loads(result)
    except json.decoder.JSONDecodeError:
        reply += "`Error: Can't extract the link`\n"
        return reply
    dl_url = data["download"]
    name = data["file_name"]
    size = naturalsize(int(data["file_size"]))
    reply += f"[{name} ({size})]({dl_url})\n"
    return reply


async def mediafire(url: str) -> str:
    """MediaFire direct links generator"""
    try:
        link = re.findall(r"\bhttps?://.*mediafire\.com\S+", url)[0]
    except IndexError:
        return "`No MediaFire links found`\n"
    reply = ""
    async with _client() as client:
        page = BeautifulSoup((await client.get(link)).content, "lxml")
    info = page.find("a", {"aria-label": "Download file"})
    dl_url = info.get("href")
    size = re.findall(r"\(.*\)", info.text)[0]
    name = page.find("div", {"class": "filename"}).text
    reply += f"[{name} {size}]({dl_url})\n"
    return reply


async def sourceforge(url: str) -> str:
    """SourceForge direct links generator"""
    try:
        link = re.findall(r"\bhttps?://.*sourceforge\.net\S+", url)[0]
    except IndexError:
        return "`No SourceForge links found`\n"
    file_path = re.findall(r"files([\s\S]*)/download", link)[0]
    reply = f"Mirrors for __{file_path.split('/')[-1]}__\n"
    project = re.findall(r"projects?/(.*?)/files", link)[0]
    mirrors = f"https://sourceforge.net/settings/mirror_choices?projectname={project}&filename={file_path}"
    async with _client() as client:
        page = BeautifulSoup((await client.get(mirrors)).content, "html.parser")
    info = page.find("ul", {"id": "mirrorList"}).findAll("li")
    for mirror in info[1:]:
        name = re.findall(r"\(([\s\S]*)\)", mirror.text.strip())[0]
        dl_url = f"https://{mirror['id']}.dl.sourceforge.net/project/{project}/{file_path}"
        reply += f"[{name}]({dl_url}) "
    return reply


async def osdn(url: str) -> str:
    """OSDN direct links generator"""
    osdn_link = "https://osdn.net"
    try:
        link = re.findall(r"\bhttps?://.*osdn\.net\S+", url)[0]
    except IndexError:
        return "`No OSDN links found`\n"
    async with _client() as client:
        page = BeautifulSoup((await client.get(link)).content, "lxml")
    info = page.find("a", {"class": "mirror_link"})
    link = urllib.parse.unquote(osdn_link + info["href"])
    reply = f"Mirrors for __{link.split('/')[-1]}__\n"
    mirrors = page.find("form", {"id": "mirror-select-form"}).findAll("tr")
    for data in mirrors[1:]:
        mirror = data.find("input")["value"]
        name = re.findall(r"\(([\s\S]*)\)", data.findAll("td")[-1].text.strip())[0]
        dl_url = re.sub(r"m=([\s\S]*)&f", f"m={mirror}&f", link)
        reply += f"[{name}]({dl_url}) "
    return reply


async def github(url: str) -> str:
    """GitHub direct links generator"""
    try:
        link = re.findall(r"\bhttps?://.*github\.com.*releases\S+", url)[0]
    except IndexError:
        return "`No GitHub Releases links found`\n"
    reply = ""
    dl_url = ""
    async with _client() as client:
        download = await client.get(url, follow_redirects=False)
    try:
        dl_url = download.headers["location"]
    except KeyError:
        reply += "`Error: Can't extract the link`\n"
    name = link.split("/")[-1]
    reply += f"[{name}]({dl_url}) "
    return reply


async def androidfilehost(url: str) -> str:
    """AFH direct links generator"""
    try:
        link = re.findall(r"\bhttps?://.*androidfilehost.*fid.*\S+", url)[0]
    except IndexError:
        return "`No AFH links found`\n"
    fid = re.findall(r"\?fid=([\s\S]*)", link)[0]
    user_agent = await useragent()
    headers = {"user-agent": user_agent}
    client = _client()
    await client.get(link, headers=headers)
    headers = {
        "origin": "https://androidfilehost.com",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "user-agent": user_agent,
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "x-mod-sbb-ctype": "xhr",
        "accept": "*/*",
        "referer": f"https://androidfilehost.com/?fid={fid}",
        "authority": "androidfilehost.com",
        "x-requested-with": "XMLHttpRequest",
    }
    data = {"submit": "submit", "action": "getdownloadmirrors", "fid": f"{fid}"}
    mirrors = None
    reply = ""
    error = "`Error: Can't find Mirrors for the link`\n"
    try:
        req = await client.post(
            "https://androidfilehost.com/libs/otf/mirrors.otf.php",
            headers=headers,
            data=data,
        )
        mirrors = req.json()["MIRRORS"]
    except (json.decoder.JSONDecodeError, TypeError):
        reply += error
    finally:
        await client.aclose()
    if not mirrors:
        reply += error
        return reply
    for item in mirrors:
        name = item["name"]
        dl_url = item["url"]
        reply += f"[{name}]({dl_url}) "
    return reply


async def useragent():
    """
    useragent random setter
    """
    async with _client() as client:
        resp = await client.get("https://developers.whatismybrowser.com/useragents/explore/operating_system_name/android/")
    useragents = BeautifulSoup(resp.content, "lxml").findAll("td", {"class": "useragent"})
    user_agent = choice(useragents)
    return user_agent.text


async def anonfiles(url: str) -> str:
    reply = ""
    async with _client() as client:
        html_s = (await client.get(url)).content
    soup = BeautifulSoup(html_s, "html.parser")
    _url = soup.find("a", attrs={"class": "btn-primary"})["href"]
    name = _url.rsplit("/", 1)[1]
    dl_url = _url.replace(" ", "%20")
    reply += f"[{name}]({dl_url})\n"
    return reply


"""
def onedrive(link: str) -> str:
    link_without_query = urlparse(link)._replace(query=None).geturl()
    direct_link_encoded = str(
        standard_b64encode(bytes(link_without_query, "utf-8")), "utf-8"
    )
    direct_link1 = (
        f"https://api.onedrive.com/v1.0/shares/u!{direct_link_encoded}/root/content"
    )
    resp = requests.head(direct_link1)
    if resp.status_code != 302:
        return "`Error: Unauthorized link, the link may be private`"
    dl_link = resp.next.url
    file_name = dl_link.rsplit("/", 1)[1]
    resp2 = requests.head(dl_link)
    dl_size = humanbytes(int(resp2.headers["Content-Length"]))
    return f"[{file_name} ({dl_size})]({dl_link})"
"""
