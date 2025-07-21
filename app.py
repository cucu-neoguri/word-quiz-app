import streamlit as st
import random

# 단어 저장 구조
if 'wordbook' not in st.session_state:
    st.session_state.wordbook = {}

st.title("📘 영어 단어 퀴즈 프로그램")

# 단어 추가
st.header("1. 단어 추가")
group = st.text_input("단어장 이름", key="group")
english = st.text_input("영어 단어", key="english")
korean = st.text_input("한글 뜻", key="korean")
if st.button("단어 추가"):
    if group and english and korean:
        word = {"english": english.strip(), "korean": korean.strip(), "flagged": False}
        st.session_state.wordbook.setdefault(group, []).append(word)
        st.success(f"{english} 단어가 '{group}' 단어장에 추가되었습니다.")
    else:
        st.warning("모든 항목을 입력해주세요.")

# 단어장 목록 보기
st.header("2. 단어 보기")
for group, words in st.session_state.wordbook.items():
    st.subheader(f"📘 {group}")
    for word in sorted(words, key=lambda w: w['english'].lower()):
        flag = "★" if word["flagged"] else ""
        st.write(f"{flag} {word['english']} - {word['korean']}")

# 한글 뜻 퀴즈
st.header("3. 뜻 맞히기 퀴즈")
quiz_group = st.selectbox("단어장 선택", list(st.session_state.wordbook.keys()) if st.session_state.wordbook else [])
if st.button("퀴즈 시작") and quiz_group:
    question = random.choice(st.session_state.wordbook[quiz_group])
    options = [question['korean']]
    while len(options) < 4:
        other = random.choice(st.session_state.wordbook[quiz_group])['korean']
        if other not in options:
            options.append(other)
    random.shuffle(options)
    st.write(f"영어: **{question['english']}**")
    choice = st.radio("정답을 고르세요:", options)
    if st.button("제출"):
        if choice == question['korean']:
            st.success("정답입니다!")
        else:
            st.error(f"틀렸습니다. 정답은 {question['korean']}입니다.")
