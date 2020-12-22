"""Get info about a File Extension
Syntax: .filext EXTENSION"""

import requests
from bs4 import BeautifulSoup


@bot.on(admin_cmd(pattern="filext (.*)"))
@bot.on(sudo_cmd(pattern="filext (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    sample_url = "https://www.fileext.com/file-extension/{}.html"
    input_str = event.pattern_match.group(1).lower()
    response_api = requests.get(sample_url.format(input_str))
    status_code = response_api.status_code
    if status_code == 200:
        raw_html = response_api.content
        soup = BeautifulSoup(raw_html, "html.parser")
        ext_details = soup.find_all("td", {"colspan": "3"})[-1].text
        await edit_or_reply(
            event,
            "**File Extension**: `{}`\n**Description**: `{}`".format(
                input_str, ext_details
            ),
        )
    else:
        await edit_or_reply(
            event,
            "https://www.fileext.com/ responded with {} for query: {}".format(
                status_code, input_str
            ),
        )


CMD_HELP.update(
    {
        "filext": """**Plugin : **`filext`
    
  • **Syntax : **`.filext <extension name>`
  • **Function : **__Shows you the detailed information that extension type__"""
    }
)
