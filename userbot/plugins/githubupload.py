"""
GITHUB File Uploader Plugin for userbot. Heroku Automation should be Enabled. Else u r not that lazy // For lazy people
Instructions:- Set GITHUB_ACCESS_TOKEN and GIT_REPO_NAME Variables in Heroku vars First
usage:- .commit reply_to_any_plugin //can be any type of file too. but for plugin must be in .py 
"""


from github import Github
import aiohttp
import asyncio
import os
import time
from datetime import datetime
from telethon import events
from telethon.tl.types import DocumentAttributeVideo


GIT_TEMP_DIR = "./userbot/temp/"
@command(pattern="^.commit", outgoing=True)
async def download(event):
    if event.fwd_from:
        return	
    if Var.GITHUB_ACCESS_TOKEN is None:
        await event.edit("`Please ADD Proper Access Token from github.com`") 
        return   
    if Var.GIT_REPO_NAME is None:
        await event.edit("`Please ADD Proper Github Repo Name of your userbot`")
        return 
    mone = await event.reply("Processing ...")
    if not os.path.isdir(GIT_TEMP_DIR):
        os.makedirs(GIT_TEMP_DIR)
    start = datetime.now()
    reply_message = await event.get_reply_message()
    try:
        c_time = time.time()
        print("Downloading to TEMP directory")
        downloaded_file_name = await bot.download_media(
                reply_message.media,
                GIT_TEMP_DIR
            )
    except Exception as e: 
        await mone.edit(str(e))
    else:
        end = datetime.now()
        ms = (end - start).seconds
        await event.delete()
        await mone.edit("Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms))
        await mone.edit("Committing to Github....")
        await git_commit(downloaded_file_name, mone)

async def git_commit(file_name,mone):        
    content_list = []
    access_token = Var.GITHUB_ACCESS_TOKEN
    g = Github(access_token)
    file = open(file_name,"r",encoding='utf-8')
    commit_data = file.read()
    repo = g.get_repo(Var.GIT_REPO_NAME)
    print(repo.name)
    create_file = True
    contents = repo.get_contents("")
    for content_file in contents:
        content_list.append(str(content_file))
        print(content_file)
    for i in content_list:
        create_file = True
        if i == 'ContentFile(path="'+file_name+'")':
            return await mone.edit("`File Already Exists`")
            create_file = False
    file_name = "userbot/plugins/" + file_name		
    if create_file == True:
        file_name = file_name.replace("./userbot/temp/","")
        print(file_name)
        try:
            repo.create_file(file_name, "Uploaded New Plugin", commit_data, branch="master")
            print("Committed File")
            ccess = Var.GIT_REPO_NAME
            ccess = ccess.strip()
            await mone.edit(f"`Commited On Your Github Repo`\n\n[Your STDPLUGINS](https://github.com/{ccess}/tree/master/userbot/plugins/)")
        except:    
            print("Cannot Create Plugin")
            await mone.edit("Cannot Upload Plugin")
    else:
        return await mone.edit("`Committed Suicide`")
