# Analisis Sentimen: Kebijakan WFH ASN Hari Jumat

Proyek untuk mengambil (scraping) dan menganalisis sentimen publik di X (Twitter)
terhadap kebijakan *Work From Home* (WFH) ASN pada hari Jumat.

## Isi Repositori

| File | Keterangan |
|------|-----------|
| `scrape_wfh_asn_colab.ipynb` | **Notebook Google Colab** siap pakai — scraping historis tanpa API (snscrape) + analisis sentimen IndoBERT. |
| `scrape_snscrape.py` | Script scraping data historis tanpa API (untuk dijalankan di komputer lokal). |
| `scrape_x.py` | Script scraping via X API v2 resmi (butuh Bearer Token). |
| `analyze_sentiment.py` | Script analisis sentimen (positif/netral/negatif) memakai model IndoBERT. |

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
