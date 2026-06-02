import streamlit as st

# 페이지 설정
st.set_page_config(page_title="스트림릿 보드게임", page_icon="🎮", layout="centered")

st.title("🎮 스트림릿 틱택토 게임")
st.write("친구와 번갈아가며 3개의 연속된 라인을 만들어보세요!")

# 게임 상태(session_state) 초기화
if "board" not in st.session_state:
    st.session_state.board = [""] * 9
if "turn" not in st.session_state:
    st.session_state.turn = "❌"
if "winner" not in st.session_state:
    st.session_state.winner = None

# 승리 조건 체크 함수
def check_winner():
    b = st.session_state.board
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # 가로
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # 세로
        [0, 4, 8], [2, 4, 6]             # 대각선
    ]
    for cond in win_conditions:
        if b[cond[0]] == b[cond[1]] == b[cond[2]] != "":
            return b[cond[0]]
    if "" not in b:
        return "Draw"
    return None

# 버튼 클릭 시 로직
def handle_click(idx):
    if st.session_state.board[idx] == "" and not st.session_state.winner:
        st.session_state.board[idx] = st.session_state.turn
        winner = check_winner()
        if winner:
            st.session_state.winner = winner
        else:
            # 턴 교체
            st.session_state.turn = "⭕" if st.session_state.turn == "❌" else "❌"

# 게임 리셋 함수
def reset_game():
    st.session_state.board = [""] * 9
    st.session_state.turn = "❌"
    st.session_state.winner = None

# 현재 상태 메시지 출력
if st.session_state.winner:
    if st.session_state.winner == "Draw":
        st.info("🤝 비겼습니다!")
    else:
        st.success(f"🎉 {st.session_state.winner} 승리!")
else:
    st.write(f"### 현재 턴: {st.session_state.turn}")

# 3x3 보드 그리기 (CSS로 버튼 크기 키우기)
st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        height: 80px;
        font-size: 24px !important;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# 3x3 격자 레이아웃
for i in range(3):
    cols = st.columns(3)
    for j in range(3):
        idx = i * 3 + j
        button_label = st.session_state.board[idx]
        # 빈 칸이면 인덱스를 라벨로 숨기거나 공백 처리
        display_label = button_label if button_label != "" else " "
        
        # 버튼 생성 및 클릭 이벤트 연결
        cols[j].button(display_label, key=f"btn_{idx}", on_click=handle_click, args=(idx,))

st.write("---")
# 리셋 버튼
if st.button("🔄 게임 다시 시작하기"):
    reset_game()
    st.rerun()
