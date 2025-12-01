# task4_analysis.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob

# -------------------------------
# 1. Load processed reviews
# -------------------------------
df = pd.read_csv(r'C:\Users\bia\Desktop\week2\data\processed\reviews_processed.csv')

# -------------------------------
# 2. Create sentiment column
# -------------------------------
def get_sentiment(text):
    score = TextBlob(str(text)).sentiment.polarity
    if score > 0.1:
        return 'positive'
    elif score < -0.1:
        return 'negative'
    else:
        return 'neutral'

df['sentiment'] = df['review_text'].apply(get_sentiment)

# -------------------------------
# 3. Sentiment summary per bank
# -------------------------------
sentiment_summary = df.groupby('bank_name')['sentiment'].value_counts(normalize=True).unstack().fillna(0)
print("\nSentiment Summary per Bank:\n", sentiment_summary)

# -------------------------------
# 4. Identify top 2 drivers & pain points per bank
# -------------------------------
drivers = {}
pain_points = {}

for bank in df['bank_name'].unique():
    bank_data = sentiment_summary.loc[bank]
    
    # Drivers: top 2 positive proportions
    top_drivers = bank_data.sort_values(ascending=False)[:2].index.tolist()
    drivers[bank] = top_drivers
    
    # Pain points: top 2 negative proportions
    top_pains = bank_data.sort_values()[:2].index.tolist()
    pain_points[bank] = top_pains

print("\nTop 2 Drivers per bank:", drivers)
print("Top 2 Pain Points per bank:", pain_points)

# -------------------------------
# 5. Visualizations
# -------------------------------

# 5.1 Sentiment proportion per bank
plt.figure(figsize=(8,6))
sentiment_summary.plot(kind='bar')
plt.title('Sentiment Proportion per Bank')
plt.ylabel('Proportion of Reviews')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('plots/sentiment_per_bank.png')
plt.show()

# 5.2 Rating distribution per bank
plt.figure(figsize=(8,6))
sns.histplot(data=df, x='rating', hue='bank_name', multiple='dodge', bins=5)
plt.title('Rating Distribution per Bank')
plt.xlabel('Rating')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig('plots/rating_distribution.png')
plt.show()

# -------------------------------
# 6. Recommendations per bank
# -------------------------------
print("\nRecommendations per bank:")
for bank in df['bank_name'].unique():
    print(f"{bank}:")
    print(f"  - Enhance drivers: {', '.join(drivers[bank])}")
    print(f"  - Address pain points: {', '.join(pain_points[bank])}")
