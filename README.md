# PEARL Commonality Data Collection Automation

This project automatically collects daily Cambodia and global news/trend information for PEARL commonality crops:

- Mango
- Cashew
- Rice
- Vegetables

It classifies the data by crop, market/commonality topic, Cambodia vs global source, and relevance. It uploads daily CSV/XLSX files and weekly Word reports to Google Drive.

## Required GitHub Secrets

Create these in GitHub repository settings:

1. `GOOGLE_DRIVE_FOLDER_ID`
   - Example: `1eOi4QKaDURiH9oo63qaf-9to3OcrTH1i`

2. `GOOGLE_SERVICE_ACCOUNT_JSON`
   - Paste the full content of your downloaded Google service account JSON file.

## GitHub Actions

- Daily collection: `.github/workflows/daily.yml`
- Weekly report: `.github/workflows/weekly.yml`

## Manual Run in GitHub

Go to:

Actions -> PEARL Daily News Collection -> Run workflow

## Google Drive Output

The automation creates:

- `01_Daily_News/YYYY-MM-DD/PEARL_commonality_news_YYYY-MM-DD.xlsx`
- `01_Daily_News/YYYY-MM-DD/PEARL_commonality_news_YYYY-MM-DD.csv`
- `03_Weekly_Report/PEARL_Weekly_Commonality_Report_YYYY-MM-DD.docx`

## Local test

```bash
pip install -r requirements.txt
set GOOGLE_DRIVE_FOLDER_ID=your_folder_id
set GOOGLE_SERVICE_ACCOUNT_JSON={full_json_here}
python pearl_daily_collector.py
```

For Windows, it is easier to test inside GitHub Actions because secrets are handled safely.
