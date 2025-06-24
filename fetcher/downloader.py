# new_pipc_news_bot/fetcher/downloader.py

import os
import requests
from bs4 import BeautifulSoup
from pathlib import Path

def download_pdfs(article, config):
    detail_url = article["link"]
    pdf_dir = Path(config["paths"]["pdf_dir"])
    pdf_dir.mkdir(parents=True, exist_ok=True)

    try:
        res = requests.get(detail_url)
        res.raise_for_status()
    except Exception as e:
        print(f"❌ 상세페이지 요청 실패: {e}")
        return []

    soup = BeautifulSoup(res.text, 'html.parser')
    links = soup.find_all("a", class_="downBtn")
    if not links:
        print(f"❌ PDF 다운로드 링크 없음: {detail_url}")
        return []

    saved_files = []

    for link in links:
        onclick = link.get("onclick", "")
        filename = link.get("alt") or link.get("title") or "첨부파일"

        if "fn_egov_downFile" not in onclick:
            continue

        try:
            params = onclick.split("fn_egov_downFile(")[1].split(")")[0]
            atchFileId, fileSn, fileExt = [x.strip("' ") for x in params.split(',')]

            if fileExt.lower() != "pdf":
                print(f"⏭ PDF 아님 스킵: {filename} ({fileExt})")
                continue

            download_url = f"https://www.pipc.go.kr/np/cmm/fms/FileDown.do?atchFileId={atchFileId}&fileSn={fileSn}"
            clean_name = filename.strip().replace(" ", "_").replace("/", "_")
            if not clean_name.endswith(".pdf"):
                clean_name += ".pdf"

            filepath = pdf_dir / clean_name
            headers = {"User-Agent": "Mozilla/5.0", "Referer": detail_url}
            file_res = requests.get(download_url, headers=headers)

            if file_res.status_code != 200:
                print(f"❌ 다운로드 실패 {file_res.status_code}: {download_url}")
                continue

            with open(filepath, "wb") as f:
                f.write(file_res.content)

            print(f"✅ 저장 완료: {filepath}")
            saved_files.append(filepath)

        except Exception as e:
            print(f"❌ PDF 처리 실패: {e}")
            continue

    return saved_files
