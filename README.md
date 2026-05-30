# 🎥 YouTube Comments Scraper - Destinasi Wisata Jawa Timur

Sistem web scraping untuk mengumpulkan komentar YouTube terkait destinasi wisata populer di Jawa Timur menggunakan **YouTube Data API v3** secara resmi dan gratis.

Dataset yang dihasilkan dapat digunakan untuk:

* Sentiment Analysis
* Aspect-Based Sentiment Analysis (ABSA)
* Opinion Mining
* Natural Language Processing (NLP)
* Analisis Kepuasan Wisatawan
* Penelitian Pariwisata Jawa Timur

---

## 📌 Fitur

* Menggunakan **YouTube Data API v3 (Official API)**
* Gratis dengan kuota **10.000 unit/hari**
* Mengambil komentar dari beberapa video untuk setiap destinasi wisata
* Mengambil jumlah likes pada komentar
* Menyimpan data ke format CSV
* Mendukung banyak destinasi wisata Jawa Timur
* Dapat digunakan untuk membangun dataset penelitian

---

## 🏞️ Destinasi Wisata yang Dikumpulkan

### Batu

* Jatim Park 1
* Jatim Park 2
* Jatim Park 3
* Batu Night Spectacular
* Museum Angkut
* Batu Secret Zoo

### Banyuwangi

* Kawah Ijen
* De Djawatan Forest

### Situbondo

* Taman Nasional Baluran

### Probolinggo

* Gunung Bromo
* Air Terjun Madakaripura

### Surabaya

* Tunjungan Plaza
* Taman Bungkul
* Monumen Kapal Selam
* Masjid Al-Akbar

### Pasuruan

* Taman Safari Prigen

### Lumajang

* Air Terjun Tumpak Sewu

---

## 📂 Struktur Dataset

Output file:

```text
wisata_jatim_youtube.csv
```

Kolom dataset:

| Kolom     | Keterangan                                     |
| --------- | ---------------------------------------------- |
| id        | UUID unik                                      |
| destinasi | Nama destinasi wisata                          |
| kategori  | Kategori wisata                                |
| kota      | Lokasi kota                                    |
| review    | Isi komentar YouTube                           |
| rating    | Kosong (YouTube tidak memiliki rating bintang) |
| tanggal   | Tanggal komentar                               |
| likes     | Jumlah likes komentar                          |
| platform  | Sumber data (YouTube)                          |

---

## ⚙️ Requirements

Install library yang dibutuhkan:

```bash
pip install google-api-python-client pandas
```

---

## 🔑 Mendapatkan API Key YouTube

YouTube Data API v3 dapat digunakan secara gratis melalui Google Cloud Platform.

### 1. Buka Google Cloud Console

https://console.cloud.google.com

### 2. Buat Project Baru

Klik:

```text
Select Project → New Project
```

### 3. Aktifkan YouTube Data API v3

Masuk ke:

```text
APIs & Services → Library
```

Cari:

```text
YouTube Data API v3
```

Kemudian klik:

```text
Enable
```

### 4. Buat API Key

Masuk ke:

```text
APIs & Services → Credentials
```

Klik:

```text
Create Credentials → API Key
```

### 5. Salin API Key

Masukkan ke bagian konfigurasi:

```python
API_KEY = "YOUR_API_KEY"
```

---

## 🚀 Cara Menjalankan

### 1. Clone Repository

```bash
git clone https://github.com/username/youtube-wisata-jatim-scraper.git
```

### 2. Masuk ke Folder Project

```bash
cd youtube-wisata-jatim-scraper
```

### 3. Install Dependencies

```bash
pip install google-api-python-client pandas
```

### 4. Isi API Key

Edit bagian:

```python
API_KEY = "YOUR_API_KEY"
```

### 5. Jalankan Program

```bash
python scrape_youtube_comments.py
```

---

## 📊 Konfigurasi

Parameter utama dapat diubah sesuai kebutuhan:

```python
MAX_VIDEO_PER_DESTINASI = 10
MAX_KOMENTAR_PER_VIDEO = 100
BAHASA = "id"
```

| Parameter               | Fungsi                                 |
| ----------------------- | -------------------------------------- |
| MAX_VIDEO_PER_DESTINASI | Jumlah video yang dicari per destinasi |
| MAX_KOMENTAR_PER_VIDEO  | Jumlah komentar yang diambil per video |
| BAHASA                  | Bahasa pencarian video                 |

---

## 📈 Estimasi Kuota API

YouTube Data API menyediakan:

```text
10.000 unit per hari
```

Biaya kuota:

| Operasi            | Kuota              |
| ------------------ | ------------------ |
| Search Video       | 100 unit           |
| Ambil Komentar     | 1 unit per halaman |
| Ambil 100 Komentar | ±1 unit            |

Contoh:

```text
17 destinasi
10 video per destinasi
100 komentar per video
```

Estimasi penggunaan:

```text
± 2.000 unit
```

Masih jauh di bawah batas harian.

---

## 📊 Contoh Output

```text
==================================================
✅ Total komentar : 12456
📄 File tersimpan : wisata_jatim_youtube.csv
==================================================

Jatim Park 1               856
Jatim Park 2               741
Gunung Bromo               934
Kawah Ijen                 687
Taman Safari Prigen        1021
```

---

## 🛠️ Teknologi yang Digunakan

* Python
* Pandas
* YouTube Data API v3
* Google Cloud Platform

---

## 🎯 Penggunaan Dataset

Dataset hasil scraping dapat digunakan untuk:

* Sentiment Analysis
* Aspect-Based Sentiment Analysis (ABSA)
* Text Classification
* Opinion Mining
* Topic Modeling
* Tourism Analytics
* Penelitian Pariwisata Jawa Timur

---

## 👩‍💻 Author

**Yuliani Purwitasari**

GitHub: https://github.com/ririsariii

---

## 📄 License

Project ini dibuat untuk tujuan penelitian, pembelajaran, dan pengembangan dataset akademik.

Data diperoleh melalui YouTube Data API v3 yang merupakan API resmi dari Google. Penggunaan data harus tetap mematuhi kebijakan dan Terms of Service YouTube.
