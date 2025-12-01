import psycopg2
import pandas as pd

# -----------------------------
# Load processed CSV
# -----------------------------
df = pd.read_csv("data/processed/reviews_processed.csv")

# -----------------------------
# Database connection
# -----------------------------
conn = psycopg2.connect(
    host="localhost",
    dbname="bank_reviews",
    user="postgres",
    password="MyNewPass123"   # <-- CHANGE THIS
)

cur = conn.cursor()

# -----------------------------
# Mapping bank names to IDs (case-insensitive)
# -----------------------------
bank_map = {
    "commercial bank of ethiopia": 1,
    "abyssinia bank": 2,
    "dashen bank": 3
}

# -----------------------------
# Insert each review
# -----------------------------
for _, row in df.iterrows():
    bank_name_clean = row["bank_name"].strip().lower()  # make lowercase & remove extra spaces
    bank_id = bank_map.get(bank_name_clean)

    if bank_id is None:
        print(f"Warning: Bank name not found in map: '{row['bank_name']}'")
        continue

    cur.execute("""
        INSERT INTO reviews 
        (bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, source)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        bank_id,
        row["review_text"],
        int(row["rating"]),
        row["review_date"],
        None,          # sentiment_label not in CSV
        None,          # sentiment_score not in CSV
        row["source"]
    ))

# -----------------------------
# Commit and close connection
# -----------------------------
conn.commit()
cur.close()
conn.close()

print("✅ Inserted all reviews into PostgreSQL successfully!")
