"""CoronaVirus LookUp
Syntax: .corona <country>"""
from covid import Covid
from userbot.utils import admin_cmd
from userbot import CMD_HELP

@borg.on(admin_cmd(pattern="corona(?: |$)(.*)"))
async def corona(event):
    if event.pattern_match.group(1):
        country = event.pattern_match.group(1)
    else:
        country = "World"
    covid = Covid(source="worldometers")
    data = ""
    country_data = covid.get_status_by_country_name(country)
    if country_data:
        hmm1 = country_data['confirmed']+country_data['new_cases']
        hmm2 = country_data['deaths']+country_data['new_deaths']
        data +=  f"\n⚠️Confirmed   : `{hmm1}`"
        data +=  f"\n😔Active          : `{country_data['active']}`"
        data +=  f"\n⚰️Deaths        : `{hmm2}`"
        data +=  f"\n🤕Critical          : `{country_data['critical']}`"
        data +=  f"\n😊Recovered  : `{country_data['recovered']}`"
        data +=  f"\n💉Total tests   : `{country_data['total_tests']}`"
        data +=  f"\n🥺New Cases   : `{country_data['new_cases']}`"
        data +=  f"\n😟New Deaths : `{country_data['new_deaths']}`"
    else:
        data += "\nNo information yet about this country!"
    await event.edit("**Corona Virus Info in {}:**\n{}".format(country.capitalize(), data))

CMD_HELP.update({"coronavirus":
   "`.covid ` <country name>\
   \n**USAGE :** Get an information about covid-19 data in the given country."
})
