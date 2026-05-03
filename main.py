import hashlib
import os
import json
import time
import shutil
import platform
import getpass
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


logging.basicConfig(filename='denetim_sistemi.log', level=logging.INFO, 
                    format='%(asctime)s - %(message)s')


KIRMIZI = '\033[31m'; YESIL = '\033[32m'; SARI = '\033[33m'
MAVI = '\033[34m'; CYAN = '\033[36m'; NORMAL = '\033[0m'

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
GONDERICI_MAIL = "senin-mailin@gmail.com"
GONDERICI_SIFRE = "uygulama-sifren-buraya"

def emir_selvi_banner():
    banner = f"""{CYAN}
EEEEE M   M III RRRR         SSSS EEEEE L     V   V III 
E     MM MM  I  R   R       S     E     L     V   V  I  
EEEE  M M M  I  RRRR         SSS  EEEE  L     V   V  I  
E     M   M  I  R  R            S E     L      V V   I  
EEEEE M   M III R   R       SSSS  EEEEE LLLLL   V   III 
                                                        
         [+] EMIR SELVI - ADVANCED FIM & ANTI-RANSOMWARE
{NORMAL}"""
    print(banner)

def mail_gonder(alici_mail, dosya_yolu, cihaz, detay=""):
    try:
        msg = MIMEMultipart()
        msg['From'] = GONDERICI_MAIL
        msg['To'] = alici_mail
        msg['Subject'] = "🚨 KRİTİK GÜVENLİK ALARMI!"
        body = f"Dosya: {dosya_yolu}\nCihaz: {cihaz}\nDetay: {detay}\nZaman: {datetime.now()}"
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(GONDERICI_MAIL, GONDERICI_SIFRE)
        server.send_message(msg)
        server.quit()
        return True
    except: return False

def cihaz_bilgisi_al():
    return f"{getpass.getuser()}@{platform.node()}"

# --- ADIM 1: GELİŞMİŞ HASH FONKSİYONU ---
def dosya_bilgisi_al(dosya_yolu, algoritma="sha256"):
    if not os.path.exists(dosya_yolu): return None
    stat_info = os.stat(dosya_yolu)
    hash_obj = hashlib.new(algoritma)
    with open(dosya_yolu, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_obj.update(chunk)
    return {"hash": hash_obj.hexdigest(), "boyut": stat_info.st_size}

def log_kaydet(veritabani, veri):
    with open(veritabani, "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=4)

def dosya_ara(dosya_adi):
    baslangic_dizini = os.path.expanduser("~") 
    bulunanlar = []
    print(f"\n{SARI}[...] '{dosya_adi}' aranıyor...{NORMAL}")
    for kok, _, dosyalar in os.walk(baslangic_dizini):
        if dosya_adi in dosyalar:
            bulunanlar.append(os.path.join(kok, dosya_adi))
    return bulunanlar

def dosya_secici():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear'); emir_selvi_banner()
        print(f"{MAVI}1.{NORMAL} Dosya Gezgini")
        print(f"{MAVI}2.{NORMAL} İsimle Ara")
        print(f"{KIRMIZI}q.{NORMAL} Çıkış")
        secim = input(f"\n{CYAN}Seçim: {NORMAL}")
        if secim == '1':
            yol = os.path.expanduser("~")
            while True:
                os.system('cls' if os.name == 'nt' else 'clear'); emir_selvi_banner()
                print(f"{MAVI}Konum:{NORMAL} {yol}\n" + "-"*30)
                try:
                    icerik = os.listdir(yol)
                    print(f"0. [GERİ]")
                    for i, ad in enumerate(icerik, 1): print(f"{i}. {ad}")
                    s = input(f"\n{CYAN}Seçim: {NORMAL}")
                    if s == '0': yol = os.path.dirname(yol)
                    else:
                        yeni = os.path.join(yol, icerik[int(s)-1])
                        if os.path.isdir(yeni): yol = yeni
                        else: return yeni
                except: break
        elif secim == '2':
            aranan = input(f"\n{CYAN}Dosya adı: {NORMAL}")
            sonuclar = dosya_ara(aranan)
            if sonuclar:
                for i, y in enumerate(sonuclar, 1): print(f"{i}. {y}")
                return sonuclar[int(input(f"\n{CYAN}Seçim: {NORMAL}"))-1]
        elif secim.lower() == 'q': return None

# --- ANA PROGRAM ---
os.system('cls' if os.name == 'nt' else 'clear'); emir_selvi_banner()
print(f"{SARI}[*] Bildirimlerin gönderileceği e-posta adresini giriniz.{NORMAL}")
kullanici_email = input(f"{CYAN}E-posta: {NORMAL}")

# ADIM 1: ALGORİTMA SEÇİMİ
print(f"\n{SARI}Kullanılacak Hash Algoritmasını Seçin:{NORMAL}")
print("1. SHA-256 (Standart)\n2. MD5 (Hızlı)\n3. SHA-512 (Yüksek Güvenlik)")
algo_sec = input(f"{CYAN}Seçim (1-3): {NORMAL}")
algo = {"1": "sha256", "2": "md5", "3": "sha512"}.get(algo_sec, "sha256")

izleme_listesi = {} 

while True:
    secilen_dosya = dosya_secici()
    if not secilen_dosya: break

    veritabani = "denetim_kayitlari.json"
    yedek_dosya = secilen_dosya + ".yedek"
    cihaz = cihaz_bilgisi_al()
    
    bilgi = dosya_bilgisi_al(secilen_dosya, algo)
    shutil.copy2(secilen_dosya, yedek_dosya)
    
    izleme_listesi[secilen_dosya] = {
        "yol": secilen_dosya,
        "eski_hash": bilgi["hash"],
        "eski_boyut": bilgi["boyut"],
        "yedek": yedek_dosya,
        "degisiklik_sayaci": 0,           # ADIM 4 için sayaç
        "son_degisiklik": time.time()    # ADIM 4 için zaman takibi
    }

    veri = {
        "dosya_bilgisi": {"cihaz": cihaz, "alici": kullanici_email, "algo": algo},
        "islem_gecmisi": [{"zaman": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "olay": f"İzleme Başlatıldı ({algo})"}]
    }
    log_kaydet(veritabani, veri)

    os.system('cls' if os.name == 'nt' else 'clear'); emir_selvi_banner()
    print(f"{MAVI}[!] İZLEME AKTİF ({algo.upper()}):{NORMAL} {secilen_dosya}")
    
    try:
        while True:
            mevcut_bilgi = dosya_bilgisi_al(secilen_dosya, algo)
            su_an_ts = time.time()
            su_an_str = datetime.now().strftime("%H:%M:%S")

            if mevcut_bilgi["hash"] != izleme_listesi[secilen_dosya]["eski_hash"]:
                # --- ADIM 4: RANSOMWARE ANALİZİ ---
                gecen_sure = su_an_ts - izleme_listesi[secilen_dosya]["son_degisiklik"]
                izleme_listesi[secilen_dosya]["degisiklik_sayaci"] += 1
                
                # 10 saniye içinde 3'ten fazla değişim varsa alarm ver
                if izleme_listesi[secilen_dosya]["degisiklik_sayaci"] > 3 and gecen_sure < 10:
                    alert_msg = "!!! KRİTİK: HIZLI DEĞİŞİKLİK TESPİT EDİLDİ! SALDIRI OLABİLİR !!!"
                    print(f"\n{KIRMIZI}{alert_msg}{NORMAL}")
                    mail_gonder(kullanici_email, secilen_dosya, cihaz, alert_msg)
                    shutil.copy2(yedek_dosya, secilen_dosya) # Otomatik kurtar
                    print(f"{YESIL}[+] Güvenlik için otomatik restore edildi.{NORMAL}")
                    time.sleep(5)
                    break

                detay = f"Değişim ({algo}): Boyut {izleme_listesi[secilen_dosya]['eski_boyut']} -> {mevcut_bilgi['boyut']}"
                print(f"\n{KIRMIZI}[ALARM] DEĞİŞİKLİK TESPİT EDİLDİ! ({su_an_str}){NORMAL}")
                
                if mail_gonder(kullanici_email, secilen_dosya, cihaz, detay):
                    print(f"{YESIL}[+] Uyarı maili gönderildi.{NORMAL}")
                
                karar = input(f"{SARI}Yedekten geri yüklensin mi? (e/h): {NORMAL}").lower()
                
                if karar == 'e':
                    shutil.copy2(yedek_dosya, secilen_dosya)
                    yeni_durum = dosya_bilgisi_al(secilen_dosya, algo)
                    izleme_listesi[secilen_dosya]["eski_hash"] = yeni_durum["hash"]
                    olay = "Yedekten geri yüklendi."
                else:
                    izleme_listesi[secilen_dosya]["eski_hash"] = mevcut_bilgi["hash"]
                    izleme_listesi[secilen_dosya]["eski_boyut"] = mevcut_bilgi["boyut"]
                    olay = "Değişiklik onaylandı."
                
                izleme_listesi[secilen_dosya]["son_degisiklik"] = su_an_ts
                veri["islem_gecmisi"].append({"zaman": su_an_str, "olay": olay})
                log_kaydet(veritabani, veri)

            print(f"[{su_an_str}] {YESIL}DURUM: GÜVENLİ | {NORMAL}{secilen_dosya}", end="\r")
            time.sleep(1.5)

    except KeyboardInterrupt:
        if input(f"\n\n{SARI}Başka dosya bakacak mısın? (e/h): {NORMAL}").lower() != 'e':
            break