import os
import shutil
from pathlib import Path
import pandas as pd
from datetime import datetime
import json
import logging
from utils import load_config, init_sheet, send_webhook_message, setup_logging

# 로깅 설정
config = load_config()
log_file = Path(config["paths"]["log_dir"]) / "reset.log"
setup_logging(log_file)

def backup_and_reset_json(cfg, base_backup_dir):
    project_root = Path(__file__).resolve().parent

    json_file_keys = [
        "seen_ids_file",
        "sent_articles_file"
    ]

    for key in json_file_keys:
        rel_path = cfg["files"][key]
        abs_path = os.path.join(project_root, rel_path)
        filename = os.path.basename(rel_path)
        dst_path = os.path.join(base_backup_dir, filename)

        # ✅ 파일별 초기화 타입 지정
        if key in ["seen_ids_file", "sent_articles_file"]:
            initial_data = []
        else:
            initial_data = {}

        try:
            if os.path.exists(abs_path):
                shutil.copy(abs_path, dst_path)
                logging.info(f"💾 JSON 백업 완료: {filename}")
            else:
                logging.warning(f"⚠️ JSON 원본 없음: {abs_path}")

            with open(abs_path, 'w', encoding='utf-8') as f:
                json.dump(initial_data, f, ensure_ascii=False, indent=2)
            logging.info(f"🗑️ JSON 초기화 완료: {abs_path}")
        except Exception as e:
            logging.exception(f"❌ JSON 처리 실패 ({filename})")



def reset_backup():
    cfg = load_config()
    send_webhook_message("🧹 [Reset & BackUp] 시트 백업 및 초기화 시작", cfg["webhook"]["url"])

    # 📁 날짜 기반 백업 디렉토리
    today = datetime.utcnow().strftime("%Y-%m-%d")
    base_backup_dir = os.path.join(os.getcwd(), "backups", today)
    backup_pdf_dir = os.path.join(base_backup_dir, "pdfs")
    backup_summary_dir = os.path.join(base_backup_dir, "summaries")
    os.makedirs(backup_pdf_dir, exist_ok=True)
    os.makedirs(backup_summary_dir, exist_ok=True)

    # ✅ 시트 백업 및 초기화
    spreadsheet = init_sheet(cfg)
    target_sheets = ["보도자료 히스토리"]

    for sheet_name in target_sheets:
        try:
            sheet = spreadsheet.worksheet(sheet_name)
            records = sheet.get_all_records()
            if not records:
                logging.warning(f"⚠️ '{sheet_name}' 시트에 백업할 데이터가 없습니다.")
                continue

            df = pd.DataFrame(records)
            filename = f"{sheet_name.replace(' ', '_')}_{today}.csv"
            backup_path = os.path.join(base_backup_dir, filename)

            df.to_csv(backup_path, index=False, encoding='utf-8-sig')
            logging.info(f"📁 '{sheet_name}' 시트 백업 완료: {backup_path}")

            sheet.clear()
            sheet.update([df.columns.tolist()])
            logging.info(f"🧹 '{sheet_name}' 시트 초기화 완료.")
        except Exception as e:
            logging.error(f"❌ '{sheet_name}' 처리 중 오류 발생: {e}")

    # ✅ JSON 처리
    backup_and_reset_json(cfg, base_backup_dir)

    # ✅ PDF 파일 이동
    pdf_dir = cfg["paths"]["pdf_dir"]
    for filename in os.listdir(pdf_dir):
        if filename.endswith(".pdf"):
            src = os.path.join(pdf_dir, filename)
            dst = os.path.join(backup_pdf_dir, filename)
            try:
                shutil.move(src, dst)
                logging.info(f"📄 PDF 백업 완료: {filename}")
            except Exception as e:
                logging.error(f"❌ PDF 이동 실패: {filename} — {e}")

    # ✅ 요약 텍스트 파일 이동
    summary_dir = cfg["paths"]["summary_dir"]
    for filename in os.listdir(summary_dir):
        if filename.endswith(".txt"):
            src = os.path.join(summary_dir, filename)
            dst = os.path.join(backup_summary_dir, filename)
            try:
                shutil.move(src, dst)
                logging.info(f"📝 요약 백업 완료: {filename}")
            except Exception as e:
                logging.error(f"❌ 요약 파일 이동 실패: {filename} — {e}")

    send_webhook_message("✅ [Reset] 백업 및 초기화 완료", cfg["webhook"]["url"])


if __name__ == "__main__":
    reset_backup()
