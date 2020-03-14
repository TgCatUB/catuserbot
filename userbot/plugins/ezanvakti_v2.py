import asyncio
import datetime
import json
import logging
import os
import requests
from telethon import events
from unicode_tr import unicode_tr
# from ..bin.namaz_vakti import namazvakti
from userbot.utils import admin_cmd
from datetime import datetime
import pytz
# from bin.namaz_vakti import namazvakti
from bin.namaz_vakti.namazvakti import namazvakti
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

TEMP = ''


@borg.on(admin_cmd(pattern=("ezanv ?(.*) + ?(.*)")))
async def namaz_(event):
    """kullanımı .ezanv <şehir> <ilçe>"""
    if not event.text.startswith("."):
        return ""

    if not event.pattern_match.group(1):
        LOKASYON = TEMP
        if not LOKASYON:
            await event.edit("Please specify a city or a state.")
            return
    else:
        LOKASYON = event.pattern_match.group(1)
        if LOKASYON:
            LOKASYON = LOKASYON.replace('i', 'İ').upper()
    
        # LOKASYON = LOKASYON.encode().decode('UTF-8').upper()
    # await event.edit("ezan vakti diyanetten alınıyor.")
    if not event.pattern_match.group(2):
        await event.edit("ilçe giriniz. doğru format `.ezanv <şehir> <ilçe>`")
    else:
        LOKASYON_2 = event.pattern_match.group(2)
        if LOKASYON_2:
            LOKASYON_2 = LOKASYON_2.replace('i','İ').upper()
    yer = './bin/namaz_vakti/db/yerler.ndb'
    with open(yer, "r", encoding="utf-8") as f:
        yerler_json = json.load(f)
    namaz = namazvakti()
    sehirler_sonuc = namaz.sehirler(2)
    sonuc_sehirler = {v: k for k, v in sehirler_sonuc['veri'].items()}
    # print(sonuc_sehirler)
    sehir_id = sonuc_sehirler[LOKASYON]
    # print(sehir_id)
    ilceler_sonuc = namaz.ilceler(2, sehir_id)
    # print(ilceler_sonuc)
    sonuc_ilceler = {v: k for k, v in ilceler_sonuc['veri'].items()}
    # print(sonuc_ilceler)    
    # print(event.pattern_match.group(2).upper())
    # print(yerler_json['2']['sehirler'][f"{sonuc_sehirler_1}"]['ilceler'].items())
    # inverse_yerler = {v: k for k, v in yerler_json['2']['sehirler'][f"{sonuc_sehirler_1}"]['ilceler'].items()}
    # print(inverse_yerler[LOKASYON])
    sonuc_str = sonuc_ilceler[LOKASYON_2]
    # print(sonuc_str)
    # print(sonuc_str)
    sonuc = namaz.vakit(sonuc_str)
    
    
    tz = pytz.timezone('Europe/Istanbul')
    istanbul_now = datetime.now(tz)
    bugun = istanbul_now.strftime("%d%m%Y")
    
    gun =bugun[0:2]
    ay = bugun[2:4]
    yil = bugun[4:]
    tam_gun = gun + "." + ay + "." + yil
    print(sonuc)
    # tam_gun = int(tam_gun)
    # print(sonuc)
    yer = sonuc['veri']['yer_adi']
    if sonuc['veri']['vakit']['tarih'] == tam_gun:
        # print("tru")
        tarih = sonuc['veri']['vakit']['uzun_tarih']
        hicri_tarih = sonuc['veri']['vakit']['hicri_uzun']
        imsak = sonuc['veri']['vakit']['imsak']
        gunes = sonuc['veri']['vakit']['gunes']
        ogle = sonuc['veri']['vakit']['ogle']
        ikindi = sonuc['veri']['vakit']['ikindi']
        aksam = sonuc['veri']['vakit']['aksam']
        yatsi = sonuc['veri']['vakit']['yatsi']
    out = (f"**Diyanet Namaz Vakitleri**\n\n" +
                f"📍**Yer: ** `{yer}`\n" +
                f"🗓**Tarih ** `{tarih}`\n" +
                f"🌕**Hicri Tarih :** `{hicri_tarih}`\n"+
                f"🏙**İmsak :** `{imsak}`\n" +
                f"🌅**Güneş :** `{gunes}`\n" +
                f"🌇**Öğle :** `{ogle}`\n" +
                f"🌆**İkindi :** `{ikindi}`\n" +
                f"🌃**Akşam :** `{aksam}`\n" +
                f"🌌**Yatsı :** `{yatsi}`\n"
    )
    await event.edit(out)
    # print(inverse_yerler)
    # yerlerim = inverse_yerler[LOKASYON]
    # await event.edit(sonuc)

#    print(sonuc_sehirler[LOKASYON])
#     print(LOKASYON)

    # url = f'http://muslimsalat.com/{LOKASI}.json?key=bd099c5825cbedb9aa934e255a81a5fc'
    # request = requests.get(url)
    # result = json.loads(request.text)

    # if request.status_code != 200:
    #     await namaz.edit(f"{result['status_description']}")
    #     return

    # tanggal = result["items"][0]["date_for"]
    # lokasi = result["query"]
    # lokasi2 = result["country"]
    # lokasi3 = result["address"]
    # lokasi4 = result["state"]

    # subuh = result["items"][0]["fajr"]
    # syuruk = result["items"][0]["shurooq"]
    # zuhur = result["items"][0]["dhuhr"]
    # ashar = result["items"][0]["asr"]
    # maghrib = result["items"][0]["maghrib"]
    # isya = result["items"][0]["isha"]

    # textkirim = (f"⏱  **Tarih ** `{tanggal}`:\n" +
    #              f"`{lokasi} | {lokasi2} | {lokasi3} | {lokasi4}`\n\n" +
    #              f"**Güneş :** `{subuh}`\n" +
    #              f"**İmsak :** `{syuruk}`\n" +
    #              f"**Öğle :** `{zuhur}`\n" +
    #              f"**İkindi :** `{ashar}`\n" +
    #              f"**Akşam :** `{maghrib}`\n" +
    #              f"**Yatsı :** `{isya}`\n")

    # await namaz.edit(textkirim)
