## 🧩 Lambda: Trigger Incremental AWS Glue Crawler

This AWS Lambda function is designed to automatically trigger a Glue crawler
configured for incremental updates (e.g., “Recrawl new subfolders only”).

### 🔐 Required IAM Permissions

The Lambda's execution role must include:

```json
{
  "Effect": "Allow",
  "Action": [
    "glue:GetCrawler",
    "glue:StartCrawler"
  ],
  "Resource": "*"
}
