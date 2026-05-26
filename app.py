import streamlit as st
import random
import time

st.set_page_config(page_title="Memory Game", layout="centered")

# 1. 초기 세션 상태 설정
if 'sequence' not in st.session_state:
    st.session_state.sequence = [random.randint(1, 9) for _ in range(3)] # 시작은 3개
    st.session_state.user_input = []
    st.session_state.showing = True
    st.session_state.score = 0

st.title("🧠 순서 기억하기 게임")
st.write(f"**현재 점수: {st.session_state.score}**")

# 2. 숫자 보여주기 단계
if st.session_state.showing:
    placeholder = st.empty()
    placeholder.info("숫자 순서를 잘 기억하세요!")
    time.sleep(1)
    
    for num in st.session_state.sequence:
        placeholder.metric("숫자", num)
        time.sleep(0.8)
        placeholder.empty()
        time.sleep(0.2)
        
    st.session_state.showing = False
    st.rerun()

# 3. 사용자 입력 단계
st.subheader("기억한 숫자를 순서대로 누르세요!")
cols = st.columns(3)

for i in range(1, 10):
    if cols[(i-1)%3].button(f"{i}", key=f"btn_{i}", use_container_width=True):
        st.session_state.user_input.append(i)
        
        # 정답 체크
        current_step = len(st.session_state.user_input) - 1
        if st.session_state.user_input[current_step] != st.session_state.sequence[current_step]:
            st.error(f"틀렸습니다! 최종 점수: {st.session_state.score}")
            if st.button("다시 도전"):
                st.session_state.clear()
                st.rerun()
            st.stop()
            
        # 모든 단계를 맞췄을 때
        if len(st.session_state.user_input) == len(st.session_state.sequence):
            st.success("통과! 다음 단계로 이동합니다.")
            st.session_state.score += 1
            st.session_state.sequence.append(random.randint(1, 9))
            st.session_state.user_input = []
            st.session_state.showing = True
            time.sleep(1)
            st.rerun()

# 진행 상황 표시
st.write(f"진행도: {len(st.session_state.user_input)} / {len(st.session_state.sequence)}")
