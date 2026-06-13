"""
Ambil data HISTORIS dari X (Twitter) TANPA API resmi, menggunakan snscrape.

Topik: kebijakan WFH ASN hari Jumat (untuk analisis sentimen).

CATATAN PENTING:
- snscrape TIDAK butuh API key, dan bisa ambil data historis (lintas tahun).
- TAPI sejak X mewajibkan login, snscrape sering tidak stabil / berhenti jalan.
  Kalau script ini error "blocked"/"4 requests failed", berarti X sedang
  memblokir akses tanpa login -> coba lagi nanti, atau pakai jalur lain
  (lihat dataset publik di README jawaban).
- Scraping langsung melanggar ToS X. Gunakan dengan bijak & jumlah wajar.

Install (versi dev dari GitHub lebih update daripada versi PyPI):
    pip install git+https://github.com/JustAnotherArchivist/snscrape.git

Jalankan:
    python scrape_snscrape.py
"""

import csv
import itertools

try:
    import snscrape.modules.twitter as sntwitter
except ImportError:
    raise SystemExit(
        "snscrape belum terpasang.\n"
        "Install dengan:\n"
        "  pip install git+https://github.com/JustAnotherArchivist/snscrape.git"
    )

# ---------------------------------------------------------------------------
# Konfigurasi
# ---------------------------------------------------------------------------
MAX_TWEETS = 2000
OUTPUT_FILE = "tweets_wfh_asn_historis.csv"

# Operator pencarian (sama seperti pencarian lanjutan di web X):
#   since:YYYY-MM-DD  until:YYYY-MM-DD  -> rentang tanggal historis
#   lang:id                            -> hanya bahasa Indonesia
#   -filter:retweets                   -> buang retweet
QUERY = (
    '("WFH ASN" OR "WFH PNS" OR "ASN WFH" OR "kerja dari rumah ASN" '
    'OR (ASN Jumat WFH) OR (PNS Jumat "work from home")) '
    'lang:id since:2024-01-01 until:2025-12-31 -filter:retweets'
)


def main():
    print("Mulai mengambil data historis via snscrape ...")
    print(f"Query: {QUERY}\n")

    collected = 0
    scraper = sntwitter.TwitterSearchScraper(QUERY)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["id", "created_at", "username", "likes", "retweets", "replies", "text"]
        )

        try:
            for tweet in itertools.islice(scraper.get_items(), MAX_TWEETS):
                writer.writerow(
                    [
                        tweet.id,
                        tweet.date,
                        tweet.user.username,
                        tweet.likeCount,
                        tweet.retweetCount,
                        tweet.replyCount,
                        tweet.rawContent.replace("\n", " "),
                    ]
                )
                collected += 1
                if collected % 100 == 0:
                    f.flush()
                    print(f"  ... {collected}/{MAX_TWEETS} tweet terkumpul")
        except Exception as e:
            print(f"\n[!] Berhenti karena error: {e}")
            print("    Kemungkinan X memblokir akses tanpa login.")
            print(f"    {collected} tweet yang sudah terambil tetap tersimpan.")

    print(f"\nSelesai. {collected} tweet tersimpan di '{OUTPUT_FILE}'")
    if collected == 0:
        print("\n[!] 0 tweet terambil -> snscrape kemungkinan sedang diblokir X.")
        print("    Coba jalur dataset publik (lihat penjelasan di chat).")


if __name__ == "__main__":
    main()
