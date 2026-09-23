# -*- coding: utf-8 -*-
import datetime as dt
import base64
from pathlib import Path
import pandas as pd
import streamlit as st

# ---------------------------------------------------------------- 데이터 세트
SETS = [
    {
        "id": "set1",
        "adA": "set1_a.png", "adB": "set1_b.png", "adC": "set1_c.png",
        "adText": "비교적 쉬운 취미 생활이나 큰 노력이 필요 없는 과제를 할 때는 커피숍이나 도서관에서 하거나 공부 모임을 만드는 것이 능률을 올릴 수 있습니다. 반대로 지나치게 어렵거나 도전이 필요한 과제는 차분하게 혼자 집중하는 시간을 가지는 것이 좋습니다.",
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
                {"id": "q3-3", "label": "원본 광고의 제작자 의도", "short": False, "key": {"ex": "의도: 제작자는 광고를 본 사람이 스마트워치를 구매하여 시간을 철저하게 관리하게 하려 한다. 왜냐하면 뛰어가는 학생과 1분도 놓치지 않겠다는 문구 때문이다."}}
            ]
        }
    },
    {
        "id": "set2",
        "adA": "set2_a.png", "adB": "set2_b.png", "adC": "set2_c.png",
        "adText": "잔반으로 인해 버려지는 수많은 노력과 자원을 보여주는 공익 광고 자료입니다. 식판 위의 남긴 밥 한 숟갈이 모여 거대한 산을 이루는 모습과, 이 밥을 만들기 위해 수고한 농부와 조리사의 손을 통해 우리가 무심코 버리는 음식의 가치를 일깨웁니다.",
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
            "think2": "하지만 운동화가 정말 그렇기만 한 물건인가? 나라면 이 광고를 이렇게 바꾸겠어. 수정된 이미지는 운동장에서 공을 쫓아 뛰는 학생의 발로, 주변 학생들은 같이 뛰고 있는 모습으로, 문구는 '신는 순간, 발이 가벼워집니다.'로. 이렇게 바꾸면 광고에 담긴 관점이 운동화를 ( ㉡ )로/으로 보는 것으로 바뀌게 되지.",
            "items": [
                {"id": "q3-1", "label": "㉠", "short": True, "key": {"ex": "타인의 시선을 끄는 과시용 도구"}},
                {"id": "q3-2", "label": "㉡", "short": True, "key": {"ex": "발을 편안하게 보호하고 활동을 돕는 실용적 도구"}},
                {"id": "q3-3", "label": "원본 광고의 제작자 의도", "short": False, "key": {"ex": "의도: 제작자는 광고를 본 사람이 남들의 시선을 끌기 위해 이 운동화를 구매하게 하려 한다. 왜냐하면 주변 학생들이 부러워하며 올려다보는 이미지 때문이다."}}
            ]
        }
    },
    {
        "id": "set3",
        "adA": "set3_a.png", "adB": "set3_b.png", "adC": "set3_c.png",
        "adText": "층간소음 문제와 무선 이어폰 사용에 대한 광고 자료입니다. 누군가에게는 작은 발소리가 다른 누군가에게는 천장을 흔드는 고통이 될 수 있음을 시각화하고, 복잡한 세상 속에서 자신만의 시간을 가지려는 현대인의 모습을 담았습니다.",
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
            "think2": "하지만 이어폰이 정말 그렇기만 한 물건인가? 나라면 이 광고를 이렇게 바꾸겠어. 수정된 이미지는 두 학생이 이어폰을 한 쪽씩 나눠 끼고 같은 화면을 보며 웃는 모습으로, 주변도 선명하게, 문구는 '같은 노래, 같은 순간.'으로. 이렇게 바꾸면 광고에 담긴 관점이 이어폰을 ( ㉡ )로/으로 보는 것으로 바뀌게 되지.",
            "items": [
                {"id": "q3-1", "label": "㉠", "short": True, "key": {"ex": "외부와 단절시키고 혼자만의 세계로 도피하게 하는 수단"}},
                {"id": "q3-2", "label": "㉡", "short": True, "key": {"ex": "타인과 감정을 공유하고 연결해 주는 매개체"}},
                {"id": "q3-3", "label": "원본 광고의 제작자 의도", "short": False, "key": {"ex": "의도: 제작자는 광고를 본 사람이 주변 소음을 차단하고 혼자만의 시간을 갖기 위해 이어폰을 구매하게 하려 한다. 왜냐하면 배경을 흐리게 처리하고 주인공만 평온하게 강조한 이미지 때문이다."}}
            ]
        }
    }
]

HERE = Path(__file__).parent
IMG_DIR = HERE / "images"

st.set_page_config(page_title="서·논술형 답안 연습", page_icon="📝", layout="wide")

# ---------------------------------------------------------------- 상태 초기화
ss = st.session_state
if "answers" not in ss: ss.answers = {}
if "graded" not in ss: ss.graded = set()
if "scores" not in ss: ss.scores = {}
if "student" not in ss: ss.student = ""

# ---------------------------------------------------------------- 사이드바
with st.sidebar:
    st.markdown("### 👤 학생 정보")
    ss.student = st.text_input("자신의 학번과 이름을 입력하세요.", value=ss.student, placeholder="예: 30215 홍길동")
    
    st.divider()
    st.markdown("### 💡 개념 길잡이")
    
    st.markdown("#### 1. 설명 방법 공식")
    st.markdown("""
    - **정의**: ~란 ~를 말한다.
    - **예시**: 예를 들어 ~
    - **인과**: ~ 때문에 ~한다.
    - **비교와 대조**: [공통점] ~와 ~의 공통점은 ~이다. / [차이점] ~는 ~이지만, ~는 ~이다.
    - **분석**: ~는 ~와(과) ~로 이루어져 있다.
    - **분류와 구분**: ~는 ~라는 기준에 따라 ~와(과) ~로 나뉜다.
    """)
    
    st.markdown("""
    <div style="background-color: #e8f4f8; padding: 12px; border-left: 5px solid #2b6cb0; border-radius: 4px; margin-bottom: 20px;">
        <strong>[2번 문제 풀이 팁]</strong><br>
        위 공식을 활용해 문장을 만들고 끝에 (설명방법)을 꼭 쓰세요!<br>서로 다른 두 방법을 사용해야 합니다.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 2. 시험 범위 및 용어")
    st.markdown("""
    - **시험 범위**: 교과서 96-97쪽 본문, 국어 학습지 전체
    - **재현**: 현실을 재구성했으나 현실과 똑같지 않음. 광고에서는 문구와 이미지로 드러남.
    - **관점**: 제작자가 대상을 보는 시선.
    """)
    st.markdown("""
    <div style="background-color: #e8f4f8; padding: 10px; border-left: 5px solid #2b6cb0; border-radius: 4px; margin-bottom: 10px;">
        <strong>[TIP]</strong> "( )을/를 ( )으로/로 본다"의 문장 형태로 정리
    </div>
    """, unsafe_allow_html=True)
    st.markdown("- **의도**: 제작자가 수용자에게 하게 하려는 것.")
    st.markdown("""
    <div style="background-color: #e8f4f8; padding: 10px; border-left: 5px solid #2b6cb0; border-radius: 4px;">
        <strong>[TIP]</strong> "광고를 본 사람이 ( )하게 하려 한다"의 문장 형태로 정리
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------------- 이미지 Base64 인코더 (크기 축소 및 하단 기호 디자인)
def get_base64_image(file_name, label):
    img_path = IMG_DIR / file_name
    try:
        with open(img_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
        return f"""
        <div style="background-color: #e2e8f0; padding: 20px; border-radius: 10px; text-align: center; height: 100%;">
            <img src="data:image/png;base64,{encoded}" style="max-height: 250px; width: auto; max-width: 100%; border-radius: 5px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 15px;">
            <strong style="display: block; font-size: 1.2em; color: #2d3748;">{label}</strong>
        </div>
        """
    except Exception:
        return f"<div style='background-color: #e2e8f0; padding: 20px; text-align: center; border-radius: 10px;'><strong style='color: #2d3748;'>{label}</strong><br>이미지 로드 대기 중...</div>"

# ---------------------------------------------------------------- 상단 디자인
st.markdown("### 📝 [국어] 서·논술형 답안 작성 연습")
st.markdown("##### 작성한 답안을 입력한 뒤 문제의 조건에 맞게 작성하였는지 확인하세요.")

completed = len(ss.graded)
st.progress(completed / 9.0)
st.markdown(f"**이번 회차 내가 푼 문제 : {completed}/9**")
st.caption("세트 탭을 자유롭게 이동하면서, 각 세트 안에서 문항별로 즉각 피드백을 받을 수 있어요.")
st.write("")

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
        if not ss.student.strip():
            st.error("좌측 사이드바에 학번과 이름을 먼저 입력해주세요!")
        elif all(v.strip() for v in inputs.values()):
            for it in q_data["items"]:
                k_it = f"{k_q}-{it['id']}"
                ss.answers[k_it] = inputs[k_it]
                log_action_to_sheet(s['id'], qkey, it['label'], inputs[k_it])
            ss.graded.add(k_q)
            st.success("✅ 제출 완료! 아래에서 예시 답안과 비교하며 자가 채점을 진행하세요.")
        else:
            st.warning("⚠️ 모든 빈칸에 답안을 작성한 후 제출해주세요.")

    if k_q in ss.graded:
        with st.expander("✅ 예시 답안 및 자가 채점 (클릭하여 열기)", expanded=True):
            for it in q_data["items"]:
                st.markdown(f"**[{it['label']}] 예시 답안**")
                st.info(it['key']['ex'])
            
            st.divider()
            score = st.radio(f"이 문항에 대한 나의 점수는 몇 점인가요? ({qkey.upper()})", [1, 2, 3], index=ss.scores.get(k_q, 3)-1, horizontal=True, key=f"score-{k_q}")
            ss.scores[k_q] = score

# ---------------------------------------------------------------- 네비게이션
tabs = st.tabs(["[실전 적용 1]", "[실전 적용 2]", "[실전 적용 3]", "📚 전체 복습"])

for i, tab in enumerate(tabs[:3]):
    with tab:
        s = SETS[i]
        
        st.markdown(f"""
        <div style="background-color: #f7f9fc; padding: 15px; border-radius: 5px; margin-bottom: 20px; font-size: 1.05em; line-height: 1.6; border: 1px solid #e2e8f0;">
        <span style="color: #2b6cb0; font-weight: bold;">[지문]</span><br>
        {s['adText']}
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        c1.markdown(get_base64_image(s["adA"], "(가)"), unsafe_allow_html=True)
        c2.markdown(get_base64_image(s["adB"], "(나)"), unsafe_allow_html=True)
        st.write("")
        
        # 문항 서브 탭
        q_choice = st.radio(f"문항 선택 ({s['id']})", ["1. 재현 방식", "2. 관점과 의도", "3. 비판적 읽기"], horizontal=True, label_visibility="collapsed")
        st.divider()
        
        if q_choice == "1. 재현 방식":
            q = s["q1"]
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
            
        elif q_choice == "2. 관점과 의도":
            q = s["q2"]
            st.write("두 광고에 담긴 제작자의 관점과 의도를 <조건>에 맞게 서술하시오.")
            cond([
                "광고에 재현된 내용에서 찾은 근거를 포함하여 기술할 것.",
                "아래 문장 틀에 맞추어 쓸 것.",
                " - 관점: 광고는 ( )을/를 ( )로/으로 본다. 왜냐하면 ( ) 때문이다.",
                " - 의도: 제작자는 광고를 본 사람이 ( )하게 하려 한다. 왜냐하면 ( ) 때문이다."
            ])
            question_block(s, "q2", q)
            
        else:
            q = s["q3"]
            st.markdown("**(1) ㉠, ㉡에 들어가기에 적절한 표현을 쓰시오.**")
            st.markdown("**(2) 위 광고에 담긴 제작자의 의도를 재현 방법을 근거로 들어 서술하시오.**")
            
            st.markdown(f"""
            <div style="background-color: #fcf8e3; padding: 15px; border-radius: 5px; margin-bottom: 15px; border-left: 4px solid #f0ad4e;">
            <strong>[학생의 사고 과정]</strong><br><br>
            {q['buy']}<br><br>{q['think1']}<br><br>{q['think2']}
            </div>
            """, unsafe_allow_html=True)
            
            cond([
                "광고에 재현된 내용에서 찾은 근거를 포함하여 기술할 것.",
                "아래 문장 틀에 맞추어 쓸 것.",
                " - 의도: 제작자는 광고를 본 사람이 ( )하게 하려 한다. 왜냐하면 ( ) 때문이다."
            ])
            
            # 3번 문항의 광고(C) 이미지 축소 삽입
            col_img, col_empty = st.columns([1, 1])
            with col_img:
                st.markdown(get_base64_image(s["adC"], "[광고]"), unsafe_allow_html=True)
                st.write("")
                
            question_block(s, "q3", q)

# ---------------------------------------------------------------- 복습 탭
with tabs[3]:
    if not ss.student:
        st.warning("왼쪽 사이드바에 학번과 이름을 입력하셔야 전체 복습 데이터를 확인할 수 있습니다.")
    elif not ss.graded:
        st.info("아직 제출을 완료한 문항이 없습니다. 문항을 풀고 '제출하고 피드백 받기' 버튼을 눌러주세요.")
    else:
        st.markdown(f"### 📊 {ss.student} 학생의 전체 복습 데이터")
        
        # 득점 그래프 표시
        score_data = {"문항": [], "점수": []}
        for k, v in ss.scores.items():
            set_name = "세트" + k.split("-")[0].replace("set", "")
            q_name = "문항" + k.split("-")[1].replace("q", "")
            score_data["문항"].append(f"{set_name}-{q_name}")
            score_data["점수"].append(v)
            
        if score_data["문항"]:
            df = pd.DataFrame(score_data)
            st.bar_chart(df.set_index("문항"))
        
        st.divider()
        st.markdown("#### 📝 문항별 오답 노트")
        for s in SETS:
            for qkey in ["q1", "q2", "q3"]:
                k_q = f"{s['id']}-{qkey}"
                if k_q in ss.graded:
                    st.markdown(f"**[{s['id'][-1]}번 세트 - {qkey.upper()}] (스스로 평가한 점수: {ss.scores.get(k_q, 0)}점)**")
                    for it in s[qkey]["items"]:
                        k_it = f"{k_q}-{it['id']}"
                        my_ans = ss.answers.get(k_it, "미작성")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.success(f"**나의 답안 [{it['label']}]:**\n\n{my_ans}")
                        with col2:
                            st.info(f"**예시 답안:**\n\n{it['key']['ex']}")
                    st.write("")
