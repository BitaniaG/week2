# task4_analysis.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
from wordcloud import WordCloud

# -------------------------------
# 1. Load processed reviews
# -------------------------------
df = pd.read_csv(r'C:\Users\bia\Desktop\week2\data\processed\reviews_processed.csv')

# -------------------------------
# 2. Add theme column
# -------------------------------
def assign_theme(text):
    text = str(text).lower()
    if any(word in text for word in ['slow', 'navigation', 'menu', 'lag']):
        return 'Navigation'
    elif any(word in text for word in ['payment', 'transfer', 'deposit', 'withdraw']):
        return 'Payments'
    elif any(word in text for word in ['interface', 'layout', 'design', 'ui']):
        return 'UI'
    elif any(word in text for word in ['support', 'help', 'chat', 'service']):
        return 'Customer Service'
    else:
        return 'Other'

df['theme'] = df['review_text'].apply(assign_theme)

# Optional: save updated CSV
df.to_csv(r'C:\Users\bia\Desktop\week2\data\processed\reviews_processed_with_theme.csv', index=False)

# -------------------------------
# 3. Sentiment analysis
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
# 4. Sentiment summary per bank and theme
# -------------------------------
sentiment_summary = df.groupby(['bank_name','theme'])['sentiment'].value_counts(normalize=True).unstack().fillna(0)
print("\nSentiment Summary per Bank and Theme:\n", sentiment_summary)

# -------------------------------
# 5. Identify top 2 drivers & pain points per bank per theme
# -------------------------------
drivers = {}
pain_points = {}

for bank in df['bank_name'].unique():
    bank_data = sentiment_summary.loc[bank]
    for theme in bank_data.index:
        top_drivers = bank_data.loc[theme].sort_values(ascending=False)[:2].index.tolist()
        top_pains = bank_data.loc[theme].sort_values()[:2].index.tolist()
        drivers[f"{bank} - {theme}"] = top_drivers
        pain_points[f"{bank} - {theme}"] = top_pains

print("\nTop Drivers per Bank and Theme:")
for key, value in drivers.items():
    print(f"{key}: {value}")

print("\nTop Pain Points per Bank and Theme:")
for key, value in pain_points.items():
    print(f"{key}: {value}")

# -------------------------------
# 6. Visualizations
# -------------------------------

# 6.1 Sentiment proportion per bank
plt.figure(figsize=(8,6))
bank_sentiment = df.groupby('bank_name')['sentiment'].value_counts(normalize=True).unstack().fillna(0)
bank_sentiment.plot(kind='bar')
plt.title('Sentiment Proportion per Bank')
plt.ylabel('Proportion of Reviews')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('plots/sentiment_per_bank.png')
plt.show()

# 6.2 Rating distribution per bank
plt.figure(figsize=(8,6))
sns.histplot(data=df, x='rating', hue='bank_name', multiple='dodge', bins=5)
plt.title('Rating Distribution per Bank')
plt.xlabel('Rating')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig('plots/rating_distribution.png')
plt.show()

# 6.3 WordCloud per theme
for theme in df['theme'].unique():
    text = " ".join(df[df['theme'] == theme]['review_text'])
    if text.strip():  # skip empty themes
        wc = WordCloud(width=800, height=400, background_color='white').generate(text)
        wc.to_file(f"plots/wordcloud_{theme.replace(' ','_')}.png")

# -------------------------------
# 7. Recommendations per bank
# -------------------------------
print("\nRecommendations per Bank and Theme:")
for bank in df['bank_name'].unique():
    print(f"\n{bank}:")
    for theme in df['theme'].unique():
        key = f"{bank} - {theme}"
        print(f"  Theme: {theme}")
        print(f"    - Enhance drivers: {', '.join(drivers.get(key, []))}")
        print(f"    - Address pain points: {', '.join(pain_points.get(key, []))}")
