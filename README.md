# week2
Customer Experience Analytics for Fintech Apps

Task 3 — PostgreSQL Database Setup
Database

Name: bank_reviews

Tables
1. banks
| Column    | Type         | Notes       |
| --------- | ------------ | ----------- |
| bank_id   | SERIAL       | PRIMARY KEY |
| bank_name | VARCHAR(255) | Bank name   |
| app_name  | VARCHAR(255) | App package |

2. reviews
| Column          | Type        | Notes                        |
| --------------- | ----------- | ---------------------------- |
| review_id       | SERIAL      | PRIMARY KEY                  |
| bank_id         | INT         | FOREIGN KEY → banks(bank_id) |
| review_text     | TEXT        | Processed review text        |
| rating          | INT         | Review rating                |
| review_date     | DATE        | Review date                  |
| sentiment_label | VARCHAR(50) | Optional sentiment category  |
| sentiment_score | FLOAT       | Optional sentiment score     |
| source          | VARCHAR(50) | Review source                |

Insert Script

File: scripts/insert_to_postgres.py

Instructions:

Make sure PostgreSQL is installed and running.

Update the password in the script:

conn = psycopg2.connect(
    host="localhost",
    dbname="bank_reviews",
    user="postgres",
    password="YOUR_PASSWORD"   # <-- replace with your password
)


Run the script from the VS Code terminal:

python scripts/insert_to_postgres.py


The script will insert all processed reviews into the reviews table.

Verify in PostgreSQL:

SELECT COUNT(*) FROM reviews;
SELECT bank_id, COUNT(*) FROM reviews GROUP BY bank_id;
SELECT bank_id, AVG(rating) FROM reviews GROUP BY bank_id;

Task 4: App Review Insights and Recommendations

This task analyzes user reviews for three banks’ mobile apps (Abyssinia Bank, Commercial Bank of Ethiopia, Dashen Bank) to derive insights and actionable recommendations.

Key Steps

Load and process reviews: Using reviews_processed.csv.

Sentiment analysis: Each review is labeled as positive, neutral, or negative using TextBlob.

Sentiment summary: Calculates proportion of each sentiment per bank.

Drivers and pain points:

Top 2 drivers: aspects users liked most (positive/neutral sentiment).

Top 2 pain points: aspects with negative feedback.

Visualizations:

Sentiment proportion per bank (plots/sentiment_per_bank.png)

Rating distribution per bank (plots/rating_distribution.png)

Recommendations: Suggested improvements for each bank based on drivers and pain points.

How to Run
python scripts/task4_analysis.py


Plots will be saved in the plots folder.

Recommendations and sentiment summaries are printed in the terminal.

Notes

Reviews may be biased: negative feedback is often overrepresented.

Currently, the analysis is sentiment-based only, without feature-level themes. Adding themes can provide more granular insights.