# -*- coding: utf-8 -*-
"""서논술형 답안 연습 — 광고·홍보물의 재현과 관점 (Streamlit)"""

import json
import re
import datetime as dt
from pathlib import Path

import streamlit as st

# 데이터 통합
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
        PAGES.append({"id": f"{s['id']}-{qk}", "set": s, "qkey": qk,
                      "tab": f"{si}-{qi}", "name": f"{si}번 세트 – 서·논술형 {qi}"})
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
        qdesc = ("[문항] 서·논술형 2. 두 광고에 담긴 제작자의 관점과 의도를 서술한다. 문장 틀: 관점은 \"( )을/를 ( )로/으로 본다. "
                 "그렇게 생각한 이유는 ( ) 때문이다.\", 의도는 \"제작자는 광고를 본 사람이 ( )하게 하려 한다.\" "
                 "관점의 둘째 괄호에는 사물 이름이 아니라 그 사물이 뜻하는 성질·가치를 써야 한다.")
        ad = s["adText"]["A"] + "\n" + s["adText"]["B"]
    else:
        qdesc = (f"[문항] 서·논술형 3. 광고를 비판적으로 읽는 학생의 사고 과정이다. \"{q['think1']}\" \"{q['think2']}\" "
                 f"㉠·㉡에는 광고 속 {q['obj']}을/를 무엇으로 보는지(성질·가치)를 쓴다. (2)는 수정 전 광고에 담긴 제작자의 의도를 "
                 "문장 틀 \"광고를 본 사람이 ( )하게 하려 한다. 그렇게 생각한 이유는 ( ) 때문이다.\"에 맞추어 쓰되, "
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
        raise RuntimeError("ANTHROPIC_API_KEY가 설정되지 않았습니다.")
    model = secret("MODEL", "claude-sonnet-4-6")
    msg = client.messages.create(model=model, max_tokens=1200,
                                 messages=[{"role": "user", "content": prompt}])
    text = "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")
    text = text.replace("```json", "").replace("
