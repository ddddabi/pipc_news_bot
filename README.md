# pipc_news_bot

**동향 파악 업무 (반)자동화 시스템**  
개인정보보호위원회 및 관련 기관의 보도자료를 주기적으로 감지하고, 첨부파일 요약 및 Google Sheets에 정리하는 자동화 봇입니다.

---

## 📌 프로젝트 개요

### 🎯 목적
- 개인정보위 보도자료 게시 주기를 사람이 수동으로 확인하던 문제를 해결
- 반복적인 업무 자동화로 정보 누락 방지 및 업무 효율 향상

### 🧭 주요 기능
- 새 게시글 자동 감지
- 첨부 PDF 자동 다운로드
- 텍스트 추출 및 AI 요약 (Gemini API 사용)
- Google Sheets 자동 기록
- Webhook으로 알림 전송

---

## 🛠 사용 기술 스택

| 항목 | 기술명 |
|------|--------|
| 크롤링 | Python, BeautifulSoup |
| 파일 다운로드 | requests, PyMuPDF |
| 요약 모델 | Gemini 1.5 Flash API (무료) |
| 데이터 저장 | JSON, Google Sheets |
| 자동 실행 | cron, Shell script |
| 기타 | Webhook, Logger |

> ChatGPT API는 요금 부담으로 제외하고, 무료인 Gemini API 사용

---

## 📁 파일 구조 및 구성

<img width="1140" alt="image" src="https://github.com/user-attachments/assets/13d58136-bae1-4c30-9e63-b41b3ace75fb" />

---

## 🔄 실행 흐름

<img width="1702" alt="image" src="https://github.com/user-attachments/assets/762099c0-f28f-4541-9de5-ba74f2d1107f" />


1. 크론탭 자동 실행 (예: 5분마다)
2. 새 게시글 감지 → 상세 페이지 접근
3. 첨부 PDF 다운로드 및 텍스트 추출
4. Gemini API로 요약 요청
5. 요약 결과 파싱 및 저장
6. Google Sheets에 기록
7. Webhook으로 메시지 전송
8. 처리된 게시글 ID 저장 → 중복 방지

---

## 📊 결과 예시

- ✅ Google Sheets 기록:  
  [📄 요약 엑셀 보기](https://docs.google.com/spreadsheets/d/1EPFzRwf9JrxEDsxZ1OJSPQIZW2KctYcfrprcCYIh6S8/edit?usp=sharing)
  <img width="1080" alt="image" src="https://github.com/user-attachments/assets/2a54f77e-1f04-402e-a2d9-edba4c8221f0" />


- ✅ Webhook 알림 (카카오워크 등)
  
  <img width="565" alt="image" src="https://github.com/user-attachments/assets/ec9d7353-71bb-4dfd-b60a-aa9779b3c9a8" />

- ✅ PDF 및 요약 로그 저장
  <img width="966" alt="image" src="https://github.com/user-attachments/assets/fea98685-08de-4609-8492-7f7179e68613" />

---

## 🔧 향후 개선 방향

1. 요약 품질 개선 (ChatGPT API 등 상위 모델 적용)
2. 자동화 대상 확대 (다른 정부 기관 사이트 추가)
3. 장기적으로는 워크플로우 확장 기반 구축

---

## 💡 기대 효과

- 수작업 90% 이상 감소
- 동향 누락 방지
- 반복 업무 자동화로 인한 생산성 향상

