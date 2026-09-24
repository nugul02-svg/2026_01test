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
        "q1": {
            "rowA": {"t": "'고개를 드는 것'을 '5초가 보이는 것'과 짝지어 위험을 알아챌 시간이 생긴다는 것을 보여 줌.", "i": "신호등을 넣어 학생이 보지 못하는 남은 시간을 보여 줌."},
            "items": [
                {"id": "q1-1", "label": "(나) 문구 ( ㉠ )", "short": False, "key": {"ex": "'운전자는 당신이 자기를 봤다고 생각합니다'를 넣어, 운전자와 보행자의 서로 다른 인식 차이로 인한 위험성을 보여 줌. / 운전자의 입장을 문구로 제시하여, 청소년 보행자가 스스로를 돌아보고 경각심을 가지게 함."}},
                {"id": "q1-2", "label": "(나) 이미지 ( ㉡ )", "short": False, "key": {"ex": "운전자의 시선에서 스마트폰을 보며 걷는 학생을 보여 주어, 운전자 입장에서 느끼는 상황의 아찔함과 위험성을 보여 줌. / 교복 입은 학생을 이미지에 담아 청소년이 자기 이야기처럼 여길 수 있게 함."}}
            ]
        },
        "q2": {
            "items": [
                {"id": "q2-1", "label": "(가)의 관점", "short": False, "key": {"ex": "광고는 스마트폰 보행을 생명을 위협하는 위험한 행동으로 본다. 왜냐하면 운전자 시점의 아찔한 횡단보도 이미지 때문이다."}},
                {"id": "q2-2", "label": "(가)의 의도", "short": False, "key": {"ex": "제작자는 광고를 본 사람이 보행 중 스마트폰을 보지 않게 하려 한다."}},
                {"id": "q2-3", "label": "(나)의 관점", "short": False, "key": {"ex": "광고는 스마트폰 보행을 운전자와 보행자의 서로 다른 인식 차이로 인한 치명적인 위험으로 본다. 왜냐하면 '운전자는 당신이 자기를 봤다고 생각합니다'라는 문구 때문이다."}},
                {"id": "q2-4", "label": "(나)의 의도", "short": False, "key": {"ex": "제작자는 광고를 본 사람이 보행 중 스마트폰을 보지 않게 하려 한다."}}
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
        "q1": {
            "rowA": {"t": "'한 숟갈'을 '300kg'과 나란히 놓아, 작아 보이는 양이 모이면 큰 양이 된다는 것을 보여 줌.", "i": "한 숟갈의 밥 옆에 같은 밥을 산처럼 쌓아, 남긴 양이 실제로 얼마나 큰지를 보여 줌."},
            "items": [
                {"id": "q1-1", "label": "(나) 문구 ( ㉠ )", "short": False, "key": {"ex": "'이 밥을 만든 손을 기억해 주세요'를 넣어, 우리가 무심코 남기는 음식에 많은 사람의 노고가 담겨 있음을 보여 줌. / 농부와 조리사의 수고를 언급하여, 학생들 스스로 잔반을 남기지 않도록 행동 변화를 촉구함."}},
                {"id": "q1-2", "label": "(나) 이미지 ( ㉡ )", "short": False, "key": {"ex": "농부, 조리사, 학생의 손을 나란히 배치하여, 밥 한 끼가 우리에게 오기까지의 과정을 보여 줌. / 거친 손과 부드러운 손을 대조적으로 보여주어, 버려지는 음식에 대한 죄책감과 감사함을 느끼게 함."}}
            ]
        },
        "q2": {
            "items": [
                {"id": "q2-1", "label": "(가)의 관점", "short": False, "key": {"ex": "광고는 잔반을 수많은 자원의 낭비로 본다. 왜냐하면 산처럼 쌓인 밥 이미지 때문이다."}},
                {"id": "q2-2", "label": "(가)의 의도", "short": False, "key": {"ex": "제작자는 광고를 본 사람이 음식을 남기지 않고 다 먹게 하려 한다."}},
                {"id": "q2-3", "label": "(나)의 관점", "short": False, "key": {"ex": "광고는 잔반을 수많은 사람의 노고와 정성을 버리는 행위로 본다. 왜냐하면 농부와 조리사의 거친 손 이미지 때문이다."}},
                {"id": "q2-4", "label": "(나)의 의도", "short": False, "key": {"ex": "제작자는 광고를 본 사람이 음식을 남기지 않고 다 먹게 하려 한다."}}
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
        "q1": {
            "rowA": {"t": "'당신의 발소리'를 '천장을 흔드는 것'이라고 말하여, 내게는 작은 소리가 아래층에서는 집을 흔드는 큰 소리가 된다는 것을 보여 줌.", "i": "위층의 발자국을 아래층 학생의 머리 위 그림자로 만들어, 소리가 아래층 사람을 누르는 무게가 된다는 것을 보여 줌."},
            "items": [
                {"id": "q1-1", "label": "(나) 문구 ( ㉠ )", "short": False, "key": {"ex": "'슬리퍼 한 켤레면 됩니다'라고 하여, 층간소음이라는 큰 문제가 슬리퍼를 신는 작은 실천으로 쉽게 해결될 수 있음을 보여 줌. / 쉬운 해결책을 직접적으로 제시하여, 이웃을 위해 즉시 슬리퍼를 신도록 실천을 유도함."}},
                {"id": "q1-2", "label": "(나) 이미지 ( ㉡ )", "short": False, "key": {"ex": "푹신해 보이는 슬리퍼와 그 안으로 들어가는 발을 크게 배치하여, 층간소음을 줄이기 위한 구체적이고 즉각적인 행동을 보여 줌. / 따뜻하고 푹신한 이미지를 통해 층간소음 방지가 이웃을 향한 배려임을 느끼게 함."}}
            ]
        },
        "q2": {
            "items": [
                {"id": "q2-1", "label": "(가)의 관점", "short": False, "key": {"ex": "광고는 층간소음을 이웃에게 고통을 주는 무거운 폭력으로 본다. 왜냐하면 학생을 짓누르는 거대한 발자국 그림자 이미지 때문이다."}},
                {"id": "q2-2", "label": "(가)의 의도", "short": False, "key": {"ex": "제작자는 광고를 본 사람이 이웃을 배려하여 실내에서 조용히 걷게 하려 한다."}},
                {"id": "q2-3", "label": "(나)의 관점", "short": False, "key": {"ex": "광고는 층간소음을 작은 실천으로 쉽게 해결할 수 있는 문제로 본다. 왜냐하면 푹신한 슬리퍼 이미지 때문이다."}},
                {"id": "q2-4", "label": "(나)의 의도", "short": False, "key": {"ex": "제작자는 광고를 본 사람이 층간소음 방지를 위해 실내에서 슬리퍼를 신게 하려 한다."}}
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

st.set_page_config(page_title="국어 답안 작성 연습", page_icon="🕵️‍♂️", layout="wide")

# ---------------------------------------------------------------- 커스텀 CSS 디자인
st.markdown("""
<style>
.stMarkdown a.header-anchor, .stMarkdown a.header-anchor svg {
    display: none !important;
    visibility: hidden !important;
}
.stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size: 1.3rem !important;
    font-weight: 800 !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #ff4b4b !important;
    border-bottom: 2px solid #ff4b4b !important;
}
button[data-baseweb="tab"][aria-selected="true"] p {
    color: #ff4b4b !important;
}
div[data-testid="stRadio"] > div {
    display: flex !important;
    flex-direction: row !important;
    gap: 10px !important;
    margin-bottom: 25px !important;
    width: 100% !important;
}
div[data-testid="stRadio"] label {
    flex: 1 !important;
    background-color: #ffffff !important;
    border: 1px solid #ced4da !important;
    border-radius: 8px !important;
    padding: 12px 10px !important;
    justify-content: center !important;
    align-items: center !important;
    cursor: pointer !important;
    margin: 0 !important;
}
div[data-testid="stRadio"] label > div:first-child {
    display: none !important;
}
div[data-testid="stRadio"] label[data-checked="true"] {
    background-color: #1a73e8 !important;
    border-color: #1a73e8 !important;
}
div[data-testid="stRadio"] label[data-checked="true"] p {
    color: #ffffff !important;
    font-weight: bold !important;
}
div[data-testid="InputInstructions"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------- 상태 초기화
ss = st.session_state
if "answers" not in ss: ss.answers = {}
if "graded" not in ss: ss.graded = set()
if "feedbacks" not in ss: ss.feedbacks = {}
if "student" not in ss: ss.student = ""

# ---------------------------------------------------------------- 사이드바 (학습 도우미만 남김)
with st.sidebar:
    st.markdown("<div style='font-size:1.5em; font-weight:bold; margin-bottom:15px;'>📖 개념 길잡이</div>", unsafe_allow_html=True)
    
    with st.expander("📝 1) 시험 범위", expanded=True):
        st.markdown("• 교과서 96-97쪽 본문 (교과서 본문이 출제됩니다)\n• 국어 학습지 전체")
    
    with st.expander("📝 2) 반드시 알아야 할 개념", expanded=True):
        st.markdown("• **재현**: 현실을 재구성했으나 현실과 똑같지 않음. 광고에서는 문구와 이미지로 드러남.")
        st.markdown("• **관점**: 제작자가 대상을 보는 시선.")
        st.markdown("""
        <div style="background-color: #e8f4f8; padding: 10px; border-left: 4px solid #2b6cb0; border-radius: 4px; margin-bottom: 10px;">
            <span style="font-weight: bold; color: #2b6cb0;">[TIP]</span> "( )을/를 ( )으로/로 본다"의 문장 형태로 정리할 수 있음.
        </div>
        """, unsafe_allow_html=True)
        st.markdown("• **의도**: 제작자가 수용자에게 하게 하려는 것.")
        st.markdown("""
        <div style="background-color: #e8f4f8; padding: 10px; border-left: 4px solid #2b6cb0; border-radius: 4px;">
            <span style="font-weight: bold; color: #2b6cb0;">[TIP]</span> "광고를 본 사람이 ( )하게 하려 한다"의 문장 형태로 정리할 수 있음.
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------------- 로컬 채점 로직
def get_local_feedback(answer, label, set_id):
    ans = answer.replace(" ", "")
    if len(ans) < 2:
        return {"status": "error", "msg": "답안이 너무 짧습니다. 의미가 잘 드러나게 문장을 완성해 보세요."}
        
    tip_header = "\n\n**💡 통과를 위한 수정 팁**\n문장의 끝부분만 조건에 맞게 살짝 다듬어 주시면 바로 정답(✅) 처리됩니다.\n"
    
    # 1. 3번 비판적 읽기 - ㉠, ㉡ 단순 빈칸 추리 문항
    if label == "㉠" or label == "㉡":
        if set_id == "set1":
            if label == "㉠":
                words = ["관리", "쪼개", "통제", "효율", "계획", "바쁘", "빈틈", "아껴", "가치", "철저", "활용", "소중", "수단"]
                if any(w in ans for w in words): return {"status": "success", "msg": "주어진 자료를 바탕으로 관점을 아주 정확하게 추리했습니다!"}
                else: return {"status": "error", "msg": "💡 단서 분석이 아쉽습니다. 광고 속 '뛰어가는 학생'과 '1분도 놓치지 않는'이라는 문구를 다시 확인해 보세요. 시간을 여유롭게 둔다는 의미일까요, 아니면 철저하게 관리해야 한다는 의미일까요?"}
            else:
                words = ["휴식", "여유", "쉼", "편안", "충전", "자유", "쉬는", "즐기", "여가"]
                if any(w in ans for w in words): return {"status": "success", "msg": "주어진 자료를 바탕으로 관점을 아주 정확하게 추리했습니다!"}
                else: return {"status": "error", "msg": "💡 단서 분석이 아쉽습니다. '쉬는 시간 15분', '벤치에 앉아 쉬는' 등의 힌트를 바탕으로, 학생이 시간을 어떻게 쓰기를 바라는지 추리해 보세요."}
                
        elif set_id == "set2":
            if label == "㉠":
                words = ["시선", "과시", "자랑", "뽐내", "부러움", "타인", "남들", "도구", "자신감", "우월", "멋", "인기", "잘난"]
                if any(w in ans for w in words): return {"status": "success", "msg": "주어진 자료를 바탕으로 관점을 아주 정확하게 추리했습니다!"}
                else: return {"status": "error", "msg": "💡 단서 분석이 아쉽습니다. '신는 순간, 시선이 달라집니다'라는 문구와 남들이 부러워하며 올려다보는 이미지를 통해, 운동화를 어떤 용도로 보는지 추리해 보세요."}
            else:
                words = ["실용", "편안", "보호", "활동", "운동", "가볍", "도구", "목적", "기능", "건강", "도움", "뛰기"]
                if any(w in ans for w in words): return {"status": "success", "msg": "주어진 자료를 바탕으로 관점을 아주 정확하게 추리했습니다!"}
                else: return {"status": "error", "msg": "💡 단서 분석이 아쉽습니다. 운동장에서 공을 쫓아 뛰는 이미지와 '발이 가벼워집니다'라는 문구를 바탕으로, 운동화의 진짜 역할이 무엇인지 추리해 보세요."}
                
        elif set_id == "set3":
            if label == "㉠":
                words = ["단절", "혼자", "차단", "개인", "도피", "나만", "끄고", "수단", "거리", "집중", "고립", "방음", "피하"]
                if any(w in ans for w in words): return {"status": "success", "msg": "주어진 자료를 바탕으로 관점을 아주 정확하게 추리했습니다!"}
                else: return {"status": "error", "msg": "💡 단서 분석이 아쉽습니다. '세상을 끄고, 나만 남기다'라는 문구와 주변을 흐리게 처리한 이미지를 바탕으로, 이어폰이 타인과 소통하는 것인지 아니면 차단하는 것인지 추리해 보세요."}
            else:
                words = ["연결", "공유", "소통", "함께", "같이", "나눔", "타인", "매개체", "관계", "친밀", "교감", "감정"]
                if any(w in ans for w in words): return {"status": "success", "msg": "주어진 자료를 바탕으로 관점을 아주 정확하게 추리했습니다!"}
                else: return {"status": "error", "msg": "💡 단서 분석이 아쉽습니다. 두 학생이 '같은 노래'를 들으며 함께 웃는 모습을 바탕으로, 이어폰이 타인과의 관계에서 어떤 역할을 하는지 관점을 추리해 보세요."}

    # 2. 1번 재현 방식 (알수, 담겨 등 일상적 서술어 대폭 확장)
    if "문구" in label or "이미지" in label:
        if any(w in ans for w in ["이미지", "그림", "사진", "모습"]) and "문구" in label:
            return {"status": "error", "msg": "💡 문구(글)에 대한 분석을 쓰는 칸인데, 이미지나 그림에 대한 설명이 섞여 있는 것 같아요. 다시 확인해 보세요!"}
        if any(w in ans for w in ["문구", "글씨", "글귀", "텍스트", "문장"]) and "이미지" in label:
            return {"status": "error", "msg": "💡 이미지(그림)에 대한 분석을 쓰는 칸인데, 문구(글)에 대한 설명이 섞여 있는 것 같아요. 다시 확인해 보세요!"}
            
        effect_words = ["보여", "나타", "하게", "주어", "알게", "느끼", "전달", "효과", "위험", "경각심", "촉구", "깨닫", "생각", "유도", "이해", "알려", "강조", "알수", "알아", "드러", "담겨", "의미"]
        if not any(w in ans for w in effect_words):
            tip = tip_header + "> \"...(이)라는 문구/이미지를 넣어, **~라는 것을 보여 줌(알게 함/느끼게 함).**\""
            return {"status": "error", "msg": "조건 누락: 광고의 문구나 이미지만 옮겨 쓰지 말고, 그것이 주는 '효과(의미나 수용자에게 미치는 영향)'를 반드시 서술해 보세요." + tip}
        return {"status": "success", "msg": "문맥과 조건에 맞게 잘 작성했습니다! 훌륭합니다."}
        
    # 3. 2번 관점 검증
    if "관점" in label:
        reason_words = ["때문", "이유", "까닭", "왜냐하면", "보아", "보면", "라서", "므로", "통해", "여서", "어서"]
        view_words = ["본다", "보여", "생각", "여긴", "간주", "의미", "관점", "바라", "로본다", "으로본다", "여긴다"]
        
        has_reason = any(w in ans for w in reason_words)
        has_view = any(w in ans for w in view_words)
        
        if not has_reason and not has_view:
            return {"status": "error", "msg": "💡 조건 누락: 대상을 어떻게 바라보는지(~로 본다), 그리고 그 근거가 무엇인지(~때문이다)를 모두 포함해서 써보세요."}
        elif not has_reason:
            return {"status": "error", "msg": "💡 조건 누락: 관점은 잘 찾았는데, 그렇게 생각한 '근거(이유, ~때문이다 등)'가 빠져 있습니다."}
        elif not has_view:
            return {"status": "error", "msg": "💡 조건 누락: 근거는 좋은데, 그래서 대상을 무엇으로 '보는지(~로 본다, ~라고 생각한다 등)'에 대한 결론이 명확하지 않습니다."}

        if set_id == "set1":
            if not any(w in ans for w in ["위험", "위협", "생명", "사고", "문제", "인식", "차이", "치명", "아찔", "다르", "나쁜", "부정", "조심"]):
                return {"status": "error", "msg": "💡 내용 보완 필요: 문장 형식은 맞지만 내용이 타당하지 않습니다. 스마트폰 보행이 얼마나 '위험'한지, 혹은 운전자와의 '인식 차이'가 어떤지 광고 맥락에 맞게 적어주세요."}
        elif set_id == "set2":
            if not any(w in ans for w in ["낭비", "자원", "쓰레기", "버리", "산", "노고", "정성", "수고", "땀", "노력", "사람", "가치", "농부", "조리사", "귀한", "소중", "손", "감사", "중요"]):
                return {"status": "error", "msg": "💡 내용 보완 필요: 문장 형식은 맞지만 내용이 타당하지 않습니다. 음식물 쓰레기가 어떤 '낭비'인지, 혹은 누구의 '노고(손, 정성)'가 버려지는 것인지, 밥이 얼마나 '귀한' 것인지 적어주세요."}
        elif set_id == "set3":
            if not any(w in ans for w in ["폭력", "고통", "무거", "피해", "스트레스", "짓누르", "천장", "소음", "실천", "해결", "쉽게", "배려", "작은", "간단", "이웃", "심각", "나쁜"]):
                return {"status": "error", "msg": "💡 내용 보완 필요: 문장 형식은 맞지만 내용이 타당하지 않습니다. 층간소음이 이웃에게 어떤 '고통'인지, 혹은 슬리퍼가 얼마나 '쉬운 해결책(실천)'인지 적어주세요."}

        return {"status": "success", "msg": "문장 틀과 내용의 타당성까지 완벽하게 작성했습니다! 훌륭합니다."}

    # 4. 2번 의도 검증
    if label == "(가)의 의도" or label == "(나)의 의도":
        intent_words = ["하려", "하기", "하게", "유도", "목적", "바란다", "원한", "만들려", "의도", "바람", "이끌", "행동"]
        if not any(w in ans for w in intent_words):
            return {"status": "error", "msg": "💡 조건 누락: 제작자가 수용자에게 어떤 행동이나 생각을 '하게 하려는지(~하게 하려 한다, ~가 목적이다 등)'가 명확히 드러나게 써보세요."}

        if set_id == "set1":
            if not any(w in ans for w in ["보지않", "하지않", "주의", "조심", "경각심", "멈추", "스마트폰", "위험", "안전", "앞", "예방", "사고", "넣게", "길", "주위", "주변", "살피", "건너", "주시", "횡단보도"]):
                return {"status": "error", "msg": "💡 내용 보완 필요: 문장 형식은 맞지만 핵심 내용이 아쉽습니다. 사람들이 스마트폰 보행 시 어떻게 하기를 바라는지 맥락에 맞게 적어주세요."}
        elif set_id == "set2":
            if not any(w in ans for w in ["남기지", "다먹", "줄이", "버리지", "감사", "노고", "음식", "잔반", "농부", "조리사", "소중", "귀하게", "고마움", "밥"]):
                return {"status": "error", "msg": "💡 내용 보완 필요: 문장 형식은 맞지만 핵심 내용이 아쉽습니다. 음식을 어떻게 하기를 바라는지 맥락에 맞게 적어주세요."}
        elif set_id == "set3":
            if not any(w in ans for w in ["조용", "배려", "걷게", "뛰지", "슬리퍼", "신게", "실천", "층간소음", "이웃", "피해", "아래층", "사람", "생각"]):
                return {"status": "error", "msg": "💡 내용 보완 필요: 문장 형식은 맞지만 핵심 내용이 아쉽습니다. 이웃을 위해 어떻게 하기를 바라는지 맥락에 맞게 적어주세요."}

        return {"status": "success", "msg": "제작자의 의도와 핵심 내용을 문맥에 맞게 훌륭하게 파악했습니다!"}

    # 5. 3번 비판적 읽기 (원본 광고 의도)
    if "원본 광고의 제작자 의도" in label:
        reason_words = ["때문", "이유", "까닭", "왜냐하면", "보아", "보면", "라서", "므로", "통해", "여서", "어서", "바탕으로"]
        intent_words = ["하려", "하기", "하게", "유도", "목적", "바란다", "원한", "만들려", "의도", "바람", "이끌", "행동", "만든다", "사용", "사게", "사도록", "팔려", "구매", "팔기"]
        
        has_reason = any(w in ans for w in reason_words)
        has_intent = any(w in ans for w in intent_words)
        
        if not has_reason and not has_intent:
            tip = tip_header + "> \"광고를 본 사람이 ... **하게 하려 한다. 왜냐하면** ... 기 **때문이다.**\""
            return {"status": "error", "msg": "조건 누락: 제작자의 의도(~하게 하려 한다)와 그 근거(~때문이다)를 모두 포함해서 써보세요." + tip}
        elif not has_reason:
            tip = tip_header + "> \"... **하게 하려 한다. 왜냐하면** ... 기 **때문이다.**\""
            return {"status": "error", "msg": "조건 누락: 의도는 잘 찾았는데, 광고의 어떤 부분을 보고 그렇게 생각했는지 '근거(~때문이다 등)'가 빠져 있습니다." + tip}
        elif not has_intent:
            tip = tip_header + "> \"광고를 본 사람이 ... **하게 하려 한다.** 왜냐하면...\""
            return {"status": "error", "msg": "조건 누락: 근거는 좋은데, 그래서 결국 수용자가 어떤 생각이나 행동을 '하게 하려는지(~하게 하려 한다 등)'가 명확하지 않습니다." + tip}
        
        rep_words = ["문구", "이미지", "그림", "사진", "모델", "표정", "글귀", "모습", "분위기", "단어", "글씨"]
        has_rep = any(w in ans for w in rep_words)

        context_ok = False
        if set_id == "set1" and any(w in ans for w in ["뛰어", "1분", "시계", "스마트워치", "알림", "학생"]): context_ok = True
        if set_id == "set2" and any(w in ans for w in ["내려다", "시선", "달라", "부러", "운동화", "신발", "학생"]): context_ok = True
        if set_id == "set3" and any(w in ans for w in ["흐리게", "눈을", "세상", "끄고", "나만", "평온", "이어폰", "학생", "표정"]): context_ok = True

        if not (has_rep or context_ok):
            return {"status": "error", "msg": "💡 내용 보완 필요: 의도는 잘 파악했습니다! 다만, 광고의 어떤 '재현 방식(이미지 속 모델의 표정, 특정 문구 등)'을 보고 그렇게 생각했는지 구체적인 근거를 함께 적어주세요."}

        return {"status": "success", "msg": "제작자의 의도와 근거(재현 방식)를 논리적으로 아주 잘 연결했습니다! 훌륭합니다."}
            
    return {"status": "success", "msg": "조건에 맞게 잘 작성했습니다!"}

# ---------------------------------------------------------------- 이미지 렌더러
def get_base64_image(file_name, label):
    img_path = IMG_DIR / file_name
    try:
        with open(img_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
        return f"""
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center; height: 100%; border: 1px solid #e9ecef;">
            <img src="data:image/png;base64,{encoded}" style="max-height: 375px; width: auto; max-width: 100%; border-radius: 5px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 15px;">
            <strong style="display: block; font-size: 1.1em; color: #343a40;">{label}</strong>
        </div>
        """
    except Exception:
        return f"<div style='background-color: #f8f9fa; padding: 20px; text-align: center; border-radius: 10px;'><strong style='color: #343a40;'>{label}</strong><br>이미지 로드 대기 중...</div>"

# ---------------------------------------------------------------- 상단 디자인
st.markdown("<div style='font-size: 2em; font-weight: bold; margin-bottom: 0.2em;'>🕵️‍♂️ [국어] 답안 작성 연습</div>", unsafe_allow_html=True)
st.markdown("<div style='font-size: 1.2em; color: #555; margin-bottom: 1em;'>작성한 답안을 입력한 뒤 문제의 조건에 맞게 작성하였는지 확인하세요.</div>", unsafe_allow_html=True)

# 학생 정보란을 메인 화면으로 이동
with st.container():
    st.markdown("<div style='font-size:1.2em; font-weight:bold; margin-bottom:5px;'>👤 학생 정보 입력</div>", unsafe_allow_html=True)
    st.caption("자신의 학번과 이름을 정확히 입력해야 채점 결과가 누적 기록됩니다.")
    ss.student = st.text_input("학번과 이름", value=ss.student, placeholder="예: 20100 조중이", label_visibility="collapsed")
st.write("")

completed = len(ss.graded)
st.progress(completed / 9.0)
st.markdown(f"**이번 회차 내가 푼 문제 : {completed}/9**")
st.write("")

# ---------------------------------------------------------------- 구글 시트 연동 및 데이터 가공
def log_action_to_sheet(set_id, qkey, label, answer_text, fb_status, fb_msg):
    if "gcp_service_account" not in st.secrets or "SHEET_URL" not in st.secrets:
        return
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        info = dict(st.secrets["gcp_service_account"])
        creds = Credentials.from_service_account_info(info, scopes=["https://www.googleapis.com/auth/spreadsheets"])
        sh = gspread.authorize(creds).open_by_url(st.secrets["SHEET_URL"])
        ws = sh.sheet1
        ws.append_row([f"{dt.datetime.now():%Y-%m-%d %H:%M:%S}", ss.student, f"[{set_id.upper()}] {qkey}", label, answer_text, fb_status, fb_msg])
    except Exception:
        pass

def fetch_and_process_history(student_name):
    if not student_name or "gcp_service_account" not in st.secrets or "SHEET_URL" not in st.secrets:
        return []
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        info = dict(st.secrets["gcp_service_account"])
        creds = Credentials.from_service_account_info(info, scopes=["https://www.googleapis.com/auth/spreadsheets"])
        sh = gspread.authorize(creds).open_by_url(st.secrets["SHEET_URL"])
        ws = sh.sheet1
        all_data = ws.get_all_values()
        
        parsed = []
        for row in all_data:
            if len(row) >= 5 and row[1] == student_name:
                t = row[0]
                raw_q = row[2]
                label = row[3]
                ans = row[4]
                status = row[5] if len(row) > 5 else "unknown"
                msg = row[6] if len(row) > 6 else ""
                
                set_num = raw_q.split("]")[0].replace("[SET", "")
                q_num = raw_q.split(" ")[1].replace("q", "")
                
                set_name = f"[실전 적용 {set_num}]"
                q_names = {"1": "1. 재현 방식", "2": "2. 관점과 의도", "3": "3. 비판적 읽기"}
                q_name = q_names.get(q_num, f"{q_num}번 문항")
                
                full_q_name = f"{set_name} {q_name}"
                
                parsed.append({
                    "time": t,
                    "set_id": int(set_num) if set_num.isdigit() else 99,
                    "q_id": int(q_num) if q_num.isdigit() else 99,
                    "full_q_name": full_q_name,
                    "label": label,
                    "ans": ans,
                    "status": status,
                    "msg": msg
                })
                
        parsed.sort(key=lambda x: x["time"])
        attempts = {}
        for p in parsed:
            key = (p["full_q_name"], p["label"])
            attempts[key] = attempts.get(key, 0) + 1
            p["attempt"] = attempts[key]
            
        parsed.sort(key=lambda x: (x["set_id"], x["q_id"], x["label"], x["attempt"]))
        return parsed
        
    except Exception:
        return []

# ---------------------------------------------------------------- UI 컴포넌트
def cond_box(lines, template_lines=None):
    body = "<br>".join(f"• {ln}" for ln in lines)
    temp_box = ""
    if template_lines:
        temp_body = "<br>".join(f"- {t}" for t in template_lines)
        temp_box = f"<div style='background-color: #ffffff; border: 1px solid #ced4da; padding: 10px; margin-top: 10px; border-radius: 5px; color: #495057;'>{temp_body}</div>"
        
    st.markdown(f"""
    <div style="background-color: #f8f9fa; border-left: 4px solid #4a90e2; padding: 15px; margin-bottom: 20px; border-radius: 5px;">
        <strong style="color: #4a90e2;">&lt;조건&gt;</strong><br>
        <span style="font-size: 0.95em;">{body}</span>
        {temp_box}
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------------- 네비게이션
tabs = st.tabs(["🔎 [실전 적용 1]", "🔎 [실전 적용 2]", "🔎 [실전 적용 3]", "📚 학습 기록"])

for i, tab in enumerate(tabs[:3]):
    with tab:
        s = SETS[i]
        
        q_choice = st.radio(f"문항 선택 ({s['id']})", ["✏️ 1. 재현 방식", "✏️ 2. 관점과 의도", "✏️ 3. 비판적 읽기"], horizontal=True, label_visibility="collapsed")
        
        if q_choice == "✏️ 1. 재현 방식":
            c1, c2 = st.columns(2)
            c1.markdown(get_base64_image(s["adA"], "(가)"), unsafe_allow_html=True)
            c2.markdown(get_base64_image(s["adB"], "(나)"), unsafe_allow_html=True)
            st.write("")
            
            q = s["q1"]
            k_q = f"{s['id']}-q1"
            st.markdown("<div style='font-size:1.3em; font-weight:bold; margin-bottom:10px;'>1. 재현 방식</div>", unsafe_allow_html=True)
            st.write("두 광고의 재현 방식을 표로 정리하였다. ㉠~㉡에 들어갈 내용을 쓰시오.")
            st.markdown(f"""
            <table style="width:100%; border-collapse: collapse; text-align: left; margin-bottom: 20px;">
              <tr style="background-color: #f1f3f5; border-bottom: 2px solid #dee2e6;">
                <th style="padding: 12px; border: 1px solid #dee2e6; width: 10%;"></th>
                <th style="padding: 12px; border: 1px solid #dee2e6; width: 45%;">문구</th>
                <th style="padding: 12px; border: 1px solid #dee2e6; width: 45%;">이미지</th>
              </tr>
              <tr>
                <td style="padding: 12px; border: 1px solid #dee2e6; font-weight: bold; background-color: #f8f9fa; text-align: center;">(가)</td>
                <td style="padding: 12px; border: 1px solid #dee2e6;">{q['rowA']['t']}</td>
                <td style="padding: 12px; border: 1px solid #dee2e6;">{q['rowA']['i']}</td>
              </tr>
              <tr>
                <td style="padding: 12px; border: 1px solid #dee2e6; font-weight: bold; background-color: #f8f9fa; text-align: center;">(나)</td>
                <td style="padding: 12px; border: 1px solid #dee2e6; color: #495057;">( ㉠ )</td>
                <td style="padding: 12px; border: 1px solid #dee2e6; color: #495057;">( ㉡ )</td>
              </tr>
            </table>
            """, unsafe_allow_html=True)
            cond_box(["광고 문구·이미지와 그 효과를 서술할 것 (표현상의 효과, 수용자에게 미치는 효과 모두 인정)."])
            
            inputs = {}
            for it in q["items"]:
                k_it = f"{k_q}-{it['id']}"
                inputs[k_it] = st.text_area(f"**{it['label']}**", value=ss.answers.get(k_it, ""), key=f"w-{k_it}", placeholder="내용을 입력하세요", height=100)
            
            st.write("")
            col1, col2, col3 = st.columns([2, 1.5, 1])
            with col3:
                submit_btn = st.button("🚀 제출하고 피드백 받기", key=f"btn-{k_q}", type="primary", use_container_width=True)
                
            if submit_btn:
                if not ss.student.strip():
                    st.error("상단에 학번과 이름을 먼저 입력해주세요!")
                elif all(v.strip() for v in inputs.values()):
                    for it in q["items"]:
                        k_it = f"{k_q}-{it['id']}"
                        ss.answers[k_it] = inputs[k_it]
                        fb = get_local_feedback(inputs[k_it], it['label'], s['id'])
                        ss.feedbacks[k_it] = fb
                        log_action_to_sheet(s['id'], "q1", it['label'], inputs[k_it], fb["status"], fb["msg"])
                    ss.graded.add(k_q)
                else:
                    st.warning("⚠️ 모든 빈칸에 내용을 입력하세요.")

            if k_q in ss.graded:
                for it in q["items"]:
                    k_it = f"{k_q}-{it['id']}"
                    fb = ss.feedbacks[k_it]
                    st.markdown(f"**[{it['label']}] 채점 결과**")
                    if fb["status"] == "success":
                        st.success(f"✅ {fb['msg']}")
                    else:
                        st.error(f"{fb['msg']}")
                    with st.expander("👀 모범 답안 보기"):
                        st.info(it['key']['ex'])
            
        elif q_choice == "✏️ 2. 관점과 의도":
            c1, c2 = st.columns(2)
            c1.markdown(get_base64_image(s["adA"], "(가)"), unsafe_allow_html=True)
            c2.markdown(get_base64_image(s["adB"], "(나)"), unsafe_allow_html=True)
            st.write("")
            
            q = s["q2"]
            k_q = f"{s['id']}-q2"
            st.markdown("<div style='font-size:1.3em; font-weight:bold; margin-bottom:10px;'>2. 관점과 의도</div>", unsafe_allow_html=True)
            st.write("두 광고에 담긴 제작자의 관점과 의도를 <조건>에 맞게 서술하시오.")
            cond_box(
                ["광고에 재현된 내용에서 찾은 근거를 포함하여 기술할 것.", "아래 문장 틀에 맞추어 쓸 것. (단, 의도를 작성할 때는 이유를 쓰지 않아도 됨.)"],
                ["관점: 광고는 ( )을/를 ( )로/으로 본다. 왜냐하면 ( ) 때문이다.", "의도: 제작자는 광고를 본 사람이 ( )하게 하려 한다."]
            )
            
            inputs = {}
            for it in q["items"]:
                k_it = f"{k_q}-{it['id']}"
                inputs[k_it] = st.text_area(f"**{it['label']}**", value=ss.answers.get(k_it, ""), key=f"w-{k_it}", placeholder="내용을 입력하세요", height=80)
            
            st.write("")
            col1, col2, col3 = st.columns([2, 1.5, 1])
            with col3:
                submit_btn = st.button("🚀 제출하고 피드백 받기", key=f"btn-{k_q}", type="primary", use_container_width=True)
                
            if submit_btn:
                if not ss.student.strip():
                    st.error("상단에 학번과 이름을 먼저 입력해주세요!")
                elif all(v.strip() for v in inputs.values()):
                    for it in q["items"]:
                        k_it = f"{k_q}-{it['id']}"
                        ss.answers[k_it] = inputs[k_it]
                        fb = get_local_feedback(inputs[k_it], it['label'], s['id'])
                        ss.feedbacks[k_it] = fb
                        log_action_to_sheet(s['id'], "q2", it['label'], inputs[k_it], fb["status"], fb["msg"])
                    ss.graded.add(k_q)
                else:
                    st.warning("⚠️ 모든 빈칸에 내용을 입력하세요.")

            if k_q in ss.graded:
                for it in q["items"]:
                    k_it = f"{k_q}-{it['id']}"
                    fb = ss.feedbacks[k_it]
                    st.markdown(f"**[{it['label']}] 채점 결과**")
                    if fb["status"] == "success":
                        st.success(f"✅ {fb['msg']}")
                    else:
                        st.error(f"{fb['msg']}")
                    with st.expander("👀 모범 답안 보기"):
                        st.info(it['key']['ex'])
            
        else:
            q = s["q3"]
            k_q = f"{s['id']}-q3"
            st.markdown("<div style='font-size:1.3em; font-weight:bold; margin-bottom:10px;'>3. 비판적 읽기</div>", unsafe_allow_html=True)
            
            col_ad, col_think = st.columns([1, 1.2])
            with col_ad:
                st.markdown(get_base64_image(s["adC"], "[광고]"), unsafe_allow_html=True)
            with col_think:
                st.markdown(f"""
                <div style="background-color: #fcf8e3; padding: 20px; border-radius: 8px; border-left: 5px solid #f0ad4e; height: 100%;">
                    <strong style="color: #d9831f; font-size: 1.1em;">[학생의 사고 과정]</strong><br><br>
                    {q['buy']}<br><br>{q['think1']}<br><br>{q['think2']}
                </div>
                """, unsafe_allow_html=True)
            st.write("")
            
            st.markdown("**(1) ㉠, ㉡에 들어가기에 적절한 표현을 쓰시오.**")
            inputs = {}
            for it in q["items"][:2]:
                k_it = f"{k_q}-{it['id']}"
                inputs[k_it] = st.text_input(f"**{it['label']}**", value=ss.answers.get(k_it, ""), key=f"w-{k_it}", placeholder="내용을 입력하세요")
            st.write("")
            
            st.markdown("**(2) 위 광고에 담긴 제작자의 의도를 재현 방법을 근거로 들어 서술하시오.**")
            cond_box(
                ["광고에 재현된 내용에서 찾은 근거를 포함하여 기술할 것.", "아래 문장 틀에 맞추어 쓸 것."],
                ["의도: 제작자는 광고를 본 사람이 ( )하게 하려 한다. 왜냐하면 ( ) 때문이다."]
            )
            it = q["items"][2]
            k_it = f"{k_q}-{it['id']}"
            inputs[k_it] = st.text_area(f"**{it['label']}**", value=ss.answers.get(k_it, ""), key=f"w-{k_it}", placeholder="내용을 입력하세요", height=100)
            
            st.write("")
            col1, col2, col3 = st.columns([2, 1.5, 1])
            with col3:
                submit_btn = st.button("🚀 제출하고 피드백 받기", key=f"btn-{k_q}", type="primary", use_container_width=True)
                
            if submit_btn:
                if not ss.student.strip():
                    st.error("상단에 학번과 이름을 먼저 입력해주세요!")
                elif all(v.strip() for v in inputs.values()):
                    for i_it in q["items"]:
                        k_id = f"{k_q}-{i_it['id']}"
                        ss.answers[k_id] = inputs[k_id]
                        fb = get_local_feedback(inputs[k_id], i_it['label'], s['id'])
                        ss.feedbacks[k_id] = fb
                        log_action_to_sheet(s['id'], "q3", i_it['label'], inputs[k_id], fb["status"], fb["msg"])
                    ss.graded.add(k_q)
                else:
                    st.warning("⚠️ 모든 빈칸에 내용을 입력하세요.")

            if k_q in ss.graded:
                for i_it in q["items"]:
                    k_id = f"{k_q}-{i_it['id']}"
                    fb = ss.feedbacks[k_id]
                    st.markdown(f"**[{i_it['label']}] 채점 결과**")
                    if fb["status"] == "success":
                        st.success(f"✅ {fb['msg']}")
                    else:
                        st.error(f"{fb['msg']}")
                    with st.expander("👀 모범 답안 보기"):
                        st.info(i_it['key']['ex'])

# ---------------------------------------------------------------- 학습 기록 탭
with tabs[3]:
    st.markdown("<div style='font-size:1.5em; font-weight:bold; margin-bottom:10px;'>📝 누적 학습 기록</div>", unsafe_allow_html=True)
    st.caption("구글 스프레드시트에 안전하게 보관된 회차별 누적 학습 기록을 불러옵니다.")
    
    if not ss.student:
        st.warning("⚠️ 상단에 학번과 이름을 입력하셔야 누적 학습 기록을 조회할 수 있습니다.")
    else:
        if st.button("📥 내 이전 기록 모두 불러오기", type="primary"):
            with st.spinner("과거 기록을 정리해서 가져오는 중입니다..."):
                history_data = fetch_and_process_history(ss.student)
                
            if not history_data:
                st.info("아직 저장된 학습 기록이 없습니다. 문제를 풀고 제출해 보세요!")
            else:
                st.success(f"성공적으로 불러왔습니다! 문항 번호 순으로 과거 제출 내역을 보여줍니다.")
                st.divider()
                
                current_q = None
                for item in history_data:
                    if current_q != item['full_q_name']:
                        st.markdown(f"<div style='font-size:1.3em; font-weight:bold; margin-top:20px; margin-bottom:10px;'>📚 {item['full_q_name']}</div>", unsafe_allow_html=True)
                        current_q = item['full_q_name']
                        
                    st.markdown(f"**[{item['label']}] - {item['attempt']}회 응시**")
                    
                    col_ans, col_stat = st.columns([4, 1])
                    with col_ans:
                        st.info(f"**나의 답안:** {item['ans']}")
                        if item['msg']:
                            if item['status'] == "success":
                                st.success(f"**피드백:**\n\n{item['msg']}")
                            else:
                                st.error(f"**피드백:**\n\n{item['msg']}")
                    with col_stat:
                        if item['status'] == "success":
                            st.success("✅ 조건 충족")
                        elif item['status'] == "error":
                            st.error("💡 보완 필요")
                        else:
                            st.warning("결과 없음")
                            
                    st.write("")
                st.divider()
