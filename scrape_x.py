"""
Script untuk mengambil data dari X (Twitter) menggunakan X API v2 resmi via Tweepy.

Persiapan:
1. Daftar developer account di https://developer.x.com/
2. Buat sebuah Project + App, lalu ambil "Bearer Token"
3. Install dependency:  pip install tweepy python-dotenv
4. Buat file .env berisi:  X_BEARER_TOKEN=isi_token_kamu_disini
5. Jalankan:  python scrape_x.py
"""

import os
import csv
import time
from datetime import datetime

import tweepy
from dotenv import load_dotenv

load_dotenv()

BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")
if not BEARER_TOKEN:
    raise SystemExit("X_BEARER_TOKEN belum diset. Buat file .env dulu ya.")

# Inisialisasi client. wait_on_rate_limit=True membuat script otomatis
# menunggu jika kuota rate limit habis (tidak langsung error).
client = tweepy.Client(bearer_token=BEARER_TOKEN, wait_on_rate_limit=True)


def search_tweets(query: str, max_results: int = 2000, output_file: str = "tweets.csv"):
    """
    Cari tweet terbaru berdasarkan query lalu simpan ke CSV.

    query        : kata kunci pencarian, contoh: "gempa lang:id -is:retweet"
    max_results  : total tweet yang ingin diambil (akan dipaginasi otomatis)
    output_file  : nama file CSV hasil

    Catatan: data ditulis baris-per-baris (incremental) dan di-flush berkala,
    jadi kalau script terhenti di tengah jalan, data yang sudah terambil aman.
    """
    tweet_fields = ["created_at", "author_id", "public_metrics", "lang"]
    collected = 0
    start_time = time.time()

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["id", "created_at", "author_id", "lang", "likes", "retweets", "replies", "text"]
        )

        # Paginator menangani perpindahan halaman secara otomatis.
        paginator = tweepy.Paginator(
            client.search_recent_tweets,
            query=query,
            tweet_fields=tweet_fields,
            max_results=100,  # maksimal 100 per request untuk endpoint ini
        )

        try:
            for tweet in paginator.flatten(limit=max_results):
                metrics = tweet.public_metrics or {}
                writer.writerow(
                    [
                        tweet.id,
                        tweet.created_at,
                        tweet.author_id,
                        tweet.lang,
                        metrics.get("like_count", 0),
                        metrics.get("retweet_count", 0),
                        metrics.get("reply_count", 0),
                        tweet.text.replace("\n", " "),
                    ]
                )
                collected += 1

                # Tampilkan progress & simpan ke disk tiap 100 tweet.
                if collected % 100 == 0:
                    f.flush()
                    elapsed = int(time.time() - start_time)
                    print(f"  ... {collected}/{max_results} tweet terkumpul ({elapsed}s)")
        except KeyboardInterrupt:
            print("\nDihentikan manual. Data yang sudah terkumpul tetap tersimpan.")

    print(f"Selesai. {collected} tweet tersimpan di '{output_file}'")


def get_user_tweets(username: str, max_results: int = 100, output_file: str = "user_tweets.csv"):
    """Ambil tweet terbaru dari satu akun tertentu (tanpa tanda @)."""
    user = client.get_user(username=username)
    if user.data is None:
        raise SystemExit(f"User '{username}' tidak ditemukan.")

    user_id = user.data.id
    collected = 0

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "created_at", "likes", "retweets", "text"])

        paginator = tweepy.Paginator(
            client.get_users_tweets,
            id=user_id,
            tweet_fields=["created_at", "public_metrics"],
            exclude=["retweets", "replies"],
            max_results=100,
        )

        for tweet in paginator.flatten(limit=max_results):
            metrics = tweet.public_metrics or {}
            writer.writerow(
                [
                    tweet.id,
                    tweet.created_at,
                    metrics.get("like_count", 0),
                    metrics.get("retweet_count", 0),
                    tweet.text.replace("\n", " "),
                ]
            )
            collected += 1

    print(f"Selesai. {collected} tweet dari @{username} tersimpan di '{output_file}'")


if __name__ == "__main__":
    # Query khusus topik: kebijakan WFH ASN hari Jumat.
    # Beberapa variasi istilah digabung dengan OR agar cakupannya luas.
    # lang:id   -> hanya bahasa Indonesia
    # -is:retweet -> buang retweet agar opini tidak terduplikasi
    topik_query = (
        '("WFH ASN" OR "WFH PNS" OR "ASN WFH" OR "work from home ASN" '
        'OR ("ASN" "Jumat" "WFH") OR ("ASN" "kerja dari rumah")) '
        'lang:id -is:retweet'
    )

    search_tweets(query=topik_query, max_results=2000, output_file="tweets_wfh_asn.csv")
