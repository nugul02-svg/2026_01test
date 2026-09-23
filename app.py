# -*- coding: utf-8 -*-
"""서논술형 답안 연습 — 광고·홍보물의 재현과 관점 (Streamlit)

실행:  streamlit run app.py
비밀값(.streamlit/secrets.toml 또는 Streamlit Cloud의 Secrets):
  ANTHROPIC_API_KEY = "sk-ant-..."
  MODEL = "claude-sonnet-4-6"          # 생략 가능
  SHEET_URL = "[https://docs.google.com/spreadsheets/d/](https://docs.google.com/spreadsheets/d/)..."   # 구글 시트 연동 시
  [gcp_service_account]                 # 구글 시트 연동 시 (서비스 계정 JSON 내용)
  type = "service_account"
  ...
"""
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
            "buy": "
