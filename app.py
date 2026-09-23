# -*- coding: utf-8 -*-
"""서논술형 답안 연습 — 광고·홍보물의 재현과 관점 (Streamlit)"""

import json
import re
import datetime as dt
from pathlib import Path

import streamlit as st

# 데이터
SETS = [
    {
        "id": "set1",
        "adA": "ad_a.png",
        "adB": "ad_b.png",
        "adC": "ad_c.png",
        "adText": {
            "A": "(가) 광고: 신선한 채소를 강조하며 '자연을 베어 물다'라는 문구가 적혀 있다.",
            "B": "(나) 광고: 바쁜 직장인이 빠르게 식사하는 모습과 '1분 완성, 당신의 에너지'라는 문구가 있다.",
            "C": "공익 광고: 일회용 컵이 산처럼 쌓여 있는 이미지."
        },
        "q1": {
            "rowA": {
                "t": "자연을 베어 물다",
                "i": "신선한 채소와 두툼한 패티"
            },
            "items": [
                {
                    "id": "q1-1",
                    "label": "( ㉠ ) 문구",
                    "short": True,
                    "key": {
                        "ex": "1분 완성, 당신의 에너지",
                        "ok": ["당신의 에너지", "1분 완성"],
                        "no": ["빠르게 먹다", "바쁜 직장인"]
                    }
                },
                {
                    "id": "q1-2",
                    "label": "( ㉡ ) 이미지",
                    "short": False,
                    "key": {
                        "ex": "바쁘게 먹고 가는 모습으로, 제품의 간편함과 신속함을 강조한다.",
                        "ok": ["바쁜 사람의 모습으로 신속함을 보여준다.", "빠르게 먹는 모습으로 간편함을 나타낸다."],
                        "no": ["맛있게 먹는다.", "채소가 신선하다."]
                    }
                }
            ]
        },
        "q2": {
            "items": [
                {
                    "id": "q2-1",
                    "label": "제작자의 관점과 의도",
                    "short": False,
                    "key": {
                        "ex": "관점은 '햄버거'를 '빠른 에너지 충전 수단'으로 본다. 그렇게 생각한 이유는 '바쁜 직장인이 빠르게 식사하는 모습' 때문이다. 의도는 제작자는 광고를 본 사람이 '제품을 구매'하게 하려 한다.",
                        "ok": ["관점은 햄버거를 간편한 식사로 본다.", "의도는 햄버거를 사 먹게 하려 한다."],
                        "no": ["관점은 햄버거를 자연으로 본다."]
                    }
                }
            ]
        },
        "q3": {
            "buy": "광고가 대상의 단면만 보여주는 것은 아닌지 생각하며 비판적으로 읽어야 해.",
            "think1": "이 광고는 환경 오염의 심각성을 보여주고 있어.",
            "think2": "하지만 일상적인 실천 방안이나 대안은 부족해.",
            "obj": "일회용 컵",
            "items": [
                {
                    "id": "q3-1",
                    "label": "㉠",
                    "short": True,
                    "key": {
                        "ex": "환경 오염의 원인",
                        "ok": ["쓰레기 문제", "자연 훼손"],
                        "no": ["편리한 도구"]
                    }
                },
                {
                    "id": "q3-2",
                    "label": "㉡",
                    "short": True,
                    "key": {
                        "ex": "해결해야 할 문제",
                        "ok": ["심각한 상황"],
                        "no": ["일상적인 것"]
                    }
                },
                {
                    "id": "q3-3",
                    "label": "(2) 제작자의 의도",
                    "short": False,
                    "key": {
                        "ex": "광고를 본 사람이 '일회용 컵 사용을 줄이도록' 하려 한다. 그렇게 생각한 이유는 '일회용 컵이 산처럼 쌓인 이미지' 때문이다.",
                        "ok": ["환경을 보호하게 하려 한다.", "쓰레기 산 이미지를 통해 경각심을 주려 한다."],
                        "no": ["일회용 컵을 쓰게 하려 한다."]
                    }
                }
            ]
        }
    }
]

HERE = Path(__file__).parent
IMG_DIR = HERE / "images"

st.set_page_config(page_title="서논술형 답안 연습", page_icon="✍️", layout="centered")

# ---------------------------------------------------------------- 페이지 목록
PAGES = []
for si, s in enumerate(SETS, 1):
    for qi, qk in enumerate(["q1", "q2", "q3"], 1):
        PAGES.append({"id": f"{s['id']}-{qk}", "set": s, "qkey": qk, "tab": f"{si}-{qi}", "name": f"{si}번 세트 – 서·논술형 {qi}"})
PAGES.append({"id": "result", "tab": "결과", "name": "결과 정리"})
PAGE_IDS = [p["id"] for p in PAGES]

ss = st.session_state
ss.setdefault("page", PAGE_IDS[0])
ss.setdefault("answers", {})
ss.setdefault("verdicts", {})
ss.setdefault("graded", set())
ss.setdefault("student", "")

def akey(set_id, item_id):
    return f"{set_id}-{item_id}"

# ---------------------------------------------------------------- 채점
GRADE_RULES = (
    "[판정 원칙]\n"
    "1. 표현이 예시 답안과 달라도 인정 기준의 뜻을 담고 있으면 '정'. 맞춤법·문장 다듬기는 판정에 넣지 않는다.\n"
    "2. 재현 방법을 명시하지 않아도 그 문구·이미지가 드러내는 광고의 '뜻'이 있으면 '정'. 감상만 있으면 '오'.\n"
    "3. 근거(이유)는 구체적이어야 하며 효과가 나타나야 한다. 인용만 있고 효과가 없으면 '오'.\n"
    "4. 점수나 부분점수를 절대 언급하지 않는다.\n"
    "5. feedback은 한 문장으로 친절하게 작성한다. '오'일 때는 정답을 그대로 알려주지 않는다.\n"
    "6. 답이 비어 있거나 무의미하면 '오'로 하고 feedback에 답을 써달라고 한다."
)

def build_prompt(s, qkey, answers):
    q = s[qkey]
    if qkey == "q1":
        qdesc = (
            "[문항] 서·논술형 1. (나) 광고의 문구(㉠)와 이미지(㉡)에 대해 그로 인한 효과를 쓴다.\n"
            f"참고(가): 문구: {q['rowA']['t']} / 이미지: {q['rowA']['i']}"
        )
        ad = s["adText"]["A"] + "\n" + s["adText"]["B"]
    elif qkey == "q2":
        qdesc = (
            "[문항] 서·논술형 2. 관점과 의도 서술.\n"
            "틀: 관점은 '( )을/를 ( )로/으로 본다. 이유는 ( ) 때문이다.', 의도는 '사람이 ( )하게 하려 한다.'"
        )
        ad = s["adText"]["A"] + "\n" + s["adText"]["B"]
    else:
        qdesc = (
            f"[문항] 서·논술형 3. ㉠·㉡에는 광고 속 {q['obj']}을/를 무엇으로 보는지 쓴다.\n"
            "(2)는 수정 전 의도를 '사람이 ( )하게 하려 한다. 이유는 ( ) 때문이다.'에 맞춰 쓴다."
        )
        ad = s["adText"]["C"]
        
    keys = "\n".join(
        f"- {it['id']} ({it['label']})\n  예시: {it['key']['ex']}\n  인정: {' / '.join(it['key']['ok'])}\n  불인정: {' / '.join(it['key']['no'])}"
        for it in q["items"]
    )
    ans = "\n".join(f"- {it['id']}: {json.dumps(answers[it['id']], ensure_ascii=False)}" for it in q["items"])
    
    return (
        f"중2 국어 교사로서 아래 기준을 읽고 '정' 또는 '오'로 판정하세요.\n\n"
        f"[광고 설명]\n{ad}\n\n{qdesc}\n\n[인정답안 기준]\n{keys}\n\n{GRADE_RULES}\n\n[학생 답안]\n{ans}\n\n"
        "반드시 JSON 배열만 출력하세요: [{\"id\":\"q1a\",\"verdict\":\"정\",\"feedback\":\"...\"}]"
    )

def secret(name, default=None):
    try:
        return st.secrets.get(name, default)
    except Exception:
        return default

@st.cache_resource
def get_client():
    import anthropic
    key = secret("ANTHROPIC_API_KEY", "")
    if not key:
        return None
    return anthropic.Anthropic(api_key=key)

def call_grader(prompt):
    client = get_client()
    if client is None:
        raise RuntimeError("ANTHROPIC_API_KEY 설정이 필요합니다.")
    model = secret("MODEL", "claude-sonnet-4-6")
    msg = client.messages.create(model=model, max_tokens=1200, messages=[{"role": "user", "content": prompt}])
    text = "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")
    
    backticks = chr(96) * 3
    text = text.replace(f"{backticks}json", "").replace(backticks, "").strip()
    
    m = re.search(r"\[.*\]", text, re.S)
    return json.loads(m.group(0) if m else text)

def grade(s, qkey):
    q = s[qkey]
    answers = {it["id"]: ss.answers.get(akey(s["id"], it["id"]), "").strip() for it in q["items"]}
    if not any(answers.values()):
        ss["msg"] = ("warning", "먼저 답을 써 주세요.")
        return
    try:
        with st.spinner("채점 중…"):
            res = call_grader(build_prompt(s, qkey, answers))
    except Exception as e:
        ss["msg"] = ("error", f"채점 오류가 발생했습니다. 다시 눌러 주세요. ({e})")
        return
    for it in q["items"]:
        r = next((x for x in res if isinstance(x, dict) and x.get("id") == it["id"]), None)
        if r is None:
            continue
        ss.verdicts[akey(s["id"], it["id"])] = {
            "verdict": "정" if str(r.get("verdict", "")).strip() == "정" else "오",
            "feedback": str(r.get("feedback", "")),
            "answer": answers[it["id"]],
        }
    ss.graded.add(f"{s['id']}-{qkey}")

# ---------------------------------------------------------------- UI 조각
def show_verdict(k):
    v = ss.verdicts.get(k)
    if not v:
        return
    stale = v["answer"] != ss.answers.get(k, "").strip()
    if stale:
        st.caption("답을 고쳤어요. 다시 채점하면 새 판정을 받을 수 있어요.")
        return
    (st.success if v["verdict"] == "정" else st.error)(f"**{v['verdict']}**  {v['feedback']}")

def answer_box(set_id, it):
    k = akey(set_id, it["id"])
    widget = st.text_input if it.get("short") else st.text_area
    val = widget(it["label"], value=ss.answers.get(k, ""), key=f"w-{k}", placeholder="여기에 쓰세요")
    ss.answers[k] = val
    show_verdict(k)

def range_box(items):
    for it in items:
        st.markdown(f"**{it['label']}**  \n예시 답안: {it['key']['ex']}")
        for o in it["key"]["ok"]:
            st.markdown(f"- 인정: {o}")
        for n in it["key"]["no"]:
            st.markdown(f"- 불인정: {n}")

def grade_bar(s, qkey):
    c1, c2 = st.columns([1, 2])
    if c1.button("채점하기", key=f"g-{s['id']}-{qkey}", type="primary", width="stretch"):
        grade(s, qkey)
        st.rerun()
    if ss.get("msg"):
        kind, text = ss.pop("msg")
        getattr(st, kind)(text)
    unlocked = f"{s['id']}-{qkey}" in ss.graded
    with c2:
        if unlocked:
            with st.expander("인정 답안 범위 보기"):
                range_box(s[qkey]["items"])
        else:
            st.caption("인정 답안 범위는 채점 후 열립니다.")

def cond(lines, template=None):
    body = "\n".join(f"◦ {ln}" for ln in lines)
    st.markdown(f"**〈조건〉**  \n{body}")
    if template:
        st.markdown("\n".join(f"> {t}" for t in template))

def ads(s):
    st.markdown("**[서·논술형 1~2] 다음 자료를 읽고 물음에 답하시오.**")
    c1, c2 = st.columns(2)
    # 이미지 파일이 준비되지 않았을 경우 에러를 방지하려면 아래 두 줄을 주석(#) 처리하고 텍스트로 대체하세요.
    c1.image(str(IMG_DIR / s["adA"]), caption="(가)", width="stretch")
    c2.image(str(IMG_DIR / s["adB"]), caption="(나)", width="stretch")

def pager(idx):
    c1, c2 = st.columns(2)
    if idx > 0 and c1.button(f"← {PAGES[idx-1]['name']}", width="stretch"):
        ss.page = PAGE_IDS[idx - 1]; st.rerun()
    if idx < len(PAGES) - 1 and c2.button(f"{PAGES[idx+1]['name']} →", type="primary", width="stretch"):
        ss.page = PAGE_IDS[idx + 1]; st.rerun()

# ---------------------------------------------------------------- 문항 페이지
def page_q1(s):
    q = s["q1"]; ads(s)
    st.subheader("서·논술형 1")
    st.write("재현 방식 ㉠~㉡에 들어갈 내용을 쓰시오.")
    st.table({"": ["(가)", "(나)"], "문구": [q["rowA"]["t"], "( ㉠ )"], "이미지": [q["rowA"]["i"], "( ㉡ )"]})
    cond(["광고 문구·이미지와 효과를 한 문장으로 쓸 것."])
    for it in q["items"]: answer_box(s["id"], it)
    grade_bar(s, "q1")

def page_q2(s):
    q = s["q2"]; ads(s)
    st.subheader("서·논술형 2")
    st.write("제작자의 관점과 의도를 서술하시오.")
    cond(["재현된 내용에서 근거를 찾을 것", "문장 틀에 맞출 것"],
         ["관점: ( )을/를 ( )로/으로 본다. 이유는 ( ) 때문이다.", "의도: 사람이 ( )하게 하려 한다."])
    for it in q["items"]: answer_box(s["id"], it)
    grade_bar(s, "q2")

def page_q3(s):
    q = s["q3"]
    st.markdown("**[서·논술형 3] 다음 자료를 읽고 물음에 답하시오.**")
    c1, c2 = st.columns([1, 1.15])
    # 이미지 파일이 준비되지 않았을 경우 에러를 방지하려면 아래 줄을 주석(#) 처리하고 텍스트로 대체하세요.
    c1.image(str(IMG_DIR / s["adC"]), caption="[광고]", width="stretch")
    with c2:
        st.markdown("**[학생의 사고 과정]**")
        st.markdown(q["buy"]); st.markdown(q["think1"]); st.markdown(q["think2"])
    st.markdown("**(1) ㉠, ㉡에 적절한 표현을 쓰시오.**")
    answer_box(s["id"], q["items"][0]); answer_box(s["id"], q["items"][1])
    st.markdown("**(2) 제작자 의도를 서술하시오.**")
    cond(["근거를 포함할 것", "문장 틀에 맞출 것"], ["의도: 사람이 ( )하게 하려 한다. 이유는 ( ) 때문이다."])
    answer_box(s["id"], q["items"][2])
    grade_bar(s, "q3")

# ---------------------------------------------------------------- 결과 페이지
def collect():
    out = []
    for si, s in enumerate(SETS, 1):
        for qi, qk in enumerate(["q1", "q2", "q3"], 1):
            rows = []
            for it in s[qk]["items"]:
                k = akey(s["id"], it["id"]); a = ss.answers.get(k, "").strip(); v = ss.verdicts.get(k)
                if not a: status = "미작성"
                elif v is None: status = "미채점"
                elif v["answer"] != a: status = "수정 후 미채점"
                else: status = v["verdict"]
                rows.append({"답란": it["label"], "내 답안": a or "—", "판정": status, "피드백": v["feedback"] if v and status in ("정", "오") else ""})
            out.append({"key": f"{s['id']}-{qk}", "name": f"{si}번 세트 – 서·논술형 {qi}", "rows": rows})
    return out

def result_text(data):
    lines = [f"학번·이름: {ss.student}", f"제출 시각: {dt.datetime.now():%Y-%m-%d %H:%M}", ""]
    for d in data:
        lines.append(f"[{d['name']}]")
        for r in d["rows"]:
            fb = f" / {r['피드백']}" if r["피드백"] else ""
            lines.append(f"{r['답란']}: {r['내 답안']} → {r['판정']}{fb}")
        lines.append("")
    return "\n".join(lines)

def submit_to_sheet(data):
    import gspread
    from google.oauth2.service_account import Credentials
    info = dict(secret("gcp_service_account"))
    creds = Credentials.from_service_account_info(info, scopes=["https://www.googleapis.com/auth/spreadsheets"])
    sh = gspread.authorize(creds).open_by_url(secret("SHEET_URL"))
    ws = sh.sheet1
    header = ["제출시각", "학번·이름"] + [f"{d['name']}" for d in data] + ["정 개수", "작성 개수"]
    if not ws.row_values(1): ws.append_row(header)
    cells = []
    ok = done = 0
    for d in data:
        cells.append("\n".join(f"{r['답란']}: {r['내 답안']} → {r['판정']}" for r in d["rows"]))
        for r in d["rows"]:
            if r["내 답안"] != "—": done += 1
            if r["판정"] == "정": ok += 1
    ws.append_row([f"{dt.datetime.now():%Y-%m-%d %H:%M:%S}", ss.student] + cells + [ok, done])

def page_result():
    c1, c2 = st.columns([3, 1])
    c1.subheader("결과 정리")
    if c2.button("다시 풀기", type="secondary", width="stretch"): ss["confirm_reset"] = True
    if ss.get("confirm_reset"):
        st.warning("모두 지우고 다시 풀까요?")
        a, b = st.columns(2)
        if a.button("네, 다시 풀게요", type="primary", width="stretch"):
            for k in list(ss.keys()):
                if k.startswith("w-"): del ss[k]
            ss.answers = {}; ss.verdicts = {}; ss.graded = set(); ss.confirm_reset = False
            ss.page = PAGE_IDS[0]; st.rerun()
        if b.button("아니요", width="stretch"):
            ss.confirm_reset = False; st.rerun()
            
    ss.student = st.text_input("학번·이름", value=ss.student, placeholder="예: 20415 홍길동")
    data = collect()
    st.markdown(f"**답란 {sum(len(d['rows']) for d in data)}개 중 작성 {sum(1 for d in data for r in d['rows'] if r['내 답안'] != '—')}개, 정 {sum(1 for d in data for r in d['rows'] if r['판정'] == '정')}개**")
    for i, d in enumerate(data):
        h1, h2 = st.columns([3, 1])
        h1.markdown(f"**{d['name']}**")
        if h2.button("이 문항으로", key=f"go-{d['key']}", width="stretch"):
            ss.page = d["key"]; st.rerun()
        st.table(d["rows"])
    txt = result_text(data)
    c1, c2 = st.columns(2)
    sheet_ok = secret("gcp_service_account") is not None and secret("SHEET_URL") is not None
    if c1.button("구글 시트로 제출", type="primary", width="stretch", disabled=not sheet_ok):
        if not ss.student.strip(): st.warning("학번·이름을 먼저 써 주세요.")
        else:
            try:
                submit_to_sheet(data); st.success("제출 완료!")
            except Exception as e:
                st.error(f"제출 실패: {e}")
    if not sheet_ok: c1.caption("구글 시트 미설정 상태입니다.")
    c2.download_button("결과 내려받기(.txt)", data=txt, file_name=f"결과_{ss.student or '학생'}.txt", mime="text/plain", width="stretch")

# ---------------------------------------------------------------- 메인
st.title("서논술형 답안 연습")
st.caption("광고·홍보물의 재현과 관점 — 1회 시험 대비")

choice = st.radio("문항", [p["tab"] for p in PAGES], horizontal=True, label_visibility="collapsed", index=PAGE_IDS.index(ss.page))
sel = next(p for p in PAGES if p["tab"] == choice)
if sel["id"] != ss.page: ss.page = sel["id"]
idx = PAGE_IDS.index(ss.page)
page = PAGES[idx]

if page["id"] == "result": page_result()
else:
    {"q1": page_q1, "q2": page_q2, "q3": page_q3}[page["qkey"]](page["set"])
st.divider()
pager(idx)
