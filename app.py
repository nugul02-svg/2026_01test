# -*- coding: utf-8 -*-
import datetime as dt
from pathlib import Path
import streamlit as st

# ---------------------------------------------------------------- 데이터 세트
SETS = [
    {
        "id": "set1",
        "adA": "set1_a.png", "adB": "set1_b.png", "adC": "set1_c.png",
        "adText": {
            "A": "(가) 보행 중 스마트폰 사용 위험 경고 광고",
            "B": "(나) 보행 중 스마트폰 사용 위험 경고 광고",
            "C": "스마트워치 상업 광고"
        },
        "q1": {
            "rowA": {"t": "'고개를 드는 것'을 '5초가 보이는 것'과 짝지어 위험을 알아챌 시간이 생긴다는 것을 보여 줌.", "i": "신호등을 넣어 학생이 보지 못하는 남은 시간을 보여 줌."},
            "items": [
                {"id": "q1-1", "label": "(나) 문구 ( ㉠ )", "short": False, "key": {"ex": "'운전자는 당신이 자기를 봤다고 생각합니다'를 넣어, 운전자와 보행자의 서로 다른 인식 차이로 인한 위험성을 보여 줌."}},
                {"id": "q1-2", "label": "(나) 이미지 ( ㉡ )", "short": False, "key": {"ex": "운전자의 시선에서 스마트폰을 보며 걷는 학생을 보여 주어, 운전자 입장에서 느끼는 상황의 아찔함과 위험성을 보여 줌."}}
            ]
        },
        "q2": {
            "items": [
                {"id": "q2-1", "label": "제작자의 관점과 의도", "short": False, "key": {"ex": "관점: 광고는 스마트폰 보행을 생명을 위협하는 위험한 행동으로 본다. 왜냐하면 운전자 시점의 아찔한 횡단보도 이미지 때문이다.\n의도: 제작자는 광고를 본 사람이 보행 중 스마트폰을 보지 않게 하려 한다. 왜냐하면 사고가 날 수 있기 때문이다."}}
            ]
        },
        "q3": {
            "buy": "새 시계를 사야 하는데. 이 광고를 살펴볼까?",
            "think1": "뛰어가는 학생과 시계 화면의 알림들이 그려진 이미지와 '1분도 놓치지 않는 하루.'라는 문구를 종합해 보면 제작자는 시간을 ( ㉠ )로/으로 보는 관점을 지닌 것 같아.",
            "think2": "하지만 시간이 정말 그렇기만 한 것인가? 나만 하더라도 그렇게 살지 않는데. 나라면 이 광고를 이렇게 바꾸겠어. 수정된 이미지는 벤치에 앉아 쉬는 학생의 손목에서 시계 화면이 '쉬는 시간 15분. 잘 쉬고 있어요.'라고 알려주는 모습으로, 문구는 '쉬는 1분도 충실히 챙기는 하루.'로. 이렇게 바꾸면 광고에 담긴 관점이 시간을 ( ㉡ )로/으로 보는 것으로 바뀌게 되니 실제 학생들의 하루를 더 정확하게 반영했다고 볼 수 있지.",
            "items": [
                {"id": "q3-1", "label": "㉠", "short": True, "key": {"ex": "빈틈없이 관리하고 쪼개어 써야 할 대상"}},
                {"id": "q3-2", "label": "㉡", "short": True, "key": {"ex": "휴식을 취하며 여유를 누릴 수 있는 것"}},
                {"id": "q3-3", "label": "(2) 원본 광고의 제작자 의도", "short": False, "key": {"ex": "의도: 제작자는 광고를 본 사람이 스마트워치를 구매하여 시간을 철저하게 관리하게 하려 한다. 왜냐하면 뛰어가는 학생과 1분도 놓치지 않겠다는 문구 때문이다."}}
            ]
        }
    },
    {
        "id": "set2",
        "adA": "set2_a.png", "adB": "set2_b.png", "adC": "set2_c.png",
        "adText": {
            "A": "(가) 잔반 줄이기 공익 광고",
            "B": "(나) 잔반 줄이기 공익 광고",
            "C": "운동화 상업 광고"
        },
        "q1": {
            "rowA": {"t": "'한 숟갈'을 '300kg'과 나란히 놓아, 작아 보이는 양이 모이면 큰 양이 된다는 것을 보여 줌.", "i": "한 숟갈의 밥 옆에 같은 밥을 산처럼 쌓아, 남긴 양이 실제로 얼마나 큰지를 보여 줌."},
            "items": [
                {"id": "q1-1", "label": "(나) 문구 ( ㉠ )", "short": False, "key": {"ex": "'이 밥을 만든 손을 기억해 주세요'를 넣어, 우리가 무심코 남기는 음식에 많은 사람의 노고가 담겨 있음을 보여 줌."}},
                {"id": "q1-2", "label": "(나) 이미지 ( ㉡ )", "short": False, "key": {"ex": "농부, 조리사, 학생의 손을 나란히 배치하여, 밥 한 끼가 우리에게 오기까지의 과정과 감사의 필요성을 보여 줌."}}
            ]
        },
        "q2": {
            "items": [
                {"id": "q2-1", "label": "제작자의 관점과 의도", "short": False, "key": {"ex": "관점: 광고는 잔반을 수많은 사람의 노고와 정성을 버리는 행위로 본다. 왜냐하면 농부와 조리사의 거친 손 이미지 때문이다.\n의도: 제작자는 광고를 본 사람이 음식을 남기지 않고 다 먹게 하려 한다. 왜냐하면 누군가의 소중한 노력이기 때문이다."}}
            ]
        },
        "q3": {
            "buy": "운동화를 새로 사야 하는데, 이 광고를 살펴볼까?",
            "think1": "운동화를 크게 보여 주고 다른 학생들이 내려다보는 이미지와 '신는 순간, 시선이 달라집니다.'라는 문구를 종합해 보면 제작자는 운동화를 ( ㉠ )로/으로 보는 관점을 지닌 것 같아.",
            "think2": "하지만 운동화가 정말 그렇기만 한 물건인가? 나만 하더라도 그렇게 신지 않는데. 나라면 이 광고를 이렇게 바꾸겠어. 수정된 이미지는 운동장에서 공을 쫓아 뛰는 학생의 발로, 주변 학생들은 같이 뛰고 있는 모습으로, 문구는 '신는 순간, 발이 가벼워집니다.'로. 이렇게 바꾸면 광고에 담긴 관점이 운동화를 ( ㉡ )로/으로 보는 것으로 바뀌게 되니 실제 학생들의 하루를 더 정확하게 반영했다고 볼 수 있지.",
            "items": [
                {"id": "q3-1", "label": "㉠", "short": True, "key": {"ex": "타인의 시선을 끄는 과시용 도구"}},
                {"id": "q3-2", "label": "㉡", "short": True, "key": {"ex": "발을 편안하게 보호하고 활동을 돕는 실용적 도구"}},
                {"id": "q3-3", "label": "(2) 원본 광고의 제작자 의도", "short": False, "key": {"ex": "의도: 제작자는 광고를 본 사람이 남들의 시선을 끌기 위해 이 운동화를 구매하게 하려 한다. 왜냐하면 주변 학생들이 부러워하며 올려다보는 이미지 때문이다."}}
            ]
        }
    },
    {
        "id": "set3",
        "adA": "set3_a.png", "adB": "set3_b.png", "adC": "set3_c.png",
        "adText": {
            "A": "(가) 층간소음 방지 공익 광고",
            "B": "(나) 층간소음 방지 공익 광고",
            "C": "무선 이어폰 상업 광고"
        },
        "q1": {
            "rowA": {"t": "'당신의 발소리'를 '천장을 흔드는 것'이라고 말하여, 내게는 작은 소리가 아래층에서는 집을 흔드는 큰 소리가 된다는 것을 보여 줌.", "i": "위층의 발자국을 아래층 학생의 머리 위 그림자로 만들어, 소리가 아래층 사람을 누르는 무게가 된다는 것을 보여 줌."},
            "items": [
                {"id": "q1-1", "label": "(나) 문구 ( ㉠ )", "short": False, "key": {"ex": "'슬리퍼 한 켤레면 됩니다'라고 하여, 층간소음이라는 큰 문제가 슬리퍼를 신는 작은 실천으로 쉽게 해결될 수 있음을 보여 줌."}},
                {"id": "q1-2", "label": "(나) 이미지 ( ㉡ )", "short": False, "key": {"ex": "푹신해 보이는 슬리퍼와 그 안으로 들어가는 발을 크게 배치하여, 층간소음을 줄이기 위한 구체적이고 즉각적인 행동을 보여 줌."}}
            ]
        },
        "q2": {
            "items": [
                {"id": "q2-1", "label": "제작자의 관점과 의도", "short": False, "key": {"ex": "관점: 광고는 층간소음을 이웃에게 고통을 주는 무거운 폭력으로 본다. 왜냐하면 학생을 짓누르는 거대한 발자국 그림자 이미지 때문이다.\n의도: 제작자는 광고를 본 사람이 이웃을 배려하여 실내에서 조용히 걷게 하려 한다. 왜냐하면 아래층에 큰 고통이 되기 때문이다."}}
            ]
        },
        "q3": {
            "buy": "이어폰을 사야 하는데, 이 광고를 살펴볼까?",
            "think1": "주변을 흐리게 하고 혼자 눈을 감은 학생을 그린 이미지와 '세상을 끄고, 나만 남기다.'라는 문구를 종합해 보면 제작자는 이어폰을 ( ㉠ )로/으로 보는 관점을 지닌 것 같아.",
            "think2": "하지만 이어폰이 정말 그렇기만 한 물건인가? 나만 하더라도 그렇게 쓰지 않는데. 나라면 이 광고를 이렇게 바꾸겠어. 수정된 이미지는 두 학생이 이어폰을 한 쪽씩 나눠 끼고 같은 화면을 보며 웃는 모습으로, 주변도 선명하게, 문구는 '같은 노래, 같은 순간.'으로. 이렇게 바꾸면 광고에 담긴 관점이 이어폰을 ( ㉡ )로/으로 보는 것으로 바뀌게 되니 실제 학생들의 하루를 더 정확하게 반영했다고 볼 수 있지.",
            "items": [
                {"id": "q3-1", "label": "㉠", "short": True, "key": {"ex": "외부와 단절시키고 혼자만의 세계로 도피하게 하는 수단"}},
                {"id": "q3-2", "label": "㉡", "short": True, "key": {"ex": "타인과 감정을 공유하고 연결해 주는 매개체"}},
                {"id": "q3-3", "label": "(2) 원본 광고의 제작자 의도", "short": False, "key": {"ex": "의도: 제작자는 광고를 본 사람이 주변 소음을 차단하고 혼자만의 시간을 갖기 위해 이어폰을 구매하게 하려 한다. 왜냐하면 배경을 흐리게 처리하고 주인공만 평온하게 강조한 이미지 때문이다."}}
            ]
        }
    }
]

HERE = Path(__file__).parent
IMG_DIR = HERE / "images"

st.set_page_config(page_title="서논술형 답안 연습", page_icon="📝", layout="wide")

# ---------------------------------------------------------------- 상태 초기화
ss = st.session_state
if "answers" not in ss: ss.answers = {}
if "graded" not in ss: ss.graded = set()
if "student" not in ss: ss.student = ""

# 문항 총 개수 계산
TOTAL_Q = sum(len(s[qk]["items"]) for s in SETS for qk in ["q1", "q2", "q3"])

# ---------------------------------------------------------------- 좌측 사이드바 (정보 제공 및 이름 입력)
with st.sidebar:
    st.header("👤 학생 정보")
    ss.student = st.text_input("학번과 이름을 입력하세요", value=ss.student, placeholder="예: 30215 홍길동")
    if not ss.student:
        st.warning("문항을 풀기 전 반드시 학번·이름을 입력해 주세요.")
    
    st.divider()
    st.header("💡 필수 개념 다지기")
    st.markdown("""
    **1. 광고·홍보물**
    - 상품이나 서비스를 구매하게 하거나 정보를 널리 알리려는 설득의 목적으로 제작됨.
    
    **2. 재현**
    - 제작자가 자신의 관점과 의도를 담아 현실을 다시 나타내는 것. 특정 이미지나 문구를 선택적으로 사용함 (현실과 일치하지 않음).
    
    **3. 관점**
    - 대상을 무엇으로 보는가?
    - **"( )를/을 ( )로/으로 본다"** 형태의 문장으로 정리.
    
    **4. 의도**
    - 수용자가 무엇을 하게 하려는가?
    - **"광고를 본 사람이 ( )하게 하려 한다"** 형태의 문장으로 정리.
    """)

# ---------------------------------------------------------------- 상단 디자인 (진행률 및 네비게이션)
PAGES = []
for si, s in enumerate(SETS, 1):
    for qi, qk in enumerate(["q1", "q2", "q3"], 1):
        PAGES.append({"id": f"{s['id']}-{qk}", "set": s, "qkey": qk, "tab": f"{si}-{qi}", "name": f"📝 {si}번 세트 – 서·논술형 {qi}"})
PAGES.append({"id": "review", "tab": "복습", "name": "📚 복습 및 결과 모아보기"})
PAGE_IDS = [p["id"] for p in PAGES]

if "page" not in ss: ss.page = PAGE_IDS[0]

completed_q = len([k for k, v in ss.answers.items() if v.strip()])
progress_val = completed_q / TOTAL_Q if TOTAL_Q > 0 else 0

st.progress(progress_val)
st.caption(f"**현재 진행 상황:** 전체 {TOTAL_Q}개 문항 중 {completed_q}개 작성 완료")
st.divider()

# ---------------------------------------------------------------- 구글 시트 연동 (행 단위 실시간 기록)
def log_action_to_sheet(student_name, question_label, answer_text):
    if "gcp_service_account" not in st.secrets or "SHEET_URL" not in st.secrets:
        return # 시트 설정이 없으면 패스
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        info = dict(st.secrets["gcp_service_account"])
        creds = Credentials.from_service_account_info(info, scopes=["https://www.googleapis.com/auth/spreadsheets"])
        sh = gspread.authorize(creds).open_by_url(st.secrets["SHEET_URL"])
        ws = sh.sheet1
        
        # [제출시각, 학번·이름, 문항번호, 작성답안] 형태로 한 줄씩 누적 기록
        row_data = [f"{dt.datetime.now():%Y-%m-%d %H:%M:%S}", student_name, question_label, answer_text]
        ws.append_row(row_data)
    except Exception as e:
        st.error(f"데이터 기록 중 오류가 발생했습니다: {e}")

# ---------------------------------------------------------------- UI 컴포넌트
def akey(set_id, item_id):
    return f"{set_id}-{item_id}"

def answer_box_with_grade(set_id, it):
    k = akey(set_id, it["id"])
    widget = st.text_input if it.get("short") else st.text_area
    val = widget(f"**{it['label']}**", value=ss.answers.get(k, ""), key=f"w-{k}", placeholder="여기에 답안을 작성하세요")
    ss.answers[k] = val
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("제출 및 예시답안 확인", key=f"btn-{k}", type="primary", use_container_width=True):
            if not ss.student.strip():
                st.error("사이드바에 학번·이름을 먼저 입력하세요.")
            elif not val.strip():
                st.warning("답안을 작성한 후 눌러주세요.")
            else:
                with st.spinner("기록 중..."):
                    log_action_to_sheet(ss.student, it['label'], val)
                ss.graded.add(k)
                st.success("제출 완료!")
                
    if k in ss.graded:
        with st.expander("✅ 예시 답안 보기 (스스로 비교하며 복습해 보세요)", expanded=True):
            st.info(f"**[예시 답안]**\n\n{it['key']['ex']}")

def cond(lines):
    body = "\n".join(f"◦ {ln}" for ln in lines)
    st.markdown(f"**〈조건〉**  \n{body}")

def ads(s):
    st.markdown("##### [서·논술형 1~2] 다음 자료를 읽고 물음에 답하시오.")
    c1, c2 = st.columns(2)
    try: c1.image(str(IMG_DIR / s["adA"]), caption="(가)", use_column_width=True)
    except: c1.info("(가) 광고 이미지 자리")
    try: c2.image(str(IMG_DIR / s["adB"]), caption="(나)", use_column_width=True)
    except: c2.info("(나) 광고 이미지 자리")

# ---------------------------------------------------------------- 문항 페이지 렌더링
def page_q1(s):
    q = s["q1"]; ads(s)
    st.subheader(f"📝 {s['id'][-1]}번 세트 - 서·논술형 1")
    st.write("두 광고의 재현 방식을 표로 정리하였다. ㉠~㉡에 들어갈 내용을 <조건>에 맞게 쓰시오.")
    st.table({"": ["(가)", "(나)"], "문구": [q["rowA"]["t"], "( ㉠ )"], "이미지": [q["rowA"]["i"], "( ㉡ )"]})
    
    cond([
        "광고 문구·이미지와 그로 인한 효과를 한 문장으로 쓸 것.",
        "아래 문장 틀에 맞추어 쓸 것.",
        "> - ( )을/를 ( )하여(만들어/넣어/불러), ( )을/를 보여 줌."
    ])
    st.divider()
    for it in q["items"]: 
        answer_box_with_grade(s["id"], it)
        st.write("")

def page_q2(s):
    q = s["q2"]; ads(s)
    st.subheader(f"📝 {s['id'][-1]}번 세트 - 서·논술형 2")
    st.write("두 광고에 담긴 제작자의 관점과 의도를 <조건>에 맞게 서술하시오.")
    cond([
        "광고에 재현된 내용에서 찾은 근거를 포함하여 기술할 것.",
        "아래 문장 틀에 맞추어 쓸 것.",
        "> - 관점: 광고는 ( )을/를 ( )로/으로 본다. 왜냐하면 ( ) 때문이다.",
        "> - 의도: 제작자는 광고를 본 사람이 ( )하게 하려 한다. 왜냐하면 ( ) 때문이다."
    ])
    st.divider()
    for it in q["items"]: 
        answer_box_with_grade(s["id"], it)
        st.write("")

def page_q3(s):
    q = s["q3"]
    st.markdown("##### [서·논술형 3] 다음 자료를 읽고 물음에 답하시오.")
    c1, c2 = st.columns([1, 1.15])
    try: c1.image(str(IMG_DIR / s["adC"]), caption="[광고]", use_column_width=True)
    except: c1.info("[광고] 이미지 자리")
    with c2:
        st.markdown("**[학생의 사고 과정]**")
        st.info(f"{q['buy']}\n\n{q['think1']}\n\n{q['think2']}")
    
    st.subheader(f"📝 {s['id'][-1]}번 세트 - 서·논술형 3")
    st.markdown("**(1) ㉠, ㉡에 들어가기에 적절한 표현을 쓰시오.**")
    answer_box_with_grade(s["id"], q["items"][0])
    answer_box_with_grade(s["id"], q["items"][1])
    
    st.divider()
    st.markdown("**(2) 위 광고에 담긴 제작자의 의도를 재현 방법을 근거로 들어 서술하시오.**")
    cond([
        "광고에 재현된 내용에서 찾은 근거를 포함하여 기술할 것.",
        "아래 문장 틀에 맞추어 쓸 것.",
        "> - 의도: 제작자는 광고를 본 사람이 ( )하게 하려 한다. 왜냐하면 ( ) 때문이다."
    ])
    answer_box_with_grade(s["id"], q["items"][2])

# ---------------------------------------------------------------- 복습 탭
def page_review():
    st.subheader("📚 나의 답안 복습하기")
    st.caption("지금까지 작성한 나의 답안과 예시 답안을 한눈에 비교하며 부족한 점을 점검해 보세요.")
    
    if not ss.graded:
        st.info("아직 제출 및 확인을 완료한 문항이 없습니다. 문항을 풀고 '제출 및 예시답안 확인' 버튼을 눌러주세요.")
        return

    for s in SETS:
        for qk in ["q1", "q2", "q3"]:
            for it in s[qk]["items"]:
                k = akey(s["id"], it["id"])
                if k in ss.graded:
                    my_ans = ss.answers.get(k, "")
                    st.markdown(f"**[{s['id'][-1]}번 세트 - {it['label']}]**")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.success(f"**나의 답안:**\n\n{my_ans}")
                    with col2:
                        st.info(f"**예시 답안:**\n\n{it['key']['ex']}")
                    st.divider()

# ---------------------------------------------------------------- 네비게이션 및 렌더링
choice = st.radio("문항 이동", [p["tab"] for p in PAGES], horizontal=True, label_visibility="collapsed", index=PAGE_IDS.index(ss.page))
sel = next(p for p in PAGES if p["tab"] == choice)
if sel["id"] != ss.page: 
    ss.page = sel["id"]
    st.rerun()

idx = PAGE_IDS.index(ss.page)
page = PAGES[idx]

if page["id"] == "review": 
    page_review()
else:
    {"q1": page_q1, "q2": page_q2, "q3": page_q3}[page["qkey"]](page["set"])

st.divider()
c1, c2 = st.columns(2)
if idx > 0 and c1.button(f"← 이전: {PAGES[idx-1]['name']}", use_container_width=True):
    ss.page = PAGE_IDS[idx - 1]
    st.rerun()
if idx < len(PAGES) - 1 and c2.button(f"다음: {PAGES[idx+1]['name']} →", type="primary", use_container_width=True):
    ss.page = PAGE_IDS[idx + 1]
    st.rerun()
