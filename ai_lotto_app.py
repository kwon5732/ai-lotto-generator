# ai_lotto_app.py
import streamlit as st
import random
from datetime import datetime

st.set_page_config(page_title="AI 로또 전략 생성기", layout="centered")
st.title("AI 전략 기반 로또 번호 생성기")

# 자동 생성 시 1회만 실행되도록 세션 체크
if "auto_generated" not in st.session_state:
    st.session_state.auto_generated = False

# 저장 목록 초기화
if "history" not in st.session_state:
    st.session_state.history = []

# 전략 설정 입력
st.sidebar.header("맞춤 전략 설정")
odd_even_option = st.sidebar.selectbox("홀짝 비율", ["무작위", "3:3", "4:2", "2:4"])
include_40s = st.sidebar.checkbox("40번대 포함", value=True)
avoid_consecutive = st.sidebar.checkbox("연속 숫자 피하기", value=True)
require_unique_ends = st.sidebar.checkbox("끝자리 다양성 확보", value=True)
wide_range = st.sidebar.checkbox("숫자 범위 넓히기", value=True)

def generate_lotto():
    all_numbers = list(range(1, 46))
    random.shuffle(all_numbers)

    while True:
        numbers = sorted(random.sample(all_numbers, 6))

        # 전략 조건 검사
        odd = sum(1 for n in numbers if n % 2 == 1)
        even = 6 - odd
        has_40s = any(n >= 40 for n in numbers)
        has_consecutive = any(numbers[i] + 1 == numbers[i+1] for i in range(5))
        unique_ends = len(set(n % 10 for n in numbers)) >= 5
        spread = max(numbers) - min(numbers) > 25

        # 전략 필터 적용
        if odd_even_option == "3:3" and odd != 3: continue
        if odd_even_option == "4:2" and odd != 4: continue
        if odd_even_option == "2:4" and odd != 2: continue
        if include_40s and not has_40s: continue
        if avoid_consecutive and has_consecutive: continue
        if require_unique_ends and not unique_ends: continue
        if wide_range and not spread: continue

        return numbers, {
            "홀짝 비율": f"{odd}홀/{even}짝",
            "40번대 포함 여부": "포함" if has_40s else "없음",
            "연속 숫자": "없음" if not has_consecutive else "포함됨",
            "끝자리 다양성": "우수" if unique_ends else "부족",
            "숫자 분산": "넓게 분포됨" if spread else "좁게 몰림"
        }

# 자동 1회 생성
if not st.session_state.auto_generated:
    numbers, strategy = generate_lotto()
    st.session_state.current = (numbers, strategy)
    st.session_state.auto_generated = True
    st.session_state.history.append((datetime.now(), numbers, strategy))

if st.button("새 번호 추천받기"):
    numbers, strategy = generate_lotto()
    st.session_state.current = (numbers, strategy)
    st.session_state.history.append((datetime.now(), numbers, strategy))

# 출력
if "current" in st.session_state:
    numbers, strategy = st.session_state.current
    st.subheader("추천 번호")
    st.write(" ".join(f"{n:02d}" for n in numbers))

    st.subheader("적용된 전략")
    for k, v in strategy.items():
        st.write(f"- **{k}**: {v}")

# 저장된 번호 내역
if st.session_state.history:
    st.subheader("내역")
    for i, (dt, nums, strat) in enumerate(reversed(st.session_state.history[-10:]), 1):
        st.markdown(f"{i}. {dt.strftime('%Y-%m-%d %H:%M:%S')} → " +
                    " ".join(f"{n:02d}" for n in nums))
streamlit
