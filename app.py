import streamlit as st
import random

# 앱 제목 설정
st.title("🔢 숫자 맞추기 게임")
st.write("1부터 100 사이의 숫자를 맞춰보세요!")

# 1. 게임 초기화 (오류 방지를 위해 세션 상태 확인)
if 'target_number' not in st.session_state:
    st.session_state.target_number = random.randint(1, 100)
    st.session_state.count = 0
    st.session_state.game_over = False

# 2. 사용자 입력 창
user_guess = st.number_input("숫자를 입력하세요", min_value=1, max_value=100, step=1)
submit_button = st.button("확인")

# 3. 게임 로직
if submit_button and not st.session_state.game_over:
    st.session_state.count += 1
    
    if user_guess < st.session_state.target_number:
        st.warning("더 큰 숫자입니다! ↑")
    elif user_guess > st.session_state.target_number:
        st.warning("더 작은 숫자입니다! ↓")
    else:
        st.success(f"정답입니다! 🎉 {st.session_state.count}번 만에 맞추셨네요.")
        st.session_state.game_over = True
        st.balloons() # 축하 효과

# 4. 다시 시작 버튼
if st.session_state.game_over:
    if st.button("게임 다시 시작"):
        # 상태 초기화
        del st.session_state.target_number
        st.rerun()
