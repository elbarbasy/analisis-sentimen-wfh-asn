# Analisis Sentimen: Kebijakan WFH ASN Hari Jumat

Proyek untuk mengambil (scraping) dan menganalisis sentimen publik di X (Twitter)
terhadap kebijakan *Work From Home* (WFH) ASN pada hari Jumat.

## Isi Repositori

| File | Keterangan |
|------|-----------|
| `scrape_wfh_asn_harvest_colab.ipynb` | **Notebook Colab (REKOMENDASI)** — crawling historis >2000 tweet via `tweet-harvest` (pakai `auth_token`, tanpa API developer). |
| `scrape_wfh_asn_api_colab.ipynb` | Notebook Colab versi **API resmi X** (tweepy + Bearer Token). |
| `scrape_wfh_asn_colab.ipynb` | Notebook Colab versi **snscrape** (tanpa API, sering diblokir di Colab). |
| `scrape_snscrape.py` | Script scraping historis tanpa API (untuk dijalankan di komputer lokal). |
| `scrape_x.py` | Script scraping via X API v2 resmi (butuh Bearer Token). |
| `analyze_sentiment.py` | Script analisis sentimen (positif/netral/negatif) memakai model IndoBERT. |

## Perbandingan Metode Scraping

| Metode | API/Token | Historis | Volume besar | Stabil di Colab | Sesuai ToS |
|--------|-----------|----------|--------------|-----------------|------------|
| tweet-harvest | `auth_token` (cookie login) | ✅ | ✅ >2000 | ✅ | ⚠️ Tidak |
| API resmi (tweepy) | Bearer Token (developer) | ❌ 7 hari | ❌ (gratis) | ✅ | ✅ Ya |
| snscrape | Tidak perlu | ✅ | ✅ | ⚠️ Sering diblokir | ⚠️ Tidak |

## Cara Cepat (Google Colab)

1. Buka [Google Colab](https://colab.research.google.com).
2. **File → Open notebook → tab GitHub**, lalu cari repositori ini, atau **Upload** file `scrape_wfh_asn_colab.ipynb`.
3. Jalankan tiap sel berurutan dari atas ke bawah.

## Cara Lokal

```bash
pip install -r requirements.txt

# Opsi A: scraping historis tanpa API
python scrape_snscrape.py

# Opsi B: scraping via API resmi (butuh file .env berisi X_BEARER_TOKEN)
python scrape_x.py

# Analisis sentimen pada CSV hasil scraping
python analyze_sentiment.py
```

## Catatan

- **snscrape** tidak butuh API key & bisa ambil data historis, tetapi sejak X mewajibkan login, kadang diblokir (khususnya dari IP datacenter seperti Google Colab). Jika gagal, coba ulang, persempit rentang tanggal, atau jalankan dari koneksi lokal.
- **X API resmi** stabil & legal, namun tier gratis sangat terbatas (butuh tier berbayar untuk volume besar).
- Scraping langsung tunduk pada Ketentuan Layanan (ToS) X — gunakan secara wajar dan bertanggung jawab.
