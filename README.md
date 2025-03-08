# Client Tracker

Client Tracker, müşteri, hizmet ve iş takibini kolaylaştıran bir web uygulamasıdır. Django framework'ü kullanılarak geliştirilmiştir.

## Özellikler

- Kullanıcı kimlik doğrulama sistemi
- Müşteri ve çalışan yönetimi
- Hizmet ve iş takibi
- Ödeme kayıtları
- Dinamik raporlama ve veri analizi

## Kurulum

### 1. Depoyu Kopyalayın

```sh
git clone https://github.com/serkancakmakk/client_tracker.git
cd client_tracker
```

### 2. Sanal Ortamı Oluşturun ve Aktif Edinu

```sh
python -m venv env
source env/bin/activate  # macOS/Linux
env\Scripts\activate  # Windows
```

### 3. Bağımlılıkları Yükleyin

```sh
pip install -r requirements.txt
```

### 4. Veritabanını Güncelleyin

```sh
python manage.py migrate
```

### 5. Süper Kullanıcı Oluşturun

```sh
python manage.py createsuperuser
```

### 6. Sunucuyu Çalıştırın

```sh
python manage.py runserver
```

## Kullanılan Teknolojiler

- **Backend:** Django, Django ORM
- **Frontend:** Bootstrap, JavaScript
- **Veritabanı:** SQLite
- **Kimlik Doğrulama:** Django Authentication

## API Kullanımı

JSON formatında veri almak için API uç noktaları mevcuttur. Örneğin:

```sh
GET /api/customers/
```

### Giriş Ekranı
![Proje Ekran Görüntüsü](client_tracker/assets/giriş_ekranı.png)
### Ana Ekran
![Proje Ekran Görüntüsü](client_tracker/assets/ana_ekran.png)
### Kullanıcı ve Servis Ekleme Ekranı
![Proje Ekran Görüntüsü](client_tracker/assets/çalışan_servis_ekleme.png)
### Giriş yapmış kullanıcıya ait işler ekranı
![Proje Ekran Görüntüsü](client_tracker/assets/baba_ait_işler.png)
### İş atama ekranı
![Proje Ekran Görüntüsü](client_tracker/assets/iş_atama.png)
### İş detay ekranı
![Proje Ekran Görüntüsü](client_tracker/assets/iş_detay.png)
### İş listesi ekranı
![Proje Ekran Görüntüsü](client_tracker/assets/iş_listesi.png)
### Müşteri detay ekranı
![Proje Ekran Görüntüsü](client_tracker/assets/müşteri_detay.png)
### Yapılan iş rapor ekranı
![Proje Ekran Görüntüsü](client_tracker/assets/yapılan_işler_raporu.png)


