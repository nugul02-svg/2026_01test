# -*- coding: utf-8 -*-
import datetime as dt
import os
from pathlib import Path
import streamlit as st

# ---------------------------------------------------------------- 데이터 세트
SETS = [
    {
        "id": "set1",
        "adA": "set1_a.png", "adB": "set1_b.png", "adC": "set1_c.png",
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

st.set_page_config(page_title="서논술형 답안 연습", page_icon="🕵️‍♂️", layout="wide")

# ---------------------------------------------------------------- 상태 초기화
ss = st.session_state
if "answers" not in ss: ss.answers = {}
if "graded" not in ss: ss.graded = set()

# ---------------------------------------------------------------- 좌측 사이드바 (개념 정리 및 서버 진단)
with st.sidebar:
    st.header("💡 필수 개념 다지기")
    st.markdown("""
    **1. 광고·홍보물**
    - 상품이나 서비스를 구매하게 하거나 정보를 널리 알리려는 설득의 목적으로 제작됨.
    
    **2. 재현**
    - 제작자가 자신의 관점과 의도를 담아 현실을 다시 나타내는 것. 특정 이미지나 문구를 선택적으로 사용. (현실과 일치하지 않음)
    
    **3. 관점**
    - 대상을 무엇으로 보는가?
    - **"( )를/을 ( )로/으로 본다"**
    
    **4. 의도**
    - 수용자가 무엇을 하게 하려는가?
    - **"광고를 본 사람이 ( )하게 하려 한다"**
    """)
    
    st.divider()
    st.markdown("🛠️ **시스템 진단 (이미지 에러 추적기)**")
    if IMG_DIR.exists():
        files = [f.name for f in IMG_DIR.iterdir()]
        if files:
            st.success(f"images 폴더를 찾았습니다! 내부 파일: {', '.join(files)}")
        else:
            st.warning("images 폴더는 있지만 안이 비어있습니다.")
    else:
        st.error(f"오류: {IMG_DIR} 경로에 images 폴더가 존재하지 않습니다.")

# ---------------------------------------------------------------- 구글 시트 연동 (익명 로그)
def log_action_to_sheet(set_id, qkey, label, answer_text):
    if "gcp_service_account" not in st.secrets or "SHEET_URL" not in st.secrets:
        return
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        info = dict(st.secrets["gcp_service_account"])
        creds = Credentials.from_service_account_info(info, scopes=["https://www.googleapis.com/auth/spreadsheets"])
        sh = gspread.authorize(creds).open_by_url(st.secrets["SHEET_URL"])
        ws = sh.sheet1
        
        row_data = [f"{dt.datetime.now():%Y-%m-%d %H:%M:%S}", f"[{set_id.upper()}] {qkey}", label, answer_text]
        ws.append_row(row_data)
    except Exception:
        pass 

# ---------------------------------------------------------------- 상단 디자인
st.markdown("# 🕵️‍♂️ [국어] 서·논술형 답안 작성 연습")
st.markdown("#### 작성한 답안을 입력한 뒤 문제의 조건에 맞게 작성하였는지 확인하세요.")

st.markdown("""
<div style="background-color: #f0f4f8; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #2b6cb0;">
<h4 style="margin-top: 0; color: #2b6cb0;">🎯 2학기 1회시험 대비 실전 모의고사</h4>
그동안 탐정이 되어 광고 홍보물 속에 담긴 관점과 의도를 추리해 온 당신! 실력을 점검해 봅시다.<br><br>
정기시험에 출제되는 서논술형 문제는 이 문항들과 자료만이 다를 뿐 동일한 질문을 던집니다.<br>
반드시 <b>국어 공책에 붙은 학습지에 답을 쓰고, 자신이 쓴 답을 웹앱에 입력</b>하세요.<br>
그래야 응답 받은 결과가 자신의 학습 재료가 됩니다. 무엇이 틀리고, 무엇이 맞았는지 명확하게 파악하고 자신의 답안이 갖추어야 하는 조건을 확인하세요.
</div>
""", unsafe_allow_html=True)

completed = len(ss.graded)
st.progress(completed / 9.0)
st.markdown(f"**완료된 📝 : {completed}/9**")
st.caption("세트 탭을 자유롭게 이동하면서, 각 세트 안에서 문항별로 즉각 피드백을 받을 수 있어요.")
st.write("")

# ---------------------------------------------------------------- UI 컴포넌트
def cond(lines):
    body = "<br>".join(f"• {ln}" for ln in lines)
    st.markdown(f"""
    <div style="background-color: #f8f9fa; border-left: 4px solid #4a90e2; padding: 10px 15px; margin-bottom: 15px; border-radius: 5px;">
        <strong style="color: #4a90e2;">&lt;조건&gt;</strong><br>
        <span style="font-size: 0.95em;">{body}</span>
    </div>
    """, unsafe_allow_html=True)

def question_block(s, qkey, q_data):
    k_q = f"{s['id']}-{qkey}"
    inputs = {}
    
    for it in q_data["items"]:
        k_it = f"{k_q}-{it['id']}"
        widget = st.text_input if it.get("short") else st.text_area
        val = widget(f"**{it['label']}**", value=ss.answers.get(k_it, ""), key=f"w-{k_it}")
        inputs[k_it] = val

    st.write("")
    if st.button("🚀 제출하고 피드백 받기", key=f"btn-{k_q}", type="primary", use_container_width=True):
        if all(v.strip() for v in inputs.values()):
            for it in q_data["items"]:
                k_it = f"{k_q}-{it['id']}"
                ss.answers[k_it] = inputs[k_it]
                log_action_to_sheet(s['id'], qkey, it['label'], inputs[k_it])
            ss.graded.add(k_q)
            st.success("✅ 제출 완료! 아래에서 피드백을 확인하세요.")
        else:
            st.warning("⚠️ 모든 빈칸에 답안을 작성한 후 제출해주세요.")

    if k_q in ss.graded:
        with st.expander("✅ 예시 답안 보기 (스스로 비교하며 점검해 보세요)", expanded=True):
            for it in q_data["items"]:
                st.markdown(f"**[{it['label']}] 예시 답안**")
                st.info(it['key']['ex'])

def ads(s):
    c1, c2 = st.columns(2)
    try:
        c1.image(str(IMG_DIR / s["adA"]), caption="(가)", use_container_width=True)
    except Exception as e:
        c1.error(f"(가) 이미지 에러: {e}")
        
    try:
        c2.image(str(IMG_DIR / s["adB"]), caption="(나)", use_container_width=True)
    except Exception as e:
        c2.error(f"(나) 이미지 에러: {e}")

# ---------------------------------------------------------------- 문항 페이지 렌더링
def page_q1(s):
    q = s["q1"]
    st.markdown("### 1. 재현 방식")
    st.write("두 광고의 재현 방식을 표로 정리하였다. ㉠~㉡에 들어갈 내용을 <조건>에 맞게 쓰시오.")
    st.markdown(f"""
| | 문구 | 이미지 |
|:---:|---|---|
| **(가)** | {q['rowA']['t']} | {q['rowA']['i']} |
| **(나)** | ( ㉠ ) | ( ㉡ ) |
    """)
    cond([
        "광고 문구·이미지와 그로 인한 효과를 한 문장으로 쓸 것.",
        "아래 문장 틀에 맞추어 쓸 것.",
        " - ( )을/를 ( )하여(만들어/넣어/불러), ( )을/를 보여 줌."
    ])
    question_block(s, "q1", q)

def page_q2(s):
    q = s["q2"]
    st.markdown("### 2. 관점과 의도")
    st.write("두 광고에 담긴 제작자의 관점과 의도를 <조건>에 맞게 서술하시오.")
    cond([
        "광고에 재현된 내용에서 찾은 근거를 포함하여 기술할 것.",
        "아래 문장 틀에 맞추어 쓸 것.",
        " - 관점: 광고는 ( )을/를 ( )로/으로 본다. 왜냐하면 ( ) 때문이다.",
        " - 의도: 제작자는 광고를 본 사람이 ( )하게 하려 한다. 왜냐하면 ( ) 때문이다."
    ])
    question_block(s, "q2", q)

def page_q3(s):
    q = s["q3"]
    st.markdown("### 3. 비판적 읽기")
    st.markdown("**(1) ㉠, ㉡에 들어가기에 적절한 표현을 쓰시오.**")
    st.markdown("**(2) 위 광고에 담긴 제작자의 의도를 재현 방법을 근거로 들어 서술하시오.**")
    
    st.markdown(f"""
    <div style="background-color: #fcf8e3; padding: 15px; border-radius: 5px; margin-bottom: 15px;">
    <strong>[학생의 사고 과정]</strong><br><br>
    {q['buy']}<br><br>{q['think1']}<br><br>{q['think2']}
    </div>
    """, unsafe_allow_html=True)
    
    cond([
        "광고에 재현된 내용에서 찾은 근거를 포함하여 기술할 것.",
        "아래 문장 틀에 맞추어 쓸 것.",
        " - 의도: 제작자는 광고를 본 사람이 ( )하게 하려 한다. 왜냐하면 ( ) 때문이다."
    ])
    question_block(s, "q3", q)

# ---------------------------------------------------------------- 네비게이션
tabs = st.tabs(["[실전 적용 1]", "[실전 적용 2]", "[실전 적용 3]", "📚 전체 복습"])

for i, tab in enumerate(tabs[:3]):
    with tab:
        s = SETS[i]
        st.markdown("##### [서·논술형 1~2] 다음 자료를 읽고 물음에 답하시오.")
        ads(s)
        st.divider()
        
        q_choice = st.radio(f"문항 선택 ({s['id']})", ["1. 재현 방식", "2. 관점과 의도", "3. 비판적 읽기"], horizontal=True, label_visibility="collapsed")
        
        if q_choice == "1. 재현 방식":
            page_q1(s)
        elif q_choice == "2. 관점과 의도":
            page_q2(s)
        else:
            st.markdown("##### [서·논술형 3] 다음 자료를 읽고 물음에 답하시오.")
            try:
                st.image(str(IMG_DIR / s["adC"]), caption="[광고]", use_container_width=True)
            except Exception as e:
                st.error(f"[광고] 이미지 에러: {e}")
            page_q3(s)

# ---------------------------------------------------------------- 복습 탭
with tabs[3]:
    st.subheader("📚 나의 답안 복습하기")
    st.caption("지금까지 작성한 나의 답안과 예시 답안을 한눈에 비교하며 부족한 점을 점검해 보세요.")
    
    if not ss.graded:
        st.info("아직 제출을 완료한 문항이 없습니다. 문항을 풀고 '제출하고 피드백 받기' 버튼을 눌러주세요.")
    else:
        for s in SETS:
            for qkey in ["q1", "q2", "q3"]:
                k_q = f"{s['id']}-{qkey}"
                if k_q in ss.graded:
                    st.markdown(f"#### 📝 {s['id'][-1]}번 세트 - {qkey.upper()}")
                    for it in s[qkey]["items"]:
                        k_it = f"{k_q}-{it['id']}"
                        my_ans = ss.answers.get(k_it, "미작성")
                        st.markdown(f"**[{it['label']}]**")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.success(f"**나의 답안:**\n\n{my_ans}")
                        with col2:
                            st.info(f"**예시 답안:**\n\n{it['key']['ex']}")
                    st.divider()
