import streamlit as st
import numpy as np

# 1. 게임 초기화 (기본 퍼즐 구성)
def init_game():
    # 0은 빈칸을 의미합니다.
    board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    st.session_state.board = np.array(board)
    st.session_state.original = np.array(board) # 수정 불가능한 칸 확인용

if 'board' not in st.session_state:
    init_game()

st.title("🧩 스트림릿 스도쿠")
st.write("빈칸(0)에 알맞은 숫자를 채워 넣으세요!")

# 2. 스도쿠 판 그리기 (3x3 구역 강조)
cols = st.columns(9)
for r in range(9):
    for c in range(9):
        key = f"cell_{r}_{c}"
        val = int(st.session_state.board[r, c])
        
        # 원래 숫자였던 칸은 수정 불가(Disabled) 처리
        is_disabled = st.session_state.original[r, c] != 0
        
        with cols[c]:
            new_val = st.number_input(
                label=f"R{r}C{c}", 
                min_value=0, 
                max_value=9, 
                value=val, 
                key=key, 
                label_visibility="collapsed",
                disabled=is_disabled
            )
            st.session_state.board[r, c] = new_val

# 3. 검증 로직 (중복 체크)
def check_sudoku():
    board = st.session_state.board
    # 가로, 세로 체크
    for i in range(9):
        row = board[i, board[i,:] > 0]
        col = board[board[:,i] > 0, i]
        if len(set(row)) != len(row) or len(set(col)) != len(col):
            return False, "행 또는 열에 중복된 숫자가 있습니다!"
    
    # 0이 없으면 완성
    if 0 in board:
        return None, "진행 중..."
    
    return True, "축하합니다! 완벽하게 푸셨네요! 🎉"

# 4. 결과 출력
status, msg = check_sudoku()
if status is True:
    st.success(msg)
    st.balloons()
elif status is False:
    st.error(msg)
else:
    st.info(msg)

if st.button("게임 초기화"):
    init_game()
    st.rerun()
