"""
Analisis sentimen tweet bahasa Indonesia tentang kebijakan WFH ASN hari Jumat.

Membaca hasil scraping (tweets_wfh_asn.csv), melakukan pembersihan teks,
lalu mengklasifikasikan sentimen tiap tweet menjadi: positif / netral / negatif
menggunakan model IndoBERT pretrained.

Persiapan:
    pip install transformers torch pandas matplotlib

Jalankan:
    python analyze_sentiment.py
"""

import re
import pandas as pd
import matplotlib.pyplot as plt
from transformers import pipeline

INPUT_FILE = "tweets_wfh_asn.csv"
OUTPUT_FILE = "tweets_wfh_asn_sentimen.csv"

# Model IndoBERT yang sudah di-fine-tune untuk sentimen 3 kelas.
MODEL_NAME = "mdhugol/indonesia-bert-sentiment-classification"

# Model ini mengembalikan label LABEL_0/1/2, kita petakan ke kata yang jelas.
LABEL_MAP = {
    "LABEL_0": "positif",
    "LABEL_1": "netral",
    "LABEL_2": "negatif",
}


def bersihkan_teks(teks: str) -> str:
    """Hapus URL, mention, hashtag-symbol, dan spasi berlebih."""
    teks = re.sub(r"http\S+|www\.\S+", "", teks)   # buang URL
    teks = re.sub(r"@\w+", "", teks)                # buang mention
    teks = re.sub(r"#", "", teks)                   # buang simbol hashtag (teks tetap)
    teks = re.sub(r"\s+", " ", teks)                # rapikan spasi
    return teks.strip()


def main():
    df = pd.read_csv(INPUT_FILE)
    if df.empty:
        raise SystemExit("File kosong, jalankan scrape_x.py dulu untuk mengambil data.")

    df["clean_text"] = df["text"].astype(str).apply(bersihkan_teks)
    df = df[df["clean_text"].str.len() > 3].reset_index(drop=True)

    print(f"Menganalisis {len(df)} tweet ...")

    classifier = pipeline(
        "sentiment-analysis",
        model=MODEL_NAME,
        truncation=True,
        max_length=256,
    )

    hasil = classifier(df["clean_text"].tolist())
    df["sentimen"] = [LABEL_MAP.get(r["label"], r["label"]) for r in hasil]
    df["skor"] = [round(r["score"], 3) for r in hasil]

    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
    print(f"Hasil tersimpan di '{OUTPUT_FILE}'\n")

    # Ringkasan distribusi sentimen
    ringkasan = df["sentimen"].value_counts()
    persen = (ringkasan / ringkasan.sum() * 100).round(1)
    print("=== Ringkasan Sentimen ===")
    for label in ["positif", "netral", "negatif"]:
        jumlah = ringkasan.get(label, 0)
        print(f"{label:8s}: {jumlah:4d} tweet ({persen.get(label, 0)}%)")

    # Visualisasi sederhana
    ringkasan.reindex(["positif", "netral", "negatif"]).plot(
        kind="bar", color=["#2ecc71", "#95a5a6", "#e74c3c"]
    )
    plt.title("Sentimen Publik: Kebijakan WFH ASN Hari Jumat")
    plt.ylabel("Jumlah Tweet")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig("sentimen_wfh_asn.png", dpi=120)
    print("\nGrafik tersimpan di 'sentimen_wfh_asn.png'")


if __name__ == "__main__":
    main()
