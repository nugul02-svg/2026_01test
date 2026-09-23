# -*- coding: utf-8 -*-
import datetime as dt
from pathlib import Path
import streamlit as st

# 데이터 세트 (1~3회차)
SETS = [
    {
        "id": "set1",
        "adA": "set1_a.png", "adB": "set1_b.png", "adC": "set1_c.png",
        "adText": {
            "A": "(가) 보행 중 스마트폰 사용 위험 경고 광고: '고개를 들면 5초가 보입니다'",
            "B": "(나) 보행 중 스마트폰 사용 위험 경고 광고: '운전자는 당신이 자기를 봤다고 생각합니다'",
            "C": "스마트워치 상업 광고: '1분도 놓치지 않는 하루'"
        },
        "q1": {
            "rowA": {"t": "'고개를 드는 것'을 '5초가 보이는 것'과 짝지어 위험을 알아챌 시간이 생긴다는 것을 보여 줌.", "i": "신호등을 넣어 학생이 보지 못하는 남은 시간을 보여 줌."},
            "items": [
                {"id": "q1-1", "label": "(나) 문구 ( ㉠ )", "short": False, "key": {"ex": "'운전자는 당신이 자기를 봤다고 생각합니다'를 넣어, 인식의 차이로 인한 위험을 보여 줌.", "ok": ["인식의 차이 위험성", "운전자의 착각"]}},
                {"id": "q1-2", "label": "(나) 이미지 ( ㉡ )", "short": False, "key": {"ex": "운전자 시선의 학생을 보여 주어 아찔함과 위험성을 보여 줌.", "ok": ["시각적 위험성", "위험하게 보이는 모습"]}}
            ]
        },
        "q2": {
            "items": [
                {"id": "q2-1", "label": "제작자의 관점과 의도", "short": False, "key": {"ex": "관점은 '스마트폰 보행'을 '위험한 행동'으로 본다. 이유는 '아찔한 횡단보도 이미지' 때문이다. 의도는 '보행 중 스마트폰을 보지 않게' 하려 한다.", "ok": ["스마트폰 보행=위험", "스마트폰 사용 중지 의도"]}}
            ]
        },
        "q3": {
            "buy": "새 시계를 사야 하는데. 이 광고를 살펴볼까?",
            "think1": "이 문구를 종합해 보면 제작자는 시간을 ( ㉠ )로/으로 보는 관점을 지닌 것 같아.",
            "think2": "수정된 이미지는 벤치에 앉아 쉬는 학생 모습으로 바꾸겠어. 이렇게 바꾸면 시간을 ( ㉡ )로/으로 보는 것으로 바뀌지.",
            "items": [
                {"id": "q3-1", "label": "㉠", "short": True, "key": {"ex": "빈틈없이 관리하고 쪼개어 써야 할 대상", "ok": ["아껴 써야 하는 것", "효율성"]}},
                {"id": "q3-2", "label": "㉡", "short": True, "key": {"ex": "휴식을 취하며 여유를 누릴 수 있는 것", "ok": ["여유", "쉬는 것"]}},
                {"id": "q3-3", "label": "(2) 원본 광고의 제작자 의도", "short": False, "key": {"ex": "의도는 '스마트워치를 구매하여 시간을 철저하게 관리하게' 하려 한다. 이유는 '뛰어가는 학생' 이미지 때문이다.", "ok": ["시계를 사서 바쁘게 살게 하려 한다."]}}
            ]
        }
    },
    {
        "id": "set2",
        "adA": "set2_a.png", "adB": "set2_b.png", "adC": "set2_c.png",
        "adText": {
            "A": "(가) 잔반 줄이기 광고: '남긴 밥 한 숟갈'과 '하루 300kg'",
            "B": "(나) 잔반 줄이기 광고: '이 밥을 만든 손을 기억해 주세요'",
            "C": "운동화 상업 광고: '신는 순간, 시선이 달라집니다'"
        },
        "q1": {
            "rowA": {"t": "'한 숟갈'을 '300kg'과 나란히 놓아 모이면 큰 양이 됨을 보여 줌.", "i": "밥을 산처럼 쌓아 남긴 양의 크기를 보여 줌."},
            "items": [
                {"id": "q1-1", "label": "(나) 문구 ( ㉠ )", "short": False, "key": {"ex": "'이 밥을 만든 손을 기억해 주세요'를 넣어 음식에 담긴 노고를 보여 줌.", "ok": ["정성과 노력", "만든 사람의 노고"]}},
                {"id": "q1-2", "label": "(나) 이미지 ( ㉡ )", "short": False, "key": {"ex": "농부, 조리사, 학생의 손을 배치하여 감사의 필요성을 보여 줌.", "ok": ["밥이 만들어지는 과정", "협력과 노력"]}}
            ]
        },
        "q2": {
            "items": [
                {"id": "q2-1", "label": "제작자의 관점과 의도", "short": False, "key": {"ex": "관점은 '잔반'을 '수많은 사람의 노고를 버리는 행위'로 본다. 이유는 '거친 손 이미지' 때문이다. 의도는 '음식을 다 먹게' 하려 한다.", "ok": ["잔반=낭비", "급식 남기지 않기"]}}
            ]
        },
        "q3": {
            "buy": "운동화를 새로 사야 하는데, 이 광고를 살펴볼까?",
            "think1": "이 문구를 종합해 보면 제작자는 운동화를 ( ㉠ )로/으로 보는 관점을 지닌 것 같아.",
            "think2": "수정된 이미지는 공을 쫓아 뛰는 발 모습으로 바꾸겠어. 이러면 운동화를 ( ㉡ )로/으로 보는 것으로 바뀌지.",
            "items": [
                {"id": "q3-1", "label": "㉠", "short": True, "key": {"ex": "타인의 시선을 끄는 과시용 도구", "ok": ["과시 수단", "신분 상승 도구"]}},
                {"id": "q3-2", "label": "㉡", "short": True, "key": {"ex": "발을 편안하게 보호하는 실용적 도구", "ok": ["실용적인 물건", "편안한 것"]}},
                {"id": "q3-3", "label": "(2) 원본 광고의 제작자 의도", "short": False, "key": {"ex": "의도는 '남들의 시선을 끌기 위해 운동화를 구매하게' 하려 한다. 이유는 '부러워하며 올려다보는 이미지' 때문이다.", "ok": ["뽐내게 하려 한다", "멋져 보이고 싶어서 사게 한다"]}}
            ]
        }
    },
    {
        "id": "set3",
        "adA": "set3_a.png", "adB": "set3_b.png", "adC": "set3_c.png",
        "adText": {
            "A": "(가) 층간소음 방지 광고: 윗층 아이와 아래층 학생을 짓누르는 발자국 그림자.",
            "B": "(나) 층간소음 방지 광고: '슬리퍼 한 켤레면 됩니다'",
            "C": "무선 이어폰 상업 광고: '세상을 끄고, 나만 남기다'"
        },
        "q1": {
            "rowA": {"t": "'당신의 발소리'를 '천장을 흔드는 것'이라 하여 큰 소리가 됨을 보여 줌.", "i": "발자국을 그림자로 만들어 소리가 누르는 무게가 됨을 보여 줌."},
            "items": [
                {"id": "q1-1", "label": "(나) 문구 ( ㉠ )", "short": False, "key": {"ex": "'슬리퍼 한 켤레면 됩니다'라고 하여 작은 실천으로 해결될 수 있음을 보여 줌.", "ok": ["작은 배려와 실천", "간단한 해결책"]}},
                {"id": "q1-2", "label": "(나) 이미지 ( ㉡ )", "short": False, "key": {"ex": "슬리퍼 안으로 들어가는 발을 배치하여 즉각적인 행동을 보여 줌.", "ok": ["구체적인 실천 방안", "배려의 시각화"]}}
            ]
        },
        "q2": {
            "items": [
                {"id": "q2-1", "label": "제작자의 관점과 의도", "short": False, "key": {"ex": "관점은 '층간소음'을 '고통을 주는 폭력'으로 본다. 이유는 '거대한 발자국 그림자' 때문이다. 의도는 '실내에서 조용히 걷게' 하려 한다.", "ok": ["층간소음=고통", "조용히 걷기 유도"]}}
            ]
        },
        "q3": {
            "buy": "이어폰을 사야 하는데, 이 광고를 살펴볼까?",
            "think1": "이 문구를 종합해 보면 제작자는 이어폰을 ( ㉠ )로/으로 보는 관점을 지닌 것 같아.",
            "think2": "수정된 이미지는 두 학생이 이어폰을 나눠 끼고 웃는 모습으로 바꾸겠어. 이러면 이어폰을 ( ㉡ )로/으로 보는 것으로 바뀌지.",
            "items": [
                {"id": "q3-1", "label": "㉠", "short": True, "key": {"ex": "외부와 단절시키고 혼자만의 세계로 도피하게 하는 수단", "ok": ["단절", "고립"]}},
                {"id": "q3-2", "label": "㉡", "short": True, "key": {"ex": "타인과 감정을 공유하고 연결해 주는 매개체", "ok": ["소통의 도구", "연결고리"]}},
                {"id": "q3-3", "label": "(2) 원본 광고의 제작자 의도", "short": False, "key": {"ex": "의도는 '소음을 차단하고 혼자만의 시간을 갖기 위해 구매하게' 하려 한다. 이유는 '배경을 흐리게 처리한 이미지' 때문이다.", "ok": ["혼자 음악을 듣게 하려 한다"]}}
            ]
        }
    }
]

HERE = Path(__file__).parent
IMG_DIR = HERE / "images"

st.set_page_config(page_title="서논술형 답안 연습", page_icon="✍️", layout="centered")

PAGES = []
for si, s in enumerate(SETS, 1):
    for qi, qk in enumerate(["q1", "q2", "q3"], 1):
        PAGES.append({"id": f"{s['id']}-{qk}", "set": s, "qkey": qk, "tab": f"{si}-{qi}", "name": f"{si}번 세트 – 서·논술형 {qi}"})
PAGES.append({"id": "result", "tab": "결과 제출", "name": "결과 제출하기"})
PAGE_IDS = [p["id"] for p in PAGES]

ss = st.session_state
ss.setdefault("page", PAGE_IDS[0])
ss.setdefault("answers", {})
ss.setdefault("student", "")

def akey(set_id, item_id):
    return f"{set_id}-{item_id}"

def answer_box(set_id, it):
    k = akey(set_id, it["id"])
    widget = st.text_input if it.get("short") else st.text_area
    val = widget(it["label"], value=ss.answers.get(k, ""), key=f"w-{k}", placeholder="여기에 답안을 작성하세요")
    ss.answers[k] = val
    
    if val.strip():
        with st.expander("✅ 예시 답안 및 인정 기준 확인하기"):
            st.markdown(f"**예시 답안:** {it['key']['ex']}")
            st.markdown(f"**인정 기준:** {', '.join(it['key']['ok'])}")

def cond(lines, template=None):
    body = "\n".join(f"◦ {ln}" for ln in lines)
    st.markdown(f"**〈조건〉**  \n{body}")
    if template:
        st.markdown("\n".join(f"> {t}" for t in template))

def ads(s):
    st.markdown("**[서·논술형 1~2] 다음 자료를 읽고 물음에 답하시오.**")
    c1, c2 = st.columns(2)
    try: c1.image(str(IMG_DIR / s["adA"]), caption="(가)", width="stretch")
    except: c1.info("(가) 광고 이미지 자리")
    try: c2.image(str(IMG_DIR / s["adB"]), caption="(나)", width="stretch")
    except: c2.info("(나) 광고 이미지 자리")

def pager(idx):
    c1, c2 = st.columns(2)
    if idx > 0 and c1.button(f"← {PAGES[idx-1]['name']}", width="stretch"):
        ss.page = PAGE_IDS[idx - 1]; st.rerun()
    if idx < len(PAGES) - 1 and c2.button(f"{PAGES[idx+1]['name']} →", type="primary", width="stretch"):
        ss.page = PAGE_IDS[idx + 1]; st.rerun()

def page_q1(s):
    q = s["q1"]; ads(s)
    st.subheader("서·논술형 1")
    st.write("재현 방식 ㉠~㉡에 들어갈 내용을 쓰시오.")
    st.table({"": ["(가)", "(나)"], "문구": [q["rowA"]["t"], "( ㉠ )"], "이미지": [q["rowA"]["i"], "( ㉡ )"]})
    cond(["광고 문구·이미지와 효과를 한 문장으로 쓸 것."])
    for it in q["items"]: answer_box(s["id"], it)

def page_q2(s):
    q = s["q2"]; ads(s)
    st.subheader("서·논술형 2")
    st.write("제작자의 관점과 의도를 서술하시오.")
    cond(["재현된 내용에서 근거를 찾을 것", "문장 틀에 맞출 것"],
         ["관점: ( )을/를 ( )로/으로 본다. 이유는 ( ) 때문이다.", "의도: 사람이 ( )하게 하려 한다."])
    for it in q["items"]: answer_box(s["id"], it)

def page_q3(s):
    q = s["q3"]
    st.markdown("**[서·논술형 3] 다음 자료를 읽고 물음에 답하시오.**")
    c1, c2 = st.columns([1, 1.15])
    try: c1.image(str(IMG_DIR / s["adC"]), caption="[광고]", width="stretch")
    except: c1.info("[광고] 이미지 자리")
    with c2:
        st.markdown("**[학생의 사고 과정]**")
        st.markdown(q["buy"]); st.markdown(q["think1"]); st.markdown(q["think2"])
    st.markdown("**(1) ㉠, ㉡에 적절한 표현을 쓰시오.**")
    answer_box(s["id"], q["items"][0]); answer_box(s["id"], q["items"][1])
    st.markdown("**(2) 제작자 의도를 서술하시오.**")
    cond(["근거를 포함할 것", "문장 틀에 맞출 것"], ["의도: 사람이 ( )하게 하려 한다. 이유는 ( ) 때문이다."])
    answer_box(s["id"], q["items"][2])

def submit_to_sheet(student_name):
    import gspread
    from google.oauth2.service_account import Credentials
    
    info = dict(st.secrets["gcp_service_account"])
    creds = Credentials.from_service_account_info(info, scopes=["https://www.googleapis.com/auth/spreadsheets"])
    sh = gspread.authorize(creds).open_by_url(st.secrets["SHEET_URL"])
    ws = sh.sheet1
    
    # 헤더 작성 (첫 줄이 비어있을 경우)
    if not ws.row_values(1):
        headers = ["제출시각", "학번·이름"]
        for s in SETS:
            for qk in ["q1", "q2", "q3"]:
                for it in s[qk]["items"]:
                    headers.append(f"[{s['id']}-{qk}] {it['label']}")
        ws.append_row(headers)
    
    # 학생 데이터 행 작성
    row_data = [f"{dt.datetime.now():%Y-%m-%d %H:%M:%S}", student_name]
    for s in SETS:
        for qk in ["q1", "q2", "q3"]:
            for it in s[qk]["items"]:
                k = akey(s["id"], it["id"])
                row_data.append(ss.answers.get(k, "미작성"))
    
    ws.append_row(row_data)

def page_result():
    st.subheader("결과 제출하기")
    st.caption("작성한 모든 답안을 선생님의 구글 시트로 제출합니다.")
    
    ss.student = st.text_input("학번·이름 (필수)", value=ss.student, placeholder="예: 30215 홍길동")
    
    sheet_ok = "gcp_service_account" in st.secrets and "SHEET_URL" in st.secrets
    
    if st.button("🚀 구글 시트로 제출하기", type="primary", width="stretch", disabled=not sheet_ok):
        if not ss.student.strip():
            st.warning("학번과 이름을 먼저 적어주세요.")
        else:
            try:
                with st.spinner("제출 중입니다..."):
                    submit_to_sheet(ss.student)
                st.success("✅ 제출이 완료되었습니다! 수고하셨습니다.")
            except Exception as e:
                st.error(f"제출에 실패했습니다. 선생님께 문의해 주세요. (에러: {e})")
                
    if not sheet_ok:
        st.error("구글 시트 연동 설정(Secrets)이 완료되지 않았습니다.")

st.title("서논술형 답안 연습")
st.caption("광고·홍보물의 재현과 관점 — 1회 시험 대비 모의고사")

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
