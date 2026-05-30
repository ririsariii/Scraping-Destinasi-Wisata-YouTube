"""
Scraper Komentar YouTube - Destinasi Wisata Jawa Timur
Menggunakan YouTube Data API v3 (GRATIS, resmi)
Output: wisata_jatim_youtube.csv

Kolom: id, destinasi, kategori, kota, review, rating, tanggal, likes, platform

Cara dapat API Key (GRATIS):
    1. Buka https://console.cloud.google.com
    2. Buat project baru
    3. Cari & aktifkan "YouTube Data API v3"
    4. Credentials → Create Credentials → API Key
    5. Isi API_KEY di bawah

Kuota gratis: 10.000 unit/hari
    - Search video     = 100 unit
    - Ambil komentar   = 1 unit per halaman (100 komentar)
    - Estimasi: ~500 komentar per destinasi = ~10 unit
    
Requirements:
    pip install google-api-python-client pandas
"""

import uuid
import pandas as pd
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# ============================================================
# KONFIGURASI
# ============================================================
API_KEY = "AIzaSyAJ6H9OoW5_d6ojuqpxx1XqYCoIYNI871E"

# Jumlah video per destinasi yang akan diambil komentarnya
MAX_VIDEO_PER_DESTINASI = 10

# Jumlah komentar per video (maks 100 per request, bisa multi-page)
MAX_KOMENTAR_PER_VIDEO = 100

# Bahasa pencarian video (id = Indonesia)
BAHASA = "id"

# ============================================================
# DATA DESTINASI 
# ============================================================
DESTINASI = [
    ("Jatim Park 1",               "Wisata Hiburan",        "Batu"),
    ("Jatim Park 2",               "Wisata Hiburan",        "Batu"),
    ("Jatim Park 3",               "Wisata Hiburan",        "Batu"),
    ("Batu Night Spectacular",     "Wisata Hiburan",        "Batu"),
    ("Museum Angkut Batu",         "Wisata Budaya/Edukasi", "Batu"),
    ("Batu Secret Zoo",            "Wisata Alam/Hiburan",   "Batu"),
    ("Kawah Ijen",                 "Wisata Alam",           "Banyuwangi"),
    ("De Djawatan Forest",         "Wisata Alam",           "Banyuwangi"),
    ("Taman Nasional Baluran",     "Wisata Alam",           "Situbondo"),
    ("Gunung Bromo",               "Wisata Alam",           "Probolinggo"),
    ("Air Terjun Madakaripura",    "Wisata Alam",           "Probolinggo"),
    ("Tunjungan Plaza Surabaya",   "Wisata Belanja",        "Surabaya"),
    ("Taman Bungkul Surabaya",     "Taman Kota",            "Surabaya"),
    ("Monumen Kapal Selam",        "Wisata Sejarah",        "Surabaya"),
    ("Masjid Al-Akbar Surabaya",   "Wisata Religi",         "Surabaya"),
    ("Taman Safari Prigen",        "Wisata Alam/Hiburan",   "Pasuruan"),
    ("Air Terjun Tumpak Sewu",     "Wisata Alam",           "Lumajang"),
]

# ============================================================
# INISIALISASI API
# ============================================================
def buat_youtube_client():
    return build("youtube", "v3", developerKey=API_KEY)


# ============================================================
# CARI VIDEO YOUTUBE
# ============================================================
def cari_video(youtube, query: str, max_results: int) -> list:
    """
    Cari video YouTube berdasarkan query destinasi.
    Return list of video_id.
    """
    try:
        response = youtube.search().list(
            q=f"{query} wisata review vlog",
            part="id,snippet",
            type="video",
            maxResults=max_results,
            relevanceLanguage=BAHASA,
            videoCaption="any",
            order="relevance",
        ).execute()

        video_ids = []
        for item in response.get("items", []):
            vid_id = item["id"].get("videoId")
            judul  = item["snippet"].get("title", "")
            if vid_id:
                video_ids.append((vid_id, judul))
                print(f"    Video: {judul[:60]}")

        return video_ids

    except HttpError as e:
        print(f"    ✗ Error cari video: {e}")
        return []


# ============================================================
# AMBIL KOMENTAR VIDEO
# ============================================================
def ambil_komentar(youtube, video_id: str, max_komentar: int) -> list:
    """
    Ambil komentar dari satu video.
    Return list of dict {teks, tanggal, likes}.
    """
    komentar = []
    next_page_token = None

    try:
        while len(komentar) < max_komentar:
            sisa = max_komentar - len(komentar)
            per_page = min(100, sisa)

            response = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=per_page,
                order="relevance",  # komentar paling relevan dulu
                pageToken=next_page_token,
                textFormat="plainText",
            ).execute()

            for item in response.get("items", []):
                top = item["snippet"]["topLevelComment"]["snippet"]
                komentar.append({
                    "teks":    top.get("textDisplay", "").strip(),
                    "tanggal": top.get("publishedAt", "")[:10],  # YYYY-MM-DD
                    "likes":   top.get("likeCount", 0),
                })

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

    except HttpError as e:
        err_str = str(e)
        if "commentsDisabled" in err_str or "disabled comments" in err_str.lower():
            print(f"      ⚠ Komentar dinonaktifkan di video ini")
        else:
            print(f"      ✗ Error ambil komentar: {e}")

    return komentar


# ============================================================
# PROSES SATU DESTINASI
# ============================================================
def proses_destinasi(youtube, nama: str, kategori: str, kota: str) -> list:
    rows = []

    # Query pencarian lebih spesifik
    query = f"{nama} Jawa Timur"
    print(f"  Mencari video: '{query} wisata review vlog'")

    video_list = cari_video(youtube, query, MAX_VIDEO_PER_DESTINASI)
    if not video_list:
        print(f"  ✗ Tidak ada video ditemukan")
        return rows

    for video_id, judul_video in video_list:
        print(f"  → Ambil komentar: {judul_video[:50]}...")
        komentar_list = ambil_komentar(youtube, video_id, MAX_KOMENTAR_PER_VIDEO)

        for km in komentar_list:
            if not km["teks"]:  # skip komentar kosong
                continue
            rows.append({
                "id":        str(uuid.uuid4()),
                "destinasi": nama,
                "kategori":  kategori,
                "kota":      kota,
                "review":    km["teks"],
                "rating":    "",          # YouTube tidak punya rating bintang
                "tanggal":   km["tanggal"],
                "likes":     km["likes"],
                "platform":  "YouTube",
            })

        print(f"      ✓ {len(komentar_list)} komentar diambil")

    return rows


# ============================================================
# MAIN LOOP
# ============================================================
def scrape_semua() -> pd.DataFrame:
    youtube = buat_youtube_client()
    semua = []
    total = len(DESTINASI)

    for idx, (nama, kategori, kota) in enumerate(DESTINASI, start=1):
        print(f"\n[{idx}/{total}] {nama} — {kota}")
        rows = proses_destinasi(youtube, nama, kategori, kota)
        semua.extend(rows)
        print(f"  ✓ Total komentar destinasi ini: {len(rows)} | Akumulasi: {len(semua)}")

    return pd.DataFrame(semua, columns=[
        "id", "destinasi", "kategori", "kota",
        "review", "rating", "tanggal", "likes", "platform"
    ])


if __name__ == "__main__":
    if API_KEY == "ISI_API_KEY_YOUTUBE_KAMU":
        print("❌ Isi dulu API_KEY di bagian KONFIGURASI!")
        exit(1)

    print("=" * 60)
    print("  Scraper YouTube Comments — Wisata Jawa Timur")
    print(f"  {MAX_VIDEO_PER_DESTINASI} video × {MAX_KOMENTAR_PER_VIDEO} komentar/video")
    print("=" * 60)

    df = scrape_semua()

    if df.empty:
        print("\n⚠ Tidak ada data terkumpul.")
    else:
        out = "wisata_jatim_youtube.csv"
        df.to_csv(out, index=False, encoding="utf-8-sig")

        print("\n" + "=" * 60)
        print(f"✅ Total komentar : {len(df)}")
        print(f"📄 File tersimpan : {out}")
        print("=" * 60)
        print("\nRingkasan per destinasi:")
        print(
            df.groupby(["destinasi", "kota"])["id"]
            .count()
            .rename("jumlah_komentar")
            .to_string()
        )

        # Estimasi kuota yang dipakai
        kuota_search  = len(DESTINASI) * 100
        kuota_comment = len(df) // 100 + len(DESTINASI) * MAX_VIDEO_PER_DESTINASI
        print(f"\nEstimasi kuota terpakai: ~{kuota_search + kuota_comment} unit")
        print(f"Sisa kuota hari ini   : ~{10000 - kuota_search - kuota_comment} unit")