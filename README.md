# Medical Telegram Data Warehouse

Data pipeline for Ethiopian medical Telegram channels.

## Setup
pip install -r requirements.txt

## Environment
Create .env file with:
- API_ID, API_HASH (from my.telegram.org)
- DB_PASSWORD (PostgreSQL password)

## Tasks
1. Telegram scraping with Telethon
2. dbt transformation with star schema
3. YOLO object detection
4. FastAPI analytical API
5. Dagster orchestration

## Structure
- data/raw/ - Data lake (JSON + images)
- medical_warehouse/ - dbt project
- src/ - Python scripts
- api/ - FastAPI application
