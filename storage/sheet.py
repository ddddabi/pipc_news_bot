# new_pipc_news_bot/storage/sheet.py

import gspread
import logging
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from datetime import datetime, timedelta, timezone

KST = timezone(timedelta(hours=9))

def write_summary_to_sheet(article, summary, config):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds_path = config["google_sheets"].get("credentials_path", "service_account.json")
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)

    sheet_id = config["google_sheets"]["spreadsheet_id"]
    worksheet_name = config["google_sheets"]["worksheet_name"]

    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.worksheet(worksheet_name)

    def safe_join(lines):
        return " / ".join(line.strip().replace("\n", " ") for line in lines if line.strip())
    
    now_kst = datetime.now(KST).strftime("%Y-%m-%d %H:%M")
    three_line_summary = safe_join(summary.get("three_line", [])) or "요약 없음"
    key_points = safe_join(summary.get("key_points", []))
    one_line = summary.get("one_line", "") or "요약 없음"
    tags = ", ".join(summary.get("tags", []))

    def safe_join(lines):
        return " / ".join(line.strip().replace("\n", " ") for line in lines if line.strip())

    row = [
        now_kst,                        # 검색일시 (오늘 날짜)
        article["date"],               # 작성일
        article["site_post_id"],       # 번호
        article["title"],
        article["link"],
        safe_join(summary.get("three_line", [])) or "요약 없음",
        safe_join(summary.get("key_points", [])) or "요약 없음",
        summary.get("one_line", "") or "요약 없음",
        ", ".join(summary.get("tags", []))
    ]

    worksheet.append_row(row, value_input_option="USER_ENTERED")
    logging.info(f"📄 Google Sheets 기록 완료: {article['title']}")