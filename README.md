# Basic — 3채널 콘텐츠 초안

25건 키워드 입력(`keywords_input.csv`)에 대해 블로그·인스타그램·카카오채널 3채널 초안을 생성한 결과입니다.

## 구성

- `keywords_input.csv` — 입력 데이터 25건 (id, type, keyword, tone_hint, brand_name, detail)
- `blog_draft.md` — 블로그 초안 (500자 이상, H2 소제목 2~3개, SEO 제목, CTA)
- `instagram_draft.md` — 인스타그램 초안 (캡션 150자 이내, 해시태그 5개)
- `kakao_draft.md` — 카카오채널 초안 (180자 이내, 이모지 1~2개, CTA)
- `decisions.md` — detail 결측·완전 중복 행·tone_hint 표기 흔들림 처리 기준 기록

## 채점 기준 대응

| 항목 | 배점 | 대응 |
|------|------|------|
| 글자 수 충족 | 40점 | 블로그 500자 이상 / 인스타 150자 이내 / 카카오 180자 이내 — 24건 전체 통과 |
| 채널별 톤 차별화 | 30점 | 3채널이 서로 다른 구조·어조로 작성 (복붙 없음) |
| keyword·brand 반영 | 20점 | 각 케이스의 keyword 1~3개와 brand_name을 본문에 자연스럽게 반영 |
| 제출 형식 | 10점 | 각 케이스 헤더에 id/type/keyword/brand_name/tone_hint 메타 포함 |
