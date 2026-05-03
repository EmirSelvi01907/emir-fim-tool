# 🛡️ Advanced FIM & Anti-Ransomware Tool
**Geliştirici:** Emir Selvi  

## 📝 Proje Hakkında
Bu araç, kritik dosyaların güvenliğini sağlamak amacıyla geliştirilmiş bir **Dosya Bütünlüğü İzleme (FIM)** ve **Davranışsal Analiz** sistemidir. Siber güvenlik araştırmalarım kapsamında geliştirdiğim bu yazılım, dosyada yapılan yetkisiz değişiklikleri saniyeler içinde saptar ve müdahale eder.

## 🛠️ Teknik Özellikler

### 1. Dinamik Hash Algoritması Seçimi
Sistem, kullanım amacına göre üç farklı kriptografik hash fonksiyonu sunar:
- **MD5:** Hızlı tarama gerektiren büyük dosyalar için optimize edilmiştir.
- **SHA-256:** Endüstri standardı, dengeli güvenlik ve hız.
- **SHA-512:** Maksimum güvenlik gerektiren kritik veri setleri için kullanılır.

### 2. Anti-Ransomware Katmanı (Davranışsal Analiz)
Yazılım, dosya üzerindeki değişikliklerin sıklığını takip eder. Eğer **10 saniye içinde 3'ten fazla** değişim saptanırsa, bu durum bir "Fidye Yazılımı" (Ransomware) saldırısı olarak değerlendirilir:
- **Otomatik Kurtarma:** Dosya anında `.yedek` dosyasından geri yüklenir.
- **Acil Durdurma:** Sistem güvenliği için izleme askıya alınır.
- **Kritik Alarm:** E-posta yoluyla yöneticiye anlık bildirim gönderilir.

### 3. Otomasyon ve Bildirim
- **SMTP Entegrasyonu:** Gmail üzerinden anlık güvenlik uyarıları.
- **Gelişmiş Dosya Gezgini:** Kullanıcı dostu terminal arayüzü ile sistem içinde dosya seçimi ve arama.
- **Detaylı Loglama:** `denetim_sistemi.log` üzerinden tüm geçmiş olayların takibi.

## 🚀 Kurulum

1. Repoyu klonlayın:
```bash
git clone https://github.com/EmirSelvi01907/emir-fim-tool.git
```

2. Gerekli Python kütüphanelerinin yüklü olduğundan emin olun (Standart kütüphaneler kullanılmıştır).

3. main.py içindeki SMTP ayarlarını kendi bilgilerinizle güncelleyin.

4. Programı çalıştırın:
```bash
python main.py
```

📜 Lisans
Bu proje eğitim ve araştırma amaçlıdır. İzinsiz ticari kullanımı önerilmez.# emir-fim-tool
