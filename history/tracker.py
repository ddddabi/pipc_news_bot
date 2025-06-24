# new_pipc_news_bot/history/tracker.py

from pathlib import Path
from utils import load_json, save_json

def is_already_processed(item_id, config):
    """
    이미 처리한 게시글인지 확인
    """
    log_path = Path(config["paths"]["log_dir"]) / "sent_articles.json"
    seen = load_json(log_path)
    return item_id in {item["nttId"] for item in seen}

def mark_as_processed(item_id, config):
    """
    게시글 ID를 sent_articles.json에 추가
    """
    log_path = Path(config["paths"]["log_dir"]) / "sent_articles.json"
    seen = load_json(log_path)

    if not any(item.get("nttId") == item_id for item in seen):
        seen.append({"nttId": item_id})
        save_json(log_path, seen)
