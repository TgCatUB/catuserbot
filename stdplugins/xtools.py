# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from telethon import events
from datetime import datetime
import requests
from uniborg.util import admin_cmd


@borg.on(admin_cmd(pattern="xtools (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    start = datetime.now()
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        username = previous_message.message
        sub_domain = input_str
    else:
        sub_domain, username = input_str.split("|")
    final_url = "https://xtools.wmflabs.org/api/user/simple_editcount/{}.wikipedia.org/{}".format(sub_domain, username)
    json_string = requests.get(final_url).json()
    result_text = json_string["liveEditCount"]
    end = datetime.now()
    ms = (end - start).seconds
    output_str = "edit count of {} ({}) in {} seconds. \n {}".format(
        username, sub_domain, str(ms), result_text)
    await event.edit(output_str)
