from transformers import pipeline
import pandas as pd
from tqdm import tqdm

# Load CSV to check columns
df = pd.read_csv("data/processed/reviews_processed.csv")
print("Columns in CSV:", df.columns)

print("Loading data...")
df = pd.read_csv("data/processed/reviews_processed.csv")

print("Loading sentiment model...")
sentiment = pipeline("sentiment-analysis")

labels = []
scores = []

print("Running sentiment analysis...")
for text in tqdm(df['review_text'], desc="Processing"):
    result = sentiment(text[:512])[0]
    labels.append(result['label'])
    scores.append(result['score'])

df['sentiment_label'] = labels
df['sentiment_score'] = scores

df.to_csv("data/processed/reviews_with_sentiment.csv", index=False)
print("Sentiment analysis complete! Saved to data/processed/")
