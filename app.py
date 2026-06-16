import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정
st.set_page_config(page_title="빡공AI: 공부 주도기", page_icon="🔥", layout="centered")
st.title("🔥 빡공AI : 공부 주도기")
st.caption("⚠️ 경고: 공부 외 딴짓 질문을 하면 즉시 강제 차단됩니다.")

# 2. API 키 설정
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("⚠️ Streamlit Secrets 설정을 확인해주세요. 'GEMINI_API_KEY'가 필요합니다.")
    st.stop()

# 3. 세션 상태 초기화
if "is_banned" not in st.session_state:
    st.session_state.is_banned = False
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. 차단된 사용자 화면 잠금
if st.session_state.is_banned:
    st.error(
        "🚨 [접속 강제 차단]\n\n"
        "공부와 상관없는 딴짓 질문(잡담, 연애, 게임 등)을 한 것이 감지되었습니다.\n\n"
        "다시 집중할 준비가 되면 창을 완전히 새로고침(F5)하고 들어오세요."
    )
    st.stop()

# 기존 대화 기록 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. 엄격한 공부 멘토 페르소나 지침
system_instruction = (
    "당신은 매우 엄격하고 냉철한 수험생 전용 공부 감독관(멘토)입니다.\n\n"
    "사용자의 질문이 '학습 내용 질의응답(수학, 영어, 과학, 코딩 등)', '공부 계획 수립', '암기 팁', '학업 동기부여' 등 "
    "실제 공부 및 학업과 직간접적으로 관련된 내용이라면 아주 명쾌하고 똑 부러지게 가르쳐주거나 자극을 주세요.\n\n"
    "★최우선 절대 규칙★: 만약 사용자의 질문이 공부와 1도 상관없는 딴소리(예: 연애 상담, 오늘 날씨, 일상 대화, 유머, 게임 이야기, 심심하다는 징징거림, 연예인 잡담 등)라면, "
    "다른 설명은 다 생략하고 오직 정확히 딱 세 글자, [딴짓함] 이라고만 답변하세요. 미사여구를 붙이면 절대 안 됩니다."
)

# 6. 사용자 입력 및 AI 처리
if user_input := st.chat_input("질문할 학습 내용이나 오늘 공부 계획을 입력하세요..."):
    # 사용자 입력 표시 및 저장
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # AI 답변 생성 프로세스
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            with st.spinner("감독관이 검사 중..."):
                model = genai.GenerativeModel(
                    model_name="gemini-2.5-flash-lite",
                    system_instruction=system_instruction
                )
                
                # 대화 기록 포맷 변환
                chat_history = []
                for msg in st.session_state.messages[:-1]:
                    role = "user" if msg["role"] == "user" else "model"
                    chat_history.append({"role": role, "parts": [msg["content"]]})
                
                # 챗봇 대화 진행 및 응답 수신
                chat = model.start_chat(history=chat_history)
                response = chat.send_message(user_input)
                ai_response = response.text.strip()
                
                # 🛑 [딴짓 감지 트랩]
                if "[딴짓함]" in ai_response or ai_response == "딴짓함":
                    st.session_state.is_banned = True
                    st.rerun()
                else:
                    # 정상 답변 출력 및 기록
                    message_placeholder.markdown(ai_response)
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                    
        except Exception as e:
            message_placeholder.error(f"🚨 시스템 오류가 발생했습니다: {str(e)}")
