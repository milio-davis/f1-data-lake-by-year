# f1-data-lake-by-year
F1 Data Lake & Analysis on AWS

Beginner Project: F1 Data Lake and Analysis with S3 + Athena + Glue. 
Goal: Build a centralized data lake for historical F1 race data.
This project demonstrates how to build a lightweight data lake on AWS using Formula 1 data. 

Tech Stack:
Lambda Python: Data ingestion
S3: Raw data storage
Glue: Crawler & Catalog
Athena: SQL-based analysis
QuickSight: Dashboard

1. Ingest public F1 data with AWS Lambda
2. Store it in Amazon S3
3. Catalog it with AWS Glue
4. Query it with AWS Athena
5. View it with AWS QuickSight

Ergast F1 API
       ↓
AWS Lambda (Ingestion script)
       ↓
AWS S3 (Raw Data)
       ↓
AWS Glue Crawler → AWS Glue Data Catalog
       ↓
AWS Athena (SQL Queries)
       ↓
AWS QuickSight
