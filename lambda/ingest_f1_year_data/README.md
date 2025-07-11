# 🚀 Lambda: Ingest F1 Data to S3

This Lambda function uploads F1 data to an AWS S3 bucket. It creates and stores 4 datasets in a single year folder: races, drivers, races and results.

## 🧰 What It Does
- Gets Ergast F1 data API for the desired year
- Creates Pandas DataFrames 
- Converts them to Parquet
- Uploads to configured S3 bucket

## 📦 Requirements
pip install -r requirements.txt
