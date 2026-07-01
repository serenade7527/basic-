# -*- coding: utf-8 -*-
"""build_html.py — blog/instagram/kakao_draft.md를 보기 좋은 단일 HTML 페이지로 변환.

사용법:
    python build_html.py
    (같은 폴더의 blog_draft.md / instagram_draft.md / kakao_draft.md를 읽어
     같은 폴더에 index.html을 생성한다)
"""

import html
import re
from pathlib import Path

BASE = Path(__file__).parent
CASE_HEADER = re.compile(r"^## 케이스 #(\S+) · (\S+) · (.+)$")
ANNOTATION = re.compile(r"^\*\(.*\)\*$")


def split_cases(text: str) -> list[dict]:
    cases = []
    current = None
    for line in text.splitlines():
        m = CASE_HEADER.match(line.strip())
        if m:
            if current:
                cases.append(current)
            case_id, ctype, keyword = m.groups()
            note = ""
            note_m = re.search(r"\s*(\(detail 결측.*\))$", keyword)
            if note_m:
                note = note_m.group(1)
                keyword = keyword[: note_m.start()].strip()
            current = {"id": case_id, "type": ctype, "keyword": keyword, "note": note, "lines": []}
        elif current is not None:
            current["lines"].append(line)
    if current:
        cases.append(current)
    return cases


def meta_and_body(case: dict) -> tuple[str, str, list[str], str]:
    brand, tone = "", ""
    body, annotation = [], ""
    for line in case["lines"]:
        s = line.strip()
        if not s or s == "---":
            continue
        if s.startswith("**brand_name**"):
            m = re.match(r"\*\*brand_name\*\*:\s*(.+?)\s*\|\s*\*\*tone_hint\*\*:\s*(.+)", s)
            if m:
                brand, tone = m.group(1), m.group(2)
            continue
        if ANNOTATION.match(s):
            annotation = s.strip("*()")
            continue
        body.append(s)
    return brand, tone, body, annotation


def blog_card(case: dict) -> str:
    brand, tone, body, annotation = meta_and_body(case)
    title = next((l.replace("**제목**:", "").strip() for l in body if l.startswith("**제목**")), "")
    parts = []
    para = None
    for l in body:
        if l.startswith("**제목**"):
            continue
        if l.startswith("## "):
            parts.append(f"<h4>{html.escape(l[3:])}</h4>")
        elif "→" in l:
            parts.append(f'<p class="cta">{html.escape(l)}</p>')
        else:
            parts.append(f"<p>{html.escape(l)}</p>")
    return card(case, brand, tone, f'<p class="title">{html.escape(title)}</p>' + "".join(parts), annotation)


def insta_card(case: dict) -> str:
    brand, tone, body, annotation = meta_and_body(case)
    tags_line = next((l for l in body if l.startswith("#")), "")
    caption = "".join(l for l in body if not l.startswith("#"))
    tags = "".join(f'<span class="tag">{html.escape(t)}</span>' for t in tags_line.split())
    content = f'<p class="caption">{html.escape(caption)}</p><div class="tags">{tags}</div>'
    return card(case, brand, tone, content, annotation)


def kakao_card(case: dict) -> str:
    brand, tone, body, annotation = meta_and_body(case)
    content = "".join(f"<p>{html.escape(l)}</p>" for l in body)
    return card(case, brand, tone, content, annotation)


def card(case: dict, brand: str, tone: str, content_html: str, annotation: str) -> str:
    note = f'<span class="note">{html.escape(case["note"])}</span>' if case["note"] else ""
    return f"""
    <div class="card">
      <div class="card-head">
        <span class="badge id">#{html.escape(case['id'])}</span>
        <span class="badge type">{html.escape(case['type'])}</span>
        <span class="keyword">{html.escape(case['keyword'])}</span>
        {note}
      </div>
      <div class="meta">{html.escape(brand)} · {html.escape(tone)}</div>
      <div class="content">{content_html}</div>
      <div class="annotation">{html.escape(annotation)}</div>
    </div>"""


def build_section(channel_id: str, label: str, cases: list[dict], render) -> str:
    cards = "".join(render(c) for c in cases)
    active = "active" if channel_id == "blog" else ""
    return f'<section id="{channel_id}" class="panel {active}"><h2>{label} ({len(cases)}건)</h2>{cards}</section>'


def main() -> None:
    blog = split_cases((BASE / "blog_draft.md").read_text(encoding="utf-8"))
    insta = split_cases((BASE / "instagram_draft.md").read_text(encoding="utf-8"))
    kakao = split_cases((BASE / "kakao_draft.md").read_text(encoding="utf-8"))

    sections = (
        build_section("blog", "블로그", blog, blog_card)
        + build_section("instagram", "인스타그램", insta, insta_card)
        + build_section("kakao", "카카오채널", kakao, kakao_card)
    )

    html_doc = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>올인원장 — Basic 3채널 콘텐츠 초안</title>
<style>
  :root {{ --blog:#2563eb; --insta:#db2777; --kakao:#eab308; }}
  * {{ box-sizing: border-box; }}
  body {{ font-family: -apple-system, "Malgun Gothic", "Apple SD Gothic Neo", sans-serif;
          background:#f5f6f8; color:#1f2430; margin:0; }}
  header {{ background:#111827; color:#fff; padding:28px 20px; text-align:center; }}
  header h1 {{ margin:0 0 6px; font-size:22px; }}
  header p {{ margin:0; color:#9ca3af; font-size:14px; }}
  nav {{ display:flex; justify-content:center; gap:8px; padding:16px; background:#fff;
         border-bottom:1px solid #e5e7eb; position:sticky; top:0; }}
  nav button {{ border:none; background:#f3f4f6; padding:10px 20px; border-radius:20px;
                font-size:14px; font-weight:600; cursor:pointer; color:#4b5563; }}
  nav button.active {{ background:#111827; color:#fff; }}
  .wrap {{ max-width:880px; margin:0 auto; padding:24px 16px 60px; }}
  .panel {{ display:none; }}
  .panel.active {{ display:block; }}
  .panel h2 {{ font-size:17px; margin:0 0 16px; color:#374151; }}
  .card {{ background:#fff; border-radius:14px; padding:20px 22px; margin-bottom:16px;
           box-shadow:0 1px 3px rgba(0,0,0,.06); }}
  .card-head {{ display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-bottom:8px; }}
  .badge {{ font-size:12px; font-weight:700; padding:3px 9px; border-radius:12px; color:#fff; }}
  .badge.id {{ background:#374151; }}
  .badge.type {{ background:#0ea5e9; }}
  .keyword {{ font-size:13px; color:#6b7280; }}
  .note {{ font-size:11px; color:#b45309; background:#fef3c7; padding:2px 8px; border-radius:10px; }}
  .meta {{ font-size:12px; color:#9ca3af; margin-bottom:10px; }}
  .content p {{ margin:0 0 10px; line-height:1.6; font-size:14px; }}
  .content .title {{ font-weight:700; font-size:15px; color:#111827; }}
  .content h4 {{ font-size:14px; margin:14px 0 6px; color:#1f2937; }}
  .content .cta {{ color:var(--blog); font-weight:600; }}
  .content .caption {{ font-size:15px; }}
  .tags {{ margin-top:6px; }}
  .tag {{ display:inline-block; font-size:12px; color:var(--insta); margin-right:6px; }}
  .annotation {{ font-size:11px; color:#9ca3af; border-top:1px dashed #e5e7eb; padding-top:8px; margin-top:6px; }}
  #blog .badge.type {{ background:var(--blog); }}
  #instagram .badge.type {{ background:var(--insta); }}
  #kakao .badge.type {{ background:var(--kakao); }}
</style>
</head>
<body>
<header>
  <h1>올인원장 — Basic 3채널 콘텐츠 초안</h1>
  <p>keywords_input.csv 25건 → 블로그·인스타그램·카카오채널 자동 생성 결과</p>
</header>
<nav>
  <button class="active" onclick="show('blog', this)">블로그</button>
  <button onclick="show('instagram', this)">인스타그램</button>
  <button onclick="show('kakao', this)">카카오채널</button>
</nav>
<div class="wrap">
{sections}
</div>
<script>
function show(id, btn) {{
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('nav button').forEach(b => b.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  btn.classList.add('active');
}}
</script>
</body>
</html>
"""

    out_path = BASE / "index.html"
    out_path.write_text(html_doc, encoding="utf-8")
    print(f"[완료] {out_path} 생성 ({len(blog)}/{len(insta)}/{len(kakao)}건)")


if __name__ == "__main__":
    main()
