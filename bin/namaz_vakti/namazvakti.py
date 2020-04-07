# -*- coding: utf-8 -*-
import os
import json
from datetime import datetime
import requests 
from bs4 import BeautifulSoup
from convertdate import islamic
import pathlib



class namazvakti():
    ulkeIsimleri = {}
    sehirIsimleri = {}
    ilceIsimleri = {}
    __veritabani = None
    __cache = ""
    __cacheKlasorYolu = "./bin/namaz_vakti/db/cache/"
    __miladiAylar = {
        1 : "Ocak",
        2 : "Şubat",
        3 : "Mart",
        4 : "Nisan",
        5 : "Mayıs",
        6 : "Haziran",
        7 : "Temmuz",
        8 : "Ağustos",
        9 : "Eylül",
        10: "Ekim",
        11: "Kasım",
        12: "Aralık"
    }
    __haftaninGunleri = {
        1 : "Pazartesi",
        2 : "Salı",
        3 : "Çarşamba",
        4 : "Perşembe",
        5 : "Cuma",
        6 : "Cumartesi",
        7 : "Pazar"
    }
    __hicriAylar = {
        1 : "Muharrem",
        2 : "Safer",
        3 : "Rebiü'l-Evvel",
        4 : "Rebiü'l-Ahir",
        5 : "Cemaziye'l-Evvel",
        6 : "Cemaziye'l-Ahir",
        7 : "Recep",
        8 : "Şaban",
        9 : "Ramazan",
        10: "Şevval",
        11: "Zi'l-ka'de",
        12: "Zi'l-Hicce"
    }
    # Başlatma metodu
    def __init__(self, cacheklasoru = None):
        # Dosya yolumuzu belirtelim
        dosyaYolu = os.path.join("./bin/namaz_vakti/db/")

        # Önce cache bellek işlemleri
        if cacheklasoru != None:
            self.__cache = cacheklasoru;
        else:
            self.__cache = os.path.join(dosyaYolu, self.__cacheKlasorYolu)

        # veritabanını oluştur!
        yerler = os.path.join(dosyaYolu,  "yerler.ndb")
        with open(yerler) as yer:
            self.__veritabani = json.load(yer)

    # cache klasörünü değiştirir
    def cacheKlasoru(self,cacheklasoru):
        self.__cache = cacheklasoru;
        return self

    # ülke isimlerini bir dict (sözlük) olarak döner! Sıralı dönmesini bekleme!
    def ulkeler(self):
        sonuc = { "durum" : "hata", "veri" : {}}
        ulkeListesi = {}

        for ulke in self.__veritabani:
            ulkeAdi = self.__veritabani[str(ulke)]["ulke_adi"]
            if ulkeAdi in self.ulkeIsimleri:
                ulkeAdi = self.ulkeIsimleri[ulkeAdi]
            ulkeListesi[int(ulke)] = ulkeAdi


        sonuc["durum"] = "basarili"
        sonuc["veri"] = ulkeListesi
        return sonuc

    # şehirleri döner. Eğer ülkenin şehirlerinin ilçesi varsa şehirleri döner yoksa ilçeleri döner!
    def sehirler(self, ulke_id):
        sonuc = { "durum" : "hata", "ilce": False, "veri" : {}}

        if str(ulke_id) in self.__veritabani:
            sonuc["durum"] = "basarili"

            ulke = self.__veritabani[str(ulke_id)]
            sehirListesi = {}
            if ulke["ilce_listesi_varmi"] == True:

                liste = []
                for i in ulke["sehirler"]:
                    liste.append(int(i))
                liste.sort()
                
                for sehir in liste:
                    sehirAdi = ulke["sehirler"][str(sehir)]["sehir_adi"]
                    if sehirAdi in self.sehirIsimleri:
                        sehirAdi = self.sehirIsimleri[sehirAdi]
                    sehirListesi[int(sehir)] = sehirAdi
            else:
                sonuc["ilce"] = True
                for sehir in ulke["sehirler"].values():
                    liste1 = []
                    for i in sehir["ilceler"]:
                        liste1.append(int(i))
                    liste1.sort()

                    for ilce in liste1:
                        sehirAdi = sehir["ilceler"][str(ilce)]
                        if sehirAdi in self.sehirIsimleri:
                            sehirAdi = self.sehirIsimleri[sehirAdi]
                        sehirListesi[ilce] = sehirAdi

        sonuc["veri"] = sehirListesi
        return sonuc

    # ilçeler listesini verir! Eğer ilçe listesi yoksa hata döndürür!
    def ilceler(self, ulke_id, sehir_id):
        sonuc = { "durum" : "hata", "veri" : {}}

        # ülke id geçerliyse!
        if str(ulke_id) in self.__veritabani:
            ulke = self.__veritabani[str(ulke_id)]

            # ilçeleri varsa dönelim!
            if ulke["ilce_listesi_varmi"] == True:
                # şehir id geçerliyse
                if str(sehir_id) in ulke["sehirler"]:
                    sonuc["durum"] = "basarili"
                    ilceListesi = {}
                    for ilce in ulke["sehirler"][str(sehir_id)]["ilceler"]:
                        ilceAdi = ulke["sehirler"][str(sehir_id)]["ilceler"][ilce]
                        if ilceAdi in self.ilceIsimleri:
                            ilceAdi = self.ilceIsimleri[ilceAdi]
                        ilceListesi[ilce] = ilceAdi
                    sonuc["veri"] = ilceListesi
        return sonuc

    # cache klasörünün içindeki dosyaları temizler
    def cacheTemizle(self):
        cache_dosyalari = os.listdir(self.__cache)
        for dosya in cache_dosyalari:
            if dosya.endswith(".ndb"):
                os.remove(os.path.join(self.__cache, dosya))

    # tek bir vakti verir!
    def vakit(self, sehir_id):

        sonuc = { "durum" : "hata", "veri" : {}}
        yer = self.__yerBilgisi(sehir_id)
        cacheDosyaAdi = "cache_" + str(yer["sehir_id"]) + ".ndb"
        cacheDosyasi = os.path.join(self.__cache, cacheDosyaAdi)
        bugun = datetime.strftime(datetime.now(), "%d.%m.%Y")

        # cache dosyası var mı ve okunabiliyor mu?
        if os.path.isfile(cacheDosyasi) and os.access(cacheDosyasi, os.R_OK):
            # cache dosyasıdan okuma işlemleri yapak!
            with open(cacheDosyasi) as v:
                jsonVeri = json.load(v)

            if bugun in jsonVeri["veri"]["vakitler"]:
                # bugün vakitlerin içinde var
                sonuc = jsonVeri
            else:
                # cache dosyası yok! o zaman sunucudan çek ver!
                veri = self.__sunucudanVeriCek(yer)
                # sonuç başarılıysa bilgileri doldur ver! değilse zaten hata olarak dönecek!
                if veri["durum"] == "basarili":
                    sonuc["durum"] = "basarili"
                    sonuc["veri"] = veri["veri"]
                    #cache belleğe ana işte burada yaz!
                    with open(os.path.join(cacheDosyasi), "w") as yaz:
                        json.dump(sonuc, yaz)
        else:
            # cache dosyası yok! o zaman sunucudan çek ver!
            veri = self.__sunucudanVeriCek(yer)
            # sonuç başarılıysa bilgileri doldur ver! değilse zaten hata olarak dönecek!
            if veri["durum"] == "basarili":
                sonuc["durum"] = "basarili"
                sonuc["veri"] = veri["veri"]
                try:
                    f = open("./bin/namaz_vakti/db/cache/"+"cache_" + str(yer["sehir_id"]) + ".ndb",'x',encoding='utf-8')
                    f.close()
                except FileExistsError as error:
                    error = None
                    pass
                with open("./bin/namaz_vakti/db/cache/"+"cache_" + str(yer["sehir_id"]) + ".ndb", 'wt', encoding='utf-8') as ver:
                    json.dump(sonuc,ver)
                # f.write(son_veri)
                # json.dump(son_veri)
                # f.close()
                # dosya = str(open(os.path.join("./bin/namaz_vakti/db/cache/"+cacheDosyaAdi)))
                # dosya_son = pathlib.Path(dosya).write_text(sonuc)
                # json.dump(sonuc,dosya_son)
                # with open(os.path.join(dosya), "wt") as yaz:
                #     json.dump(sonuc, yaz)

        if sonuc["durum"] == "basarili":
            sonuc["veri"]["vakit"] = sonuc["veri"]["vakitler"][bugun]
            del sonuc["veri"]["vakitler"]

        return sonuc

    # tüm vakitleri verir! bu cache bellekten okumaz ancak cache belleğe yazar!
    def vakitler(self, sehir_id):

        sonuc = { "durum" : "hata", "veri" : {}}
        yer = self.__yerBilgisi(sehir_id)
        cacheDosyaAdi = "cache_" + str(yer["sehir_id"]) + ".ndb"
        cacheDosyasi = os.path.join(self.__cache, cacheDosyaAdi)
        veri = self.__sunucudanVeriCek(yer)

        if veri["durum"] == "basarili":
            sonuc["durum"] = "basarili"
            sonuc["veri"] = veri["veri"]
            with open(os.path.join(cacheDosyasi), "w") as yaz:
                json.dump(sonuc, yaz)

        return sonuc

    # Yer ile ilgili bilinmesi gerekenleri verir!
    def __yerBilgisi(self, sehir_id):

        # adres dosyası
        adresDosyasi = os.path.join(os.path.join("./bin/namaz_vakti/"), "db", "adresler.ndb")
        with open(adresDosyasi) as adres:
            adresler = json.load(adres)

        veri = {}
        if str(sehir_id) in adresler:
            veri = (adresler[str(sehir_id)]).copy()

        adresler.clear()
        return veri

    # sunucudan çekilen bozuk tarihi düzeltir dd.mm.YYYY şeklinde döndürür!
    def __tarihDuzelt(self, bozukTarih):
        bozulanTarih = bozukTarih.split(" ")
        aylar = dict((v,k) for k, v in self.__miladiAylar.items())
        gun = bozulanTarih[0]
        ay = aylar[bozulanTarih[1]]
        if ay < 10:
            ay = "0" + str(ay)
        else:
            ay = str(ay)
        yil = bozulanTarih[2]
        return (gun + "." + ay + "." + yil)

    # tarih için verilen sayılarda 10 dan küçük olanlar için başına sıfır koyar stringe çevirir, yoksa sadece stringe çevirir!
    def __sifirla(self, sayi):
        if sayi < 10:
            return "0" + str(sayi)
        else:
            return str(sayi)


    # burada direk urlyi değil tüm veriyi al! böylelikle 2 kere uğraşmamış olursun!
    def __sunucudanVeriCek(self, yer):

        # geriye bunu döndürelim!
        sonuc = { "durum" : "hata", "veri" : {}}
        vakitler = {}
        # tam urlyi dolduralım
        fullURL = "http://namazvakitleri.diyanet.gov.tr" + yer["url"]
        # isteğimizi oluşturalım
        istek = requests.get(fullURL)
        # eğer isteğimiz bize sonuç döndürmüşse işleme devam edelim!
        if istek.status_code == 200:

            icerik = BeautifulSoup(istek.content, "html.parser")
            div = icerik.find( "div", {"id":"tab-1"} )
            tablo = div.find("tbody")

            for tr in tablo.find_all("tr"):      
                sira = 0
                simdikiSatir = ""

                for td in tr.find_all("td"):
                    elde = td.text          
                    if sira == 0:
                        tarih = self.__tarihDuzelt(elde)
                        tarihbol = tarih.split(".")
                        hicri_saf = islamic.from_gregorian(int(tarihbol[2]), int(tarihbol[1]), int(tarihbol[0]))
                        hicri = self.__sifirla(hicri_saf[2]) + "." + self.__sifirla(hicri_saf[1]) + "." + str(hicri_saf[0])
                        hicri_uzun = self.__sifirla(hicri_saf[2]) + " " + self.__hicriAylar[hicri_saf[1]] + " " + str(hicri_saf[0])

                        vakitler[tarih] = {
                            "tarih" : tarih,
                            "uzun_tarih" : elde,
                            "hicri" : hicri,
                            "hicri_uzun" : hicri_uzun,
                            "imsak" : "",
                            "gunes" : "",
                            "ogle" : "",
                            "ikindi" : "",
                            "aksam" : "",
                            "yatsi" : ""
                        }
                        simdikiSatir = tarih

                    if sira == 1:
                        vakitler[simdikiSatir]["imsak"] = elde
                    if sira == 2:
                        vakitler[simdikiSatir]["gunes"] = elde
                    if sira == 3:
                        vakitler[simdikiSatir]["ogle"] = elde
                    if sira == 4:
                        vakitler[simdikiSatir]["ikindi"] = elde
                    if sira == 5:
                        vakitler[simdikiSatir]["aksam"] = elde
                    if sira == 6:
                        vakitler[simdikiSatir]["yatsi"] = elde
                    sira += 1 # td for döngüsünün sonu
                sira = 0 # tr for döngüsünün sonu

            # burası if status_code == 200 ün içi
            sonuc["durum"] = "basarili"
            sonuc["veri"]["ulke"] = yer["ulke"]
            sonuc["veri"]["sehir"] = yer["sehir"]
            sonuc["veri"]["ilce"] = yer["ilce"]
            sonuc["veri"]["yer_adi"] = yer["uzun_adi"]
            sonuc["veri"]["vakitler"] = vakitler

        # sunucudan veri çek in içi!
        return sonuc