# new_pipc_news_bot/monitor/watcher.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from utils import load_json, save_json
from pathlib import Path

def check_new_articles(config):
    list_url = config["monitor"]["list_url"]
    detail_prefix = config["monitor"]["detail_prefix"]
    bbs_id = config["monitor"]["bbs_id"]
    m_code = config["monitor"]["m_code"]
    log_path = Path(config["paths"]["log_dir"]) / "seen_news_ids.json"

    seen_ids = load_json(log_path)
    new_articles = []

    payload = {
        "bbsId": bbs_id,
        "mCode": m_code,
        "pageIndex": "1"
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.post(list_url, data=payload, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.select('table.board tbody tr')

    for row in rows:
        cells = row.find_all('td')
        if len(cells) < 4:
            continue

        title_tag = cells[1].find('a')
        if not title_tag:
            continue

        href = title_tag.get("href")
        if not href or "nttId=" not in href:
            continue

        query = urlparse(href).query
        nttId = parse_qs(query)["nttId"][0]

        if nttId in seen_ids:
            continue

        title = " ".join(title_tag.text.split()).strip().rstrip('N').strip()
        date = cells[3].text.strip().replace('.', '-')
        site_post_id = cells[0].text.strip()
        detail_url = detail_prefix + href

        article = {
            "nttId": nttId,
            "title": title,
            "date": date,
            "link": detail_url,
            "site_post_id": site_post_id
        }

        new_articles.append(article)
        seen_ids.append(nttId)

    # 저장
    save_json(log_path, seen_ids)

    return new_articles
