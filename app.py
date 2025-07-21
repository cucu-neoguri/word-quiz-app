import streamlit as st
import random

# ----------------- 사용자 로그인 -------------------
st.title("📘 영어 단어 퀴즈 프로그램")

username = st.text_input("사용자 이름을 입력하세요")
if not username:
    st.warning("사용자 이름을 먼저 입력해 주세요.")
    st.stop()

# ----------------- 사용자별 단어장 및 오답 저장 구조 -------------------
if 'wordbook' not in st.session_state:
    st.session_state.wordbook = {}
if 'wrong_answers' not in st.session_state:
    st.session_state.wrong_answers = {}
if username not in st.session_state.wordbook:
    st.session_state.wordbook[username] = {}
if username not in st.session_state.wrong_answers:
    st.session_state.wrong_answers[username] = []

user_wordbook = st.session_state.wordbook[username]
user_wrong = st.session_state.wrong_answers[username]

# ----------------- 단어 추가 -------------------
st.header("1. 단어 추가")
group = st.text_input("단어장 이름", key="group")
english = st.text_input("영어 단어", key="english")
korean = st.text_input("한글 뜻", key="korean")

if st.button("단어 추가"):
    if group and english and korean:
        word = {"english": english.strip(), "korean": korean.strip(), "flagged": False}
        user_wordbook.setdefault(group, []).append(word)
        st.success(f"'{english}' 단어가 '{group}' 단어장에 추가되었습니다.")
    else:
        st.warning("모든 항목을 입력해 주세요.")

# ----------------- 단어 보기 -------------------
st.header("2. 단어 보기")
if not user_wordbook:
    st.info("등록된 단어가 없습니다.")
else:
    for group in sorted(user_wordbook.keys()):
        st.subheader(f"📘 {group}")
        for i, word in enumerate(sorted(user_wordbook[group], key=lambda w: w['english'].lower())):
            flag = "★" if word["flagged"] else ""
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{flag} {word['english']}** - {word['korean']}")
            with col2:
                if st.button("★ 토글", key=f"flag_{group}_{i}_{username}"):
                    word["flagged"] = not word["flagged"]

# ----------------- 테스트 종류 선택 -------------------
st.header("3. 단어 테스트")
if not user_wordbook:
    st.info("단어장을 먼저 추가해 주세요.")
else:
    selected_group = st.selectbox("단어장 선택", list(user_wordbook.keys()), key="quiz_group")
    test_type = st.radio("테스트 종류를 선택하세요:", ["한글 뜻 선택 테스트", "영어 스펠링 입력 테스트"])

    if st.button("테스트 시작"):
        if not user_wordbook[selected_group]:
            st.warning("선택한 단어장에 단어가 없습니다.")
        else:
            question = random.choice(user_wordbook[selected_group])

            if test_type == "한글 뜻 선택 테스트":
                options = [question['korean']]
                while len(options) < 4:
                    other = random.choice(user_wordbook[selected_group])['korean']
                    if other not in options:
                        options.append(other)
                random.shuffle(options)

                st.subheader(f"영어 단어: {question['english']}")
                choice = st.radio("뜻을 선택하세요:", options, key="korean_options")
                if st.button("제출", key="submit_korean"):
                    if choice == question['korean']:
                        st.success("정답입니다!")
                    else:
                        st.error(f"틀렸습니다. 정답은 '{question['korean']}'입니다.")
                        user_wrong.append(question)

            elif test_type == "영어 스펠링 입력 테스트":
                st.subheader(f"뜻: {question['korean']}")
                user_input = st.text_input("영어 스펠링을 입력하세요", key="spelling_input")
                if st.button("제출", key="submit_spelling"):
                    if user_input.strip().lower() == question['english'].lower():
                        st.success("정답입니다!")
                    else:
                        st.error(f"틀렸습니다. 정답은 '{question['english']}'입니다.")
                        user_wrong.append(question)

# ----------------- 오답 복습 -------------------
st.header("4. 오답 복습")
if not user_wrong:
    st.info("오답이 없습니다. 테스트를 먼저 진행해 보세요.")
else:
    review_question = random.choice(user_wrong)
    st.subheader(f"뜻: {review_question['korean']}")
    review_input = st.text_input("영어 스펠링을 입력하세요 (오답 복습)", key="review_input")
    if st.button("제출", key="submit_review"):
        if review_input.strip().lower() == review_question['english'].lower():
            st.success("정답입니다! 오답 목록에서 제거됩니다.")
            user_wrong.remove(review_question)
        else:
            st.error(f"틀렸습니다. 정답은 '{review_question['english']}'입니다.")
