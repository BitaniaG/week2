import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm
import numpy as np
import re
from scipy.sparse import vstack    # FIXED: correct way to stack sparse vectors

print("Loading cleaned review data...")
df = pd.read_csv("data/processed/reviews_with_sentiment.csv")

# -----------------------------
# 1. Preprocessing
# -----------------------------
def clean_text(text):
    if pd.isna(text):
        return ""
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    return text

df["clean_text"] = df["review_text"].astype(str).apply(clean_text)

# -----------------------------
# 2. TF-IDF Keyword Extraction
# -----------------------------
print("Extracting keywords using TF-IDF...")

vectorizer = TfidfVectorizer(stop_words="english", max_features=500)
tfidf_matrix = vectorizer.fit_transform(df["clean_text"])
feature_names = vectorizer.get_feature_names_out()

# -----------------------------
# 3. Define Themes & Keywords
# -----------------------------
themes = {
    "Login / Account Issues": ["login", "password", "otp", "account", "verification", "credentials"],
    "Performance Issues": ["slow", "crash", "freeze", "loading", "lag", "error"],
    "Transaction Problems": ["transfer", "payment", "balance", "deposit", "withdrawal", "fail"],
    "UI / UX Experience": ["design", "interface", "navigation", "feature", "layout"],
    "Customer Support": ["help", "support", "service", "response", "call"],
    "Positive Feedback": ["good", "great", "excellent", "love", "helpful", "easy"],
}

theme_keywords = list(themes.keys())
theme_vectors = []

# Create TF-IDF vector for each theme definition
for theme, words in themes.items():
    fake_sentence = " ".join(words)
    vec = vectorizer.transform([fake_sentence])
    theme_vectors.append(vec)

# FIXED: stack sparse matrices correctly
theme_vectors = vstack(theme_vectors)

# -----------------------------
# 4. Assign Theme per Review
# -----------------------------
print("Assigning themes to reviews...")

assigned_themes = []

for i in tqdm(range(len(df)), desc="Processing themes"):
    review_vec = tfidf_matrix[i]
    similarities = cosine_similarity(review_vec, theme_vectors).flatten()
    best_theme = theme_keywords[np.argmax(similarities)]
    assigned_themes.append(best_theme)

df["theme"] = assigned_themes

# -----------------------------
# 5. Save Output
# -----------------------------
output_path = "data/processed/reviews_with_themes.csv"
df.to_csv(output_path, index=False)

print("\n===================================")
print("THEME EXTRACTION COMPLETE!")
print(f"Saved to: {output_path}")
print("===================================")
