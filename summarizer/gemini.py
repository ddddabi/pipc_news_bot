# new_pipc_news_bot/summarizer/gemini.py

import google.generativeai as genai

def summarize_with_gemini(text, title="", config=None):
    api_key = config["gemini"]["api_key"]
    genai.configure(api_key=api_key)

    prompt = (
        "당신은 개인정보보호 전문가야.\n"
        "개인정보보호담당자들이 모여있는 부서에 개인정보와 관련한 동향을 간결하게 빠르게 전달하기 위해서 글을 요약할거야. "
        "독자가 개인정보 분야에서 전문성을 가지고 있는 사람이니, 글을 전문성있게 실무에 도움이 되는 방향으로 작성해줘.\n\n"
        "아래 지침을 지키지 않으면 넌 감옥에 가게 될거야.\n\n"
        "아래의 관련 텍스트를 읽고, 다음 지침에 따라 요약한 결과를 보여줘:\n"
        "1. 전체 내용을 20줄 이상으로 요약한 소제목을 달아서 ‘핵심 요약’ 필드에 작성해. 되도록이면 주요 내용이 다 들어갔으면 좋겠고, 파일에 있는 내용으로만 요약해줘.\n"
        "2. 요약한 전체 내용에서 핵심 내용을 3줄 이내로 간결하게 정리해서 '3줄 요약' 필드에 작성해.\n"
        "3. ‘한줄 요약’은 전체 내용을 1문장으로 작성해줘.\n"
        "4. 각 내용은 ~함, ~임 으로 단어로 마무리해줘.\n"
        "5. 텍스트의 핵심 키워드와 관련된 단어나 개념을 3~5개 내외로 'tags' 필드에 추가해.\n"
        "6. 숫자나 통계가 있다면 반드시 포함시켜서 변형하지 말고 요약해줘.\n"
        "7. 요약은 객관적이고 중립적인 톤을 유지해.\n"
        "8. 최종 결과는 ‘핵심요약’, ‘3줄 요약’, ‘한줄 요약’, ‘tags’로 나와야해.\n"
        "9. 요약해야 하는 내용은 텍스트로 줄게.\n"
        "10. 내가 원하는 포맷에 요약한 내용을 넣어서 출력해줘.\n\n"
        "11. pdf파일에 있는 내용으로만 요약해줘. 중립적으로 새로운 내용을 추가하지 말고 pdf파일에 있는 내용으로만 요약해줘.\n\n"

        "포맷:\n"
        f"[제목] {title}\n"
        "ThreeLineSummary: \n"
        "KeySummary: \n"
        "OneLineSummary: \n"
        "tags: \n"

        f"Content:\n{text[:8000]}\n"
    )

    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"❌ Gemini 요약 실패: {e}")
        return ""
