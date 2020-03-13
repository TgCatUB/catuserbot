"""
Check Current Beta firmwares of Samsung Devices
Syntax: .check androidVersion modelNumber
By :- Jaskaran ^_^ 
Telegram :- @Zero_cool7870

"""

from asyncio import wait
import time
import gc
from telegraph import Telegraph
from bs4 import BeautifulSoup as bs
import requests
from telethon import events
from userbot.utils import admin_cmd

telegraph = Telegraph()
telegraph.create_account(short_name='zeroc')
chat_ids = [596701090,517742107]
csclist = ['ACG', 
                'ATT', 
                'BST', 
                'CCT', 
                'GCF', 
                'LRA', 
                'SPR', 
                'TFN', 
                'TMB', 
                'USC', 
                'VMU', 
                'VZW', 
                'XAA', 
                'XAS',
                'AFG',
                'TMC',
                'TTR',
                'DRE',
                'MOB',
                'MAX',
                'TRG',
                'SEB',
                'PRO',
                'TEB',
                'BHT',
                'GBL',
                'BGL',
                'MTL',
                'VVT',
                'CAM',
                'CAU',
                'DHR',
                'CRO',
                'TWO',
                'VIP',
                'CYV',
                'CYO',
                'ETL',
                'O2C',
                'TMZ',
                'VDC',
                'EGY',
                'XEF',
                'BOG',
                'FTM',
                'SFR',
                'DBT',
                'XEG',
                'DDE',
                'VIA',
                'DTM',
                'VD2',
                'EUR',
                'COS',
                'VGR',
                'XEH',
                'TMH',
                'PAN',
                'VDH',
                'XSE',
                'XID',
                'THR',
                'MID',
                'TSI',
                'MET',
                '3IE',
                'VDI',
                'ILO',
                'CEL',
                'PTR',
                'PCL',
                'ITV',
                'HUI',
                'TIM',
                'OMN',
                'WIN',
                'SKZ',
                'AFR',
                'KEN',
                'BTC',
                'LUX',
                'VIM',
                'MBM',
                'XME',
                'MRU',
                'TMT',
                'MAT',
                'MWD',
                'PHN',
                'DNL',
                'TNL',
                'VDF',
                'ECT',
                'NEE',
                'TEN',
                'ATO',
                'PAK',
                'GLB',
                'XTC',
                'SMA',
                'XTE',
                'XEO',
                'DPL',
                'IDE',
                'PLS',
                'PRT',
                'TPL',
                'MEO',
                'OPT',
                'TPH',
                'TCL',
                'ROM',
                'COA',
                'ORO',
                'CNX',
                'SER',
                'ACR',
                'WTL',
                'XFU',
                'TSR',
                'MSR',
                'TOP',
                'ORX',
                'TMS',
                'SIO',
                'MOT',
                'SIM',
                'XFE',
                'XFA',
                'XFV',
                'SEE',
                'PHE',
                'XEC',
                'AMO',
                'ATL',
                'VDS',
                'HTS',
                'AUT',
                'SWC',
                'THL',
                'TUN',
                'SEK',
                'XSG',
                'LYS',
                'VIR',
                'BTU',
                'EVR',
                'H3G',
                'O2U',
                'VOD',
                'XEU',
                'TPD',
                'ANP',
                'CAC',
                'XXV',
                'MTZ',
                'ARO',
                'ANC',
                'CTI',
                'UFN',
                'PSN',
                'XSA',
                'OPS',
                'TEL',
                'VAU',
                'BNG',
                'BVO',
                'ZTO',
                'ZTA',
                'ZTR',
                'ZTM',
                'ZVV',
                'CHO',
                'CRC',
                'CHL',
                'CHE',
                'CHX',
                'CHT',
                'CHV',
                'COO',
                'COM',
                'COE',
                'COB',
                'ICE',
                'CDR',
                'DOR',
                'EBE',
                'ECO',
                'VFJ',
                'TGU',
                'PGU',
                'CGU',
                'INU',
                'INS',
                'JDI',
                'CWW',
                'IUS',
                'TMM',
                'TCE',
                'NPL',
                'NZC',
                'TNZ',
                'VNZ',
                'PBS',
                'TPA',
                'PCW',
                'CPA',
                'PNG',
                'CTP',
                'PSP',
                'TGP',
                'PET',
                'PNT',
                'SAM',
                'PVT',
                'PCT',
                'KSA',
                'XSP',
                'MM1',
                'SIN',
                'STH',
                'CRM',
                'NBS',
                'SLK',
                'TTT',
                'TUR',
                'EON',
                'COD',
                'MNX',
                'UFU',
                'UPO',
                'CTU',
                'KTC',
                'LUC',
                'SKC',
                'CHC',
                'TGY',
                'CHM',
                'BRI',
                'CTC']         

csclist = sorted(csclist)
@borg.on(admin_cmd(pattern=r"check"))
async def checker(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("Fetching Information, Wait!")
        print(e.text)
        messege = e.text
        modelnum = str(e.text)
        data = []
        abort = False
        flagship = False
        data = []
        piecount = int()
        piecount = 0
        counter = 0
        outandroid = 0
        modelnum = modelnum.upper()
        outandroid = modelnum[7]
        print(outandroid)
        url = "http://fota-cloud-dn.ospserver.net/firmware/"
        urlEnd = "/"+modelnum[9:]+"/version.test.xml"
        print(urlEnd)
        urlLinks = []
        out_msg = []
        try:
            outandroid = int(outandroid)
            temp = outandroid
        except ValueError:
            abort = True
            return
        for i in csclist:
            urlLinks.append(url + i + urlEnd)
        for i in urlLinks:
            r = requests.get(i)
            xmlResp = bs(r.text, 'lxml')
            try:
                latestVersion = xmlResp.findAll('latest')[0].string
                latestVersion=str(latestVersion)
                region = xmlResp.findAll('cc')[0].string
                model = xmlResp.findAll('model')[0].string
                print(region)
                # out_msg.append("Region: "+region)
                # out_msg.append("\nlatestVersion: "+latestVersion[:16])
                if outandroid != 0 and flagship != True:
                    data.append('<br/>'+'<b>Model</b> : '+model+'<br/>'+'<b>Region</b> : '+region+'<br/>'+'<b>Latest Version</b> : '+str(latestVersion[:16])+'<br/>')
                    if latestVersion[9] =="C" or latestVersion[10] == "C":
                        if outandroid == 7:
                            piecount = piecount+1
                        outandroid = outandroid + 2    
                        data.append('<b>Android Version</b> : '+str(outandroid)+'<br/>')    
                        #bot.reply_to(message,'Region : {}\nLatest Version : {}\nAndroid Version : {}\nNumber of Pie Testing Regions : {}'.format(region,latestVersion[:16],str(outandroid),piecount))
                    elif latestVersion[9] =="B" or latestVersion[10] == "B":
                        if outandroid == 8:
                            piecount = piecount + 1  
                        outandroid = outandroid + 1      
                        data.append('<b>Android Version</b> : '+str(outandroid)+'<br/>')    
                        #bot.reply_to(message,'Region : {}\nLatest Version : {}\nAndroid Version : {}\nNumber of Pie Testing Regions : {}'.format(region,latestVersion[:16],str(outandroid+1),piecount)) 
                    else:
                        if outandroid == 9:
                            piecount = piecount + 1
                        data.append('<b>Android Version</b> : '+str(outandroid)+'<br/>')    
                    #bot.reply_to(message,'Region : {}\nLatest Version : {}\nAndroid Version : {}\nNumber of Pie Testing Regions : {}'.format(region,latestVersion[:16],str(outandroid),piecount)) 
                    #print("\nAndroid Version : " + str(outandroid)+"\n")
            #bot.reply_to(message,'Region : {}\nLatest Version : {}'.format(region,latestVersion[:16]))
                data.append('--------------------------------------------------')
            except IndexError:
                pass
                gc.collect()
            outandroid = temp
        data.append('<br/><b>Number of Pie Tests</b> : '+str(piecount)+'<br/>')        
        data = str(data)
        data = data.replace("['","")
        data = data.replace(",","")
        data = data.replace("']","")
        data = data.replace("' '","")     
        response = telegraph.create_page(
        modelnum[9:],
        html_content = data
        )

        await e.edit("All Done !")
        await wait(
            [e.respond('Here is The Complete List of Firmwares for '+modelnum[9:]+' That are currently in testing '+': \nhttps://telegra.ph/{}'.format(response['path'])) ]
            )
        print("ALL DONE! Kthxbye now")
        await e.delete()
        
        
@borg.on(admin_cmd(pattern=r"otaup"))
async def checker(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("Fetching Information, Wait!")
        print(e.text)
        messege = e.text
        modelnum = str(e.text)
        data = []
        abort = False
        flagship = False
        data = []
        piecount = int()
        piecount = 0
        counter = 0
        outandroid = 0
        modelnum = modelnum.upper()
        outandroid = modelnum[7]
        print(outandroid)
        url = "http://fota-cloud-dn.ospserver.net/firmware/"
        urlEnd = "/"+modelnum[9:]+"/version.xml"
        print(urlEnd)
        urlLinks = []
        out_msg = []
        try:
            outandroid = int(outandroid)
            temp = outandroid
        except ValueError:
            abort = True
            return
        for i in csclist:
            urlLinks.append(url + i + urlEnd)
        for i in urlLinks:
            r = requests.get(i)
            xmlResp = bs(r.text, 'lxml')
            try:
                latestVersion = xmlResp.findAll('latest')[0].string
                latestVersion=str(latestVersion)
                region = xmlResp.findAll('cc')[0].string
                model = xmlResp.findAll('model')[0].string
                print(region)
                # out_msg.append("Region: "+region)
                # out_msg.append("\nlatestVersion: "+latestVersion[:16])
                if outandroid != 0 and flagship != True:
                    data.append('<br/>'+'<b>Model</b> : '+model+'<br/>'+'<b>Region</b> : '+region+'<br/>'+'<b>Latest Version</b> : '+str(latestVersion[:16])+'<br/>')
                    if latestVersion[9] =="C" or latestVersion[10] == "C":
                        if outandroid == 7:
                            piecount = piecount+1
                        outandroid = outandroid + 2    
                        data.append('<b>Android Version</b> : '+str(outandroid)+'<br/>')    
                        #bot.reply_to(message,'Region : {}\nLatest Version : {}\nAndroid Version : {}\nNumber of Pie Testing Regions : {}'.format(region,latestVersion[:16],str(outandroid),piecount))
                    elif latestVersion[9] =="B" or latestVersion[10] == "B":
                        if outandroid == 8:
                            piecount = piecount + 1  
                        outandroid = outandroid + 1      
                        data.append('<b>Android Version</b> : '+str(outandroid)+'<br/>')    
                        #bot.reply_to(message,'Region : {}\nLatest Version : {}\nAndroid Version : {}\nNumber of Pie Testing Regions : {}'.format(region,latestVersion[:16],str(outandroid+1),piecount)) 
                    else:
                        if outandroid == 9:
                            piecount = piecount + 1
                        data.append('<b>Android Version</b> : '+str(outandroid)+'<br/>')    
                    #bot.reply_to(message,'Region : {}\nLatest Version : {}\nAndroid Version : {}\nNumber of Pie Testing Regions : {}'.format(region,latestVersion[:16],str(outandroid),piecount)) 
                    #print("\nAndroid Version : " + str(outandroid)+"\n")
            #bot.reply_to(message,'Region : {}\nLatest Version : {}'.format(region,latestVersion[:16]))
                data.append('--------------------------------------------------')
            except IndexError:
                pass
                gc.collect()
            outandroid = temp
        data.append('<br/><b>Number of Pie Tests</b> : '+str(piecount)+'<br/>')        
        data = str(data)
        data = data.replace("['","")
        data = data.replace(",","")
        data = data.replace("']","")
        data = data.replace("' '","")     
        response = telegraph.create_page(
        modelnum[9:],
        html_content = data
        )

        await e.edit("All Done !")
        await wait(
            [e.respond('Here is The Complete List of Firmwares for '+modelnum[9:]+': \nhttps://telegra.ph/{}'.format(response['path'])) ]
            )
        print("ALL DONE! Kthxbye now")
        await e.delete()      
        
