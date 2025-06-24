import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

import logging
import traceback
from pathlib import Path

from utils import load_config, setup_logging, send_webhook_message
from monitor.watcher import check_new_articles
from fetcher.downloader import download_pdfs
from fetcher.parser import extract_text_from_pdf
from summarizer.gemini import summarize_with_gemini
from summarizer.parser import parse_summary_text
from storage.sheet import write_summary_to_sheet
from history.tracker import is_already_processed, mark_as_processed


def save_summary_text_file(pdf_path, summary_text, config):
    summary_dir = Path(config["paths"]["summary_dir"])
    summary_dir.mkdir(parents=True, exist_ok=True)

    base_name = Path(pdf_path).stem
    txt_path = summary_dir / f"{base_name}_summary.txt"

    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(summary_text)

    logging.info(f"📝 요약 텍스트 저장 완료: {txt_path}")
    return txt_path


def format_webhook_message(article, summary):
    return (
        f"📢 새 보도자료: {article['title']}\n"
        f"🗓 작성일: {article['date']}\n"
        f"🔗 링크: {article['link']}\n\n"
        f"📝 한줄요약:\n{summary['one_line']}\n\n"
        f"🔥 3줄 요약:\n" + "\n".join(summary['three_line']) + "\n\n"
        f"🧩 핵심 요약:\n" + "\n".join(summary['key_points']) + "\n\n"
        f"#" + " #".join(summary['tags'])
    )


def main():
    config = load_config()
    log_file = Path(config["paths"]["log_dir"]) / "run.log"
    setup_logging(log_file)

    logging.info("🚀 개인정보위 보도자료 파이프라인 시작")

    try:
        articles = check_new_articles(config)
        if not articles:
            logging.info("❎ 새로운 게시글 없음.")
            return

        for article in articles:
            if is_already_processed(article["nttId"], config):
                logging.info(f"⏭ 이미 처리된 게시글: {article['nttId']}")
                continue

            logging.info(f"📄 새 게시글 처리 시작: {article['title']}")
            pdf_paths = download_pdfs(article, config)
            if not pdf_paths:
                logging.warning(f"❌ PDF 없음: {article['title']}")
                continue

            for pdf_path in pdf_paths:
                text = extract_text_from_pdf(pdf_path)
                if not text:
                    logging.warning(f"❌ PDF 텍스트 추출 실패: {pdf_path}")
                    continue

                summary_text = summarize_with_gemini(text, title=article["title"], config=config)
                if not summary_text:
                    logging.error(f"❌ Gemini 요약 실패: {pdf_path}")
                    continue

                save_summary_text_file(pdf_path, summary_text, config)

                summary = parse_summary_text(summary_text, article["title"])
                if not summary:
                    logging.warning(f"❌ 요약 파싱 실패: {pdf_path}")
                    continue

                write_summary_to_sheet(article, summary, config)

                message = format_webhook_message(article, summary)
                send_webhook_message(message, config["webhook"]["url"])

                mark_as_processed(article["nttId"], config)
                logging.info(f"✅ 완료: {article['title']}")

    except Exception as e:
        logging.error("🚨 예외 발생:\n" + traceback.format_exc())

    logging.info("🏁 파이프라인 종료")


if __name__ == "__main__":
    main()
