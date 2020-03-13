"""
Anime Batch Downloader Plugin for userbot. //set TEMP_DIR Env Var first.
usage:- get a link of Animefrenzy.net Anime page and use in cmd.
cmd:- .anime page_link
By:- @Zero_cool7870	  

"""
from telethon import events
import asyncio
from bs4 import BeautifulSoup as bs 
import requests
import os
from userbot.utils import admin_cmd

chunk_size =  3242880


async def get_file_name(link):
	new_link = link[26:]
	l = ""
	for c in new_link:
		if c =='?':
			break
		l = l + c	
	l = l.replace("/","_")
	return l

async def download_file(url,filename):
	response = requests.get(url, stream=True)
	handle = open(filename, "wb")
	for chunk in response.iter_content(chunk_size=chunk_size):
		if chunk:  # filter out keep-alive new chunks
			handle.write(chunk)
	handle.close()   

@borg.on(admin_cmd(pattern=r"danime"))
async def anime_download(event):
	urls = []
	url_links = []
	if event.fwd_from:
		return   
	if Config.TEMP_DIR is None:
		await event.edit("Please Set Required ENV Variables First.")
		return
	download_dir=Config.TEMP_DIR	
	try:
		os.makedirs(download_dir)
	except:
		pass	
	
	var = event.text
	var = var[6:]
	res = requests.get(var)
	source = bs(res.text,'lxml')

	for a in source.find_all('a',{'class':'infovan'}):
		url_links.append(a['href'])

	for i in url_links:
		res = requests.get(i)
		source = bs(res.text,'lxml')

		for a in source.find_all('a',{'class':'an'}):
			urls.append(a['href'])
		print("Getting Link...")	
			
	
	counter = 0
	for url in urls:
		if "download.php?" in url:
			urls.pop(counter)	
		counter = counter + 1 

	counter = 0	
	for url in urls:
		if "#" in url:
			urls.pop(counter)	
		counter = counter + 1 
	await event.edit("Downloading Episodes...")
	
	for i in urls:
		filename = await get_file_name(i)
		print(filename)
		filename = download_dir+"/"+filename
		await download_file(i,filename)
	await event.edit("All Episodes Downloaded.")		
