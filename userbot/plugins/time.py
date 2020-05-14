""" It does not do to dwell on dreams and forget to live
Syntax: .getime"""

import asyncio
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from userbot.utils import admin_cmd,register


FONT_FILE_TO_USE = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


from datetime import datetime as dt

from pytz import country_names as c_n
from pytz import country_timezones as c_tz
from pytz import timezone as tz

from userbot import CMD_HELP, COUNTRY, TZ_NUMBER



async def get_tz(con):
    """ Get time zone of the given country. """
    if "(Uk)" in con:
        con = con.replace("Uk", "UK")
    if "(Us)" in con:
        con = con.replace("Us", "US")
    if " Of " in con:
        con = con.replace(" Of ", " of ")
    if "(Western)" in con:
        con = con.replace("(Western)", "(western)")
    if "Minor Outlying Islands" in con:
        con = con.replace("Minor Outlying Islands", "minor outlying islands")
    if "Nl" in con:
        con = con.replace("Nl", "NL")

    for c_code in c_n:
        if con == c_n[c_code]:
            return c_tz[c_code]
    try:
        if c_n[con]:
            return c_tz[con]
    except KeyError:
        return


@register(outgoing=True, pattern="^.ctime(?: |$)(.*)(?<![0-9])(?: |$)([0-9]+)?")
async def time_func(tdata):
    """ For .time command, return the time of
        1. The country passed as an argument,
        2. The default userbot country(set it by using .settime),
        3. The server where the userbot runs.
    """
    con = tdata.pattern_match.group(1).title()
    tz_num = tdata.pattern_match.group(2)

    t_form = "%H:%M"
    c_name = None

    if len(con) > 4:
        try:
            c_name = c_n[con]
        except KeyError:
            c_name = con
        timezones = await get_tz(con)
    elif COUNTRY:
        c_name = COUNTRY
        tz_num = TZ_NUMBER
        timezones = await get_tz(COUNTRY)
    else:
        await tdata.edit(f"`It's`  **{dt.now().strftime(t_form)}**  `here.`")
        return

    if not timezones:
        await tdata.edit("`Invaild country.`")
        return

    if len(timezones) == 1:
        time_zone = timezones[0]
    elif len(timezones) > 1:
        if tz_num:
            tz_num = int(tz_num)
            time_zone = timezones[tz_num - 1]
        else:
            return_str = f"`{c_name} has multiple timezones:`\n\n"

            for i, item in enumerate(timezones):
                return_str += f"`{i+1}. {item}`\n"

            return_str += "\n`Choose one by typing the number "
            return_str += "in the command.`\n"
            return_str += f"`Example: .time {c_name} 2`"

            await tdata.edit(return_str)
            return

    dtnow = dt.now(tz(time_zone)).strftime(t_form)

    if c_name != COUNTRY:
        await tdata.edit(
            f"`It's`  **{dtnow}**  `in {c_name}({time_zone} timezone).`")
        return

    elif COUNTRY:
        await tdata.edit(f"`It's`  **{dtnow}**  `here, in {COUNTRY}"
                         f"({time_zone} timezone).`")
        return


@register(outgoing=True, pattern="^.cdate(?: |$)(.*)(?<![0-9])(?: |$)([0-9]+)?")
async def date_func(dat):
    """ For .date command, return the date of
        1. The country passed as an argument,
        2. The default userbot country(set it by using .settime),
        3. The server where the userbot runs.
    """
    con = dat.pattern_match.group(1).title()
    tz_num = dat.pattern_match.group(2)

    d_form = "%d/%m/%y - %A"
    c_name = ''

    if len(con) > 4:
        try:
            c_name = c_n[con]
        except KeyError:
            c_name = con
        timezones = await get_tz(con)
    elif COUNTRY:
        c_name = COUNTRY
        tz_num = TZ_NUMBER
        timezones = await get_tz(COUNTRY)
    else:
        await dat.edit(f"`It's`  **{dt.now().strftime(d_form)}**  `here.`")
        return

    if not timezones:
        await dat.edit("`Invaild country.`")
        return

    if len(timezones) == 1:
        time_zone = timezones[0]
    elif len(timezones) > 1:
        if tz_num:
            tz_num = int(tz_num)
            time_zone = timezones[tz_num - 1]
        else:
            return_str = f"`{c_name} has multiple timezones:`\n"

            for i, item in enumerate(timezones):
                return_str += f"`{i+1}. {item}`\n"

            return_str += "\n`Choose one by typing the number "
            return_str += "in the command.`\n"
            return_str += f"Example: .date {c_name} 2"

            await dat.edit(return_str)
            return

    dtnow = dt.now(tz(time_zone)).strftime(d_form)

    if c_name != COUNTRY:
        await dat.edit(
            f"`It's`  **{dtnow}**  `in {c_name}({time_zone} timezone).`")
        return

    elif COUNTRY:
        await dat.edit(f"`It's`  **{dtnow}**  `here, in {COUNTRY}"
                       f"({time_zone} timezone).`")
        return





@borg.on(admin_cmd(pattern="time ?(.*)"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    current_time = datetime.now().strftime("⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡ \n⚡USERBOT TIMEZONE⚡ \n LOCATION: India \n  Time: %H:%M:%S \n  Date: %d.%m.%y \n⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡")
    start = datetime.now()
    input_str = event.pattern_match.group(1)
    reply_msg_id = event.message.id
    if input_str:
        current_time = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        reply_msg_id = previous_message.id
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):  # pylint:disable=E0602
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)  # pylint:disable=E0602
    # pylint:disable=E0602
    required_file_name = Config.TMP_DOWNLOAD_DIRECTORY + " " + str(datetime.now()) + ".webp"
    img = Image.new("RGBA", (350, 220), color=(0, 0, 0, 115))
    fnt = ImageFont.truetype(FONT_FILE_TO_USE, 30)
    drawn_text = ImageDraw.Draw(img)
    drawn_text.text((10, 10), current_time, font=fnt, fill=(255, 255, 255))
    img.save(required_file_name)
    await borg.send_file(  # pylint:disable=E0602
        event.chat_id,
        required_file_name,
        caption="Userbot: Powered by @XtraTgBot",
        # Courtesy: @ManueI15
        reply_to=reply_msg_id
    )
    os.remove(required_file_name)
    end = datetime.now()
    time_taken_ms = (end - start).seconds
    await event.edit("Created sticker in {} seconds".format(time_taken_ms))
    await asyncio.sleep(5)
    await event.delete()


@borg.on(admin_cmd(pattern="gtime (.*)"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    logger.info(input_str)  # pylint:disable=E0602

    
CMD_HELP.update({
    "time":
    ".ctime <country name/code> <timezone number>"
    "\nUsage: Get the time of a country. If a country has "
    "multiple timezones, it will list all of them "
    "and let you select one."
    ".cdate <country name/code> <timezone number>"
    "\nUsage: Get the date of a country. If a country has "
    "multiple timezones, it will list all of them "
    "and let you select one."
})    
