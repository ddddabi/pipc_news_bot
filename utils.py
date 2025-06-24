import os
import json
import yaml
import requests
from pathlib import Path
from datetime import datetime
import logging
from pathlib import Path
from oauth2client.service_account import ServiceAccountCredentials
import gspread

def load_config(path='config.yaml'):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_json(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def send_webhook_message(message, webhook_url):
    try:
        response = requests.post(webhook_url, json={"text": message})
        if response.status_code != 200:
            print(f"❌ Webhook 전송 실패: {response.status_code}")
    except Exception as e:
        print(f"❌ Webhook 예외 발생: {e}")

def setup_logging(log_path):
    log_dir = Path(log_path).parent
    log_dir.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def init_sheet(config):
    try:
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']

        creds_path = config["google_sheets"].get("credentials_path", "service_account.json")
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
        client = gspread.authorize(creds)

        sheet_id = config["google_sheets"]["spreadsheet_id"]
        sheet = client.open_by_key(sheet_id)
        logging.info(f"✅ 스프레드시트 열기 성공: {sheet.title}")
        return sheet
    except Exception as e:
        logging.exception("❌ Google Sheets 초기화 실패")
        return None
