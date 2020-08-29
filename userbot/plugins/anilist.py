"""	
Anilist Search Plugin for Userbot	
Usage : .anilist animeName	
By :- @Zero_cool7870	
"""
 
import re
import json
import asyncio
import requests
from .. import CMD_HELP
from ..utils import admin_cmd, sudo_cmd, edit_or_reply

async def callAPI(search_str):
    query = '''
    query ($id: Int,$search: String) { 
      Media (id: $id, type: ANIME,search: $search) { 
        id
        title {
          romaji
          english
        }
        description (asHtml: false)
        startDate{
            year
          }
          episodes
          chapters
          volumes
          season
          type
          format
          status
          duration
          averageScore
          genres
          bannerImage
      }
    }
    '''
    variables = {
        'search' : search_str
    }
    url = 'https://graphql.anilist.co'
    response = requests.post(url, json={'query': query, 'variables': variables})
    return response.text

async def formatJSON(outData):
    msg = ""
    jsonData = json.loads(outData)
    res = list(jsonData.keys())
    if "errors" in res:
        msg += f"**Error** : `{jsonData['errors'][0]['message']}`"
        return msg
    jsonData = jsonData['data']['Media']
    if "bannerImage" in jsonData.keys():
        msg += f"[〽️]({jsonData['bannerImage']})"
    else :
        msg += "〽️"
    title = jsonData['title']['romaji']
    link = f"https://anilist.co/anime/{jsonData['id']}"
    msg += f"[{title}]({link})"
    msg += f"\n\n**Type** : {jsonData['format']}"
    msg += f"\n**Genres** : "
    for g in jsonData['genres']:
        msg += g+" "
    msg += f"\n**Status** : {jsonData['status']}"
    msg += f"\n**Episode** : {jsonData['episodes']}"
    msg += f"\n**Year** : {jsonData['startDate']['year']}"
    msg += f"\n**Score** : {jsonData['averageScore']}"
    msg += f"\n**Duration** : {jsonData['duration']} min\n\n"
    #https://t.me/catuserbot_support/19496
    cat = f"{jsonData['description']}"
    msg += " __" + re.sub("<br>", '\n', cat) +"__"
    return msg

@borg.on(admin_cmd(pattern="anilist (.*)"))
@borg.on(sudo_cmd(pattern="anilist (.*)",allow_sudo = True))
async def anilist(event):
    input_str = event.pattern_match.group(1)
    event = await edit_or_reply(event , "Searching...")
    result = await callAPI(input_str)
    msg = await formatJSON(result)
    await event.edit(msg,link_preview=True)

CMD_HELP.update({
    "anilist":
    "**anilist**\
    \n**Syntax : **`.anilist <anime name >`\
    \n**Usage : **Shows you the details of the anime."
})
