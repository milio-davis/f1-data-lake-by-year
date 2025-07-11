# 🏎️ Formula 1 Data Lake & Analysis on AWS

<img src="https://github.com/user-attachments/assets/57f39ce2-7899-40d2-9121-02c367975a4e" alt="drawing" height="70%" />

![image](https://github.com/user-attachments/assets/580c2226-7a9d-4c73-92aa-9f49e83c10be)

# Lambda + S3 + Glue + Athena + QuickSight + IAM

## 🎯 Goal
Build a centralized data lake for historical Formula 1 race data.  
This project demonstrates how to build a lightweight, serverless data lake on AWS using F1 data.

## 📊 Project Highlights
- Serverless and event-driven architecture
- Cloud-native using AWS-native services only
- Scalable and low-cost
- Ready for interactive analysis in QuickSight

## ⚙️ AWS Tech Stack
1. **Lambda (Python)** – Public F1 API data ingestion on demand for a desired year
2. **S3** – Raw Parquet data storage in partitioned folder structure
3. **Glue** –  
   - Data Crawlers for schema discovery  
   - Glue Catalog for centralized metadata  
   - Incremental partition crawling using Lambda + Crawler
4. **Athena** – SQL-based analysis
5. **QuickSight** – Interactive dashboards and visualizations
6. **Identity and Access Management (IAM)** - Security and permissions

### 🧩 Incremental Crawling Automation
To keep the data catalog always up-to-date without reprocessing the full dataset, the project includes:

### ✅ Setup
- **Folder structure**:
  Data is stored as:
    - s3://bucket/raw/year=2025/drivers/drivers.parquet
    - s3://bucket/raw/year=2025/races/races.parquet
- **Crawler configuration**:
- Recrawl behavior: **“Recrawl new subfolders only”**
- Partition keys: e.g., `year`
- One Glue table per subfolder (e.g., `drivers`, `races`)

- **Trigger**:  
A Python-based **Lambda function** automatically starts the incremental Glue crawler when new files are added to S3 (via S3 PUT events).

### 🐍 Lambda Function Overview
- Validates crawler state (`READY`) before running
- Starts the Glue crawler
- Fully event-driven, no manual steps needed after deployment

## 🏁 Project screenshots:
<img width="1450" height="600" alt="image" src="https://github.com/user-attachments/assets/10e5960e-7bc2-4d4c-94c7-c617623a3eed" />

<img width="1450" height="600" alt="image" src="https://github.com/user-attachments/assets/029e22ca-e344-43a9-8e90-968a23e545b5" />

<img width="1450" height="600" alt="image" src="https://github.com/user-attachments/assets/6d166918-3f51-47c8-8622-164b6f499e6a" />

<img width="1450" height="600" alt="image" src="https://github.com/user-attachments/assets/4bae34f0-a31d-4c3f-ac56-9576a5f5decb" />

<img width="1450" height="600" alt="image" src="https://github.com/user-attachments/assets/8dc400e4-9009-4c57-89a3-e1f33bfe15fe" />

<img width="1450" height="600" alt="image" src="https://github.com/user-attachments/assets/a2e69fbf-1c82-4ac4-a7bc-13a0ccc334bd" />

<img width="1450" height="600" alt="image" src="https://github.com/user-attachments/assets/7450272e-1455-4be3-868c-f9be0e0342d7" />

<img width="1450" height="600" alt="image" src="https://github.com/user-attachments/assets/0865a749-5479-4a24-899f-baaacb66e725" />
