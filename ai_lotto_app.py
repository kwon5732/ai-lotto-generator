import streamlit as st
import random

st.title("🎯 AI 로또 번호 생성기")

def generate_numbers():
    return sorted(random.sample(range(1, 46), 6))

if "numbers" not in st.session_state:
    st.session_state.numbers = []

if st.button("번호 생성하기"):
    new_numbers = generate_numbers()
    st.session_state.numbers.append(new_numbers)

st.subheader("📌 생성된 번호 목록")
for i, nums in enumerate(st.session_state.numbers[::-1], 1):
    st.write(f"{i}. {nums}")
