# new_pipc_news_bot/fetcher/parser.py

import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        full_text = "\n".join(page.get_text() for page in doc)
        return full_text.strip()
    except Exception as e:
        print(f"❌ PDF 텍스트 추출 실패: {pdf_path}, 에러: {e}")
        return ""
