# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# Credits @Smart_S54.

from covid import Covid
from userbot import CMD_HELP
from userbot.utils import admin_cmd , sudo_cmd
from userbot.events import register


@borg.on(admin_cmd(pattern="cor (.*)"))
async def corona(event):
    await event.edit("`Wait Processing...🥺😭`")
    country = event.pattern_match.group(1)
    covid = Covid(source="worldometers")
    try:
        country_data = covid.get_status_by_country_name(country)
        output_text = (
            f"👤 **Confirmed     :** `{country_data['confirmed']}`\n" +
            f"😔 **Active        :** `{country_data['active']}`\n" +
            f"💀 **Deaths        :** `{country_data['deaths']}`\n" +
            f"😇 **Recovered     :** `{country_data['recovered']}`\n\n" +
            f"😕 **New Cases     :** `{country_data['new_cases']}`\n" +
            f"😭 **New Deaths    :** `{country_data['new_deaths']}`\n" +
            f"😥 **Critical      :** `{country_data['critical']}`\n" +
            f"😔 **Total Tests   :** `{country_data['total_tests']}`\n\n" +
            f"🌐 **Data provided by** [Worldometer](https://www.worldometers.info/coronavirus/country/{country})")
        await event.edit(f"__**🦠 Corona Virus Info in {country}:**__\n\n{output_text}")
    except ValueError:
        await event.edit(
            f"__**💤 No information found for: {country}!**__\n__**Check your spelling and try again.**__"
        )

@borg.on(sudo_cmd(pattern="cor (.*)", allow_sudo = True))
async def corona(event):
    country = event.pattern_match.group(1)
    covid = Covid(source="worldometers")
    try:
        country_data = covid.get_status_by_country_name(country)
        output_text = (
            f"👤 **Confirmed     :** `{country_data['confirmed']}`\n" +
            f"😔 **Active        :** `{country_data['active']}`\n" +
            f"💀 **Deaths        :** `{country_data['deaths']}`\n" +
            f"😇 **Recovered     :** `{country_data['recovered']}`\n\n" +
            f"😕 **New Cases     :** `{country_data['new_cases']}`\n" +
            f"😭 **New Deaths    :** `{country_data['new_deaths']}`\n" +
            f"😥 **Critical      :** `{country_data['critical']}`\n" +
            f"😔 **Total Tests   :** `{country_data['total_tests']}`\n\n" +
            f"🌐 **Data provided by** __**Worldometer**__")
        await event.reply(f"__**🦠 Corona Virus Info in {country}:**__\n\n{output_text}")
    except ValueError:
        await event.reply(
            f"__**💤 No information found for: {country}!**__\n__**Check your spelling and try again.**__"
        )
    
CMD_HELP.update({
    "covid":
        "`.cor` <country>"
        "\nUsage: Get an information about data covid-19 in your country.\n"
})
