# -*- coding: utf-8 -*-
"""서논술형 답안 연습 — 광고·홍보물의 재현과 관점 (Streamlit)

실행:  streamlit run app.py
비밀값(.streamlit/secrets.toml 또는 Streamlit Cloud의 Secrets):
  ANTHROPIC_API_KEY = "sk-ant-..."
  MODEL = "claude-sonnet-4-6"          # 생략 가능
  SHEET_URL = "https://docs.google.com/spreadsheets/d/..."   # 구글 시트 연동 시
  [gcp_service_account]                 # 구글 시트 연동 시 (서비스 계정 JSON 내용)
  type = "service_account"
  ...
"""
import json
import re
import datetime as dt
from pathlib import Path

import streamlit as st

from data import SETS

HERE = Path(__file__).parent
IMG_DIR = HERE / "images"

st.set_page_config(page_title="서논술형 답안 연습", page_icon="✍️", layout="centered")

# ---------------------------------------------------------------- 페이지 목록
PAGES = []
for si, s in enumerate(SETS, 1):
    for qi, qk in enumerate(["q1", "q2", "q3"], 1):
        PAGES.append({"id": f"{s['id']}-{qk}", "set": s, "qkey": qk,
                      "tab": f"{si}-{qi}", "name": f"{si}번 세트 – 서·논술형 {qi}"})
PAGES.append({"id": "result", "tab": "결과", "name": "결과 정리"})
PAGE_IDS = [p["id"] for p in PAGES]

ss = st.session_state
ss.setdefault("page", PAGE_IDS[0])
ss.setdefault("answers", {})    # key -> text
ss.setdefault("verdicts", {})   # key -> {"verdict","feedback","answer"}
ss.setdefault("graded", set())  # "s1-q1" ...
ss.setdefault("student", "")

def akey(set_id, item_id):
    return f"{set_id}-{item_id}"

# ---------------------------------------------------------------- 채점
GRADE_RULES = """[판정 원칙]
1. 표현이 예시 답안과 달라도 인정 기준의 뜻을 담고 있으면 '정'. 맞춤법·문장 다듬기는 판정에 넣지 않는다.
2. 재현 방법(시점 전환, 크게 배치 등)을 명시하지 않아도, 그 문구·이미지가 드러내는 광고의 '뜻'이 있으면 '정'. 반대로 인상·감상만 있고 뜻이 없으면 '오'.
3. 근거(이유)는 문구나 이미지 중 하나를 구체적으로 들고, 그 재현으로 인한 효과(그것이 무엇을 보여 주는지)가 있어서 관점·의도로 이어져야 한다. 인용만 있고 효과가 없거나, 광고의 주장 자체를 이유로 쓰면 '오'.
4. 점수나 부분점수를 절대 언급하지 않는다.
5. feedback은 학생에게 말하듯 한 문장. '오'일 때는 무엇이 빠졌거나 어긋났는지 짚되 정답 문장을 그대로 알려 주지 않는다. '정'일 때는 잘한 점을 한 문장으로.
6. 답이 비어 있거나 무의미한 문자열이면 '오'로 하고 feedback에 "답을 써 주세요."라고 쓴다."""

def build_prompt(s, qkey, answers):
    q = s[qkey]
    if qkey == "q1":
        qdesc = ("[문항] 서·논술형 1. 두 광고의 재현 방식을 표로 정리하였다. (나) 광고의 문구(㉠)와 이미지(㉡)에 대해, "
                 "광고의 문구·이미지와 그로 인한 효과를 한 문장으로 쓴다. 참고로 (가)에 대한 모범 기술은 다음과 같다. "
                 f"문구: {q['rowA']['t']} / 이미지: {q['rowA']['i']}")
        ad = s["adText"]["A"] + "\n" + s["adText"]["B"]
    elif qkey == "q2":
        qdesc = ("[문항] 서·논술형 2. 두 광고에 담긴 제작자의 관점과 의도를 서술한다. 문장 틀: 관점은 \"(　)을/를 (　)로/으로 본다. "
                 "그렇게 생각한 이유는 (　) 때문이다.\", 의도는 \"제작자는 광고를 본 사람이 (　)하게 하려 한다.\" "
                 "관점의 둘째 괄호에는 사물 이름이 아니라 그 사물이 뜻하는 성질·가치를 써야 한다.")
        ad = s["adText"]["A"] + "\n" + s["adText"]["B"]
    else:
        qdesc = (f"[문항] 서·논술형 3. 광고를 비판적으로 읽는 학생의 사고 과정이다. \"{q['think1']}\" \"{q['think2']}\" "
                 f"㉠·㉡에는 광고 속 {q['obj']}을/를 무엇으로 보는지(성질·가치)를 쓴다. (2)는 수정 전 광고에 담긴 제작자의 의도를 "
                 "문장 틀 \"광고를 본 사람이 (　)하게 하려 한다. 그렇게 생각한 이유는 (　) 때문이다.\"에 맞추어 쓰되, "
                 "광고에 재현된 내용에서 찾은 근거를 포함한다.")
        ad = s["adText"]["C"]
    keys = "\n".join(
        f"- {it['id']} ({it['label']})\n  예시 답안: {it['key']['ex']}\n  인정 기준: {' / '.join(it['key']['ok'])}\n  불인정: {' / '.join(it['key']['no'])}"
        for it in q["items"])
    ans = "\n".join(f"- {it['id']}: {json.dumps(answers[it['id']], ensure_ascii=False)}" for it in q["items"])
    return (f"당신은 중학교 2학년 국어 서·논술형 답안을 채점하는 교사입니다. 아래 광고 설명, 문항, 인정답안 기준을 읽고 "
            f"학생 답안을 각각 '정' 또는 '오'로 판정하세요.\n\n[광고 설명]\n{ad}\n\n{qdesc}\n\n[인정답안 기준]\n{keys}\n\n"
            f"{GRADE_RULES}\n\n[학생 답안]\n{ans}\n\n"
            "반드시 다음 JSON 배열만 출력하세요(다른 말 없이): [{\"id\":\"q1a\",\"verdict\":\"정\",\"feedback\":\"...\"}]")

def secret(name, default=None):
    try:
        return st.secrets.get(name, default)
    except Exception:  # noqa: BLE001  (secrets.toml 없음)
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
        raise RuntimeError("ANTHROPIC_API_KEY가 설정되지 않았습니다.")
    model = secret("MODEL", "claude-sonnet-4-6")
    msg = client.messages.create(model=model, max_tokens=1200,
                                 messages=[{"role": "user", "content": prompt}])
    text = "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")
    text = re.sub(r"```json|```", "", text).strip()
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
    except Exception as e:  # noqa: BLE001
        ss["msg"] = ("error", f"채점 중 문제가 생겼어요. 다시 눌러 주세요. ({e})")
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
            st.caption("인정 답안 범위는 답을 쓰고 채점한 뒤 열 수 있어요.")

def cond(lines, template=None):
    body = "\n".join(f"◦ {ln}" for ln in lines)
    st.markdown(f"**〈조건〉**  \n{body}")
    if template:
        st.markdown("\n".join(f"> {t}" for t in template))

def ads(s):
    st.markdown("**[서·논술형 1~2] 다음 자료를 읽고 물음에 답하시오.**")
    c1, c2 = st.columns(2)
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
    st.write("두 광고의 재현 방식을 표로 정리하였다. ㉠~㉡에 들어갈 내용을 〈조건〉에 맞게 쓰시오.")
    st.table({"": ["(가)", "(나)"], "문구": [q["rowA"]["t"], "( ㉠ )"], "이미지": [q["rowA"]["i"], "( ㉡ )"]})
    cond(["광고의 문구·이미지와 그로 인한 효과를 한 문장으로 쓸 것."])
    for it in q["items"]:
        answer_box(s["id"], it)
    grade_bar(s, "q1")

def page_q2(s):
    q = s["q2"]; ads(s)
    st.subheader("서·논술형 2")
    st.write("두 광고에 담긴 제작자의 관점과 의도를 〈조건〉에 맞게 서술하시오.")
    cond(["관점의 경우, 광고에 재현된 내용에서 찾은 근거를 포함하여 기술할 것", "아래 문장 틀에 맞추어 쓸 것."],
         ["- 관점: (　　)을/를 (　　)로/으로 본다. 그렇게 생각한 이유는 (　　) 때문이다.",
          "- 의도: 제작자는 광고를 본 사람이 (　　)하게 하려 한다."])
    for it in q["items"]:
        answer_box(s["id"], it)
    grade_bar(s, "q2")

def page_q3(s):
    q = s["q3"]
    st.markdown("**[서·논술형 3] 다음 자료를 읽고 물음에 답하시오.**")
    st.subheader("서·논술형 3")
    st.write("다음은 광고를 비판적으로 읽는 학생의 사고 과정이다.")
    c1, c2 = st.columns([1, 1.15])
    c1.image(str(IMG_DIR / s["adC"]), caption="[광고]", width="stretch")
    with c2:
        st.markdown("**[학생의 사고 과정]**")
        st.markdown(q["buy"]); st.markdown(q["think1"]); st.markdown(q["think2"])
    st.markdown("**(1) ㉠, ㉡에 들어가기에 적절한 표현을 쓰시오.**")
    answer_box(s["id"], q["items"][0]); answer_box(s["id"], q["items"][1])
    st.markdown("**(2) 위 광고에 담긴 제작자의 의도를 재현 방법을 근거로 들어 서술하시오. (단, ‘위 광고’는 수정 전 광고를 의미한다.)**")
    cond(["광고에 재현된 내용에서 찾은 근거를 포함하여 기술할 것", "아래 문장 틀에 맞추어 쓸 것."],
         ["- 의도: 광고를 본 사람이 (　　)하게 하려 한다. 그렇게 생각한 이유는 (　　) 때문이다."])
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
                rows.append({"답란": it["label"], "내 답안": a or "—", "판정": status,
                             "피드백": v["feedback"] if v and status in ("정", "오") else ""})
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
    """구글 시트에 한 줄 추가. secrets에 gcp_service_account와 SHEET_URL이 있어야 함."""
    import gspread
    from google.oauth2.service_account import Credentials
    info = dict(secret("gcp_service_account"))
    creds = Credentials.from_service_account_info(
        info, scopes=["https://www.googleapis.com/auth/spreadsheets"])
    sh = gspread.authorize(creds).open_by_url(secret("SHEET_URL"))
    ws = sh.sheet1
    header = ["제출시각", "학번·이름"] + [f"{d['name']}" for d in data] + ["정 개수", "작성 개수"]
    if not ws.row_values(1):
        ws.append_row(header)
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
    if c2.button("다시 풀기", type="secondary", width="stretch"):
        ss["confirm_reset"] = True
    if ss.get("confirm_reset"):
        st.warning("답안과 채점 결과를 모두 지우고 처음부터 다시 풀까요?")
        a, b = st.columns(2)
        if a.button("네, 지우고 다시 풀게요", type="primary", width="stretch"):
            for k in list(ss.keys()):
                if k.startswith("w-"):
                    del ss[k]
            ss.answers = {}; ss.verdicts = {}; ss.graded = set(); ss.confirm_reset = False
            ss.page = PAGE_IDS[0]; st.rerun()
        if b.button("아니요", width="stretch"):
            ss.confirm_reset = False; st.rerun()
    st.caption("지금까지 쓴 답안과 채점 결과를 모아 보여 줍니다.")
    ss.student = st.text_input("학번·이름", value=ss.student, placeholder="예: 20415 홍길동")
    data = collect()
    total = sum(len(d["rows"]) for d in data)
    done = sum(1 for d in data for r in d["rows"] if r["내 답안"] != "—")
    ok = sum(1 for d in data for r in d["rows"] if r["판정"] == "정")
    st.markdown(f"**답란 {total}개 중 작성 {done}개, 정 {ok}개**")
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
        if not ss.student.strip():
            st.warning("학번·이름을 먼저 써 주세요.")
        else:
            try:
                submit_to_sheet(data); st.success("제출했어요. 선생님 시트에 기록되었습니다.")
            except Exception as e:  # noqa: BLE001
                st.error(f"제출에 실패했어요. 선생님께 알려 주세요. ({e})")
    if not sheet_ok:
        c1.caption("구글 시트 연동이 설정되지 않았어요. 아래 '결과 내려받기'를 쓰세요.")
    c2.download_button("결과 내려받기(.txt)", data=txt, file_name=f"결과_{ss.student or '학생'}.txt",
                       mime="text/plain", width="stretch")

# ---------------------------------------------------------------- 메인
st.title("서논술형 답안 연습")
st.caption("광고·홍보물의 재현과 관점 — 1회 시험 대비. 문항마다 답을 쓰고 ‘채점하기’를 누르면 정·오만 알려 줍니다.")

choice = st.radio("문항", [p["tab"] for p in PAGES], horizontal=True, label_visibility="collapsed",
                  index=PAGE_IDS.index(ss.page))
sel = next(p for p in PAGES if p["tab"] == choice)
if sel["id"] != ss.page:
    ss.page = sel["id"]
idx = PAGE_IDS.index(ss.page)
page = PAGES[idx]

if page["id"] == "result":
    page_result()
else:
    st.markdown(f"### {page['name']}")
    {"q1": page_q1, "q2": page_q2, "q3": page_q3}[page["qkey"]](page["set"])
st.divider()
pager(idx)
st.caption("답안은 이 브라우저 탭을 닫기 전까지 유지됩니다. 인정 답안 범위는 채점한 뒤에 열 수 있습니다.")
