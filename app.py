import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 기본 설정
st.set_page_config(page_title="딴짓차단기", page_icon="🚫", layout="centered")

# 2. 헤더 및 안내 문구
st.title("🚫 딴짓차단기")
st.markdown("---")
st.markdown("### 🔒 초정밀 포커스 감지 작동 중")
st.info("💡 **팀원 안내사항:** 이 페이지를 켜둔 상태에서 다른 창을 클릭하거나, 듀얼 모니터로 이동하거나, 브라우저 주소창을 건드리면 즉시 경고 알림이 발생합니다.")

# 3. 핵심 이탈 감지 스크립트 (포커스 아웃 방식)
detection_script = """
<script>
    // 페이지 로드 시 시스템 알림 권한 요청
    if (Notification.permission !== "granted") {
        Notification.requestPermission();
    }

    // 브라우저가 포커스를 잃는 순간 (다른 곳을 클릭하는 순간) 즉시 실행
    window.addEventListener('blur', () => {
        if (Notification.permission === "granted") {
            new Notification("🚨 딴짓 감지!", {
                body: "창을 이탈했습니다. 즉시 복귀하세요!",
                icon: "https://cdn-icons-png.flaticon.com/512/1828/1828665.png"
            });
        }
    });
</script>
"""
# 스크립트를 화면에 보이지 않게 실행
components.html(detection_script, height=0)

# 4. 하단 경고 메시지
st.warning("⚠️ 최초 실행 시 브라우저 상단에 뜨는 **'알림 권한 허용'**을 반드시 눌러주셔야 즉시 알림이 작동합니다.")
