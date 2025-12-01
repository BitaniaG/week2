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
