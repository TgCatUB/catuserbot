"""	
	Anilist Search Plugin for Userbot	
	Usage : .anilist animeName	
	By :- @Zero_cool7870	
"""

import requests 
import re
import json
import asyncio
from userbot import CMD_HELP
from userbot.utils import admin_cmd

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
    else:
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

@borg.on(admin_cmd(pattern="anilist ?(.*)"))
async def anilist(event):
	if event.fwd_from:
		return
	input_str = event.pattern_match.group(1)
	result = await callAPI(input_str)
	msg = await formatJSON(result)
	await event.edit(msg,link_preview=True)

CMD_HELP.update({
    "anilist":
    ".anilist <anime name >\
     \nUSAGE: Shows you the details of the anime."
})
