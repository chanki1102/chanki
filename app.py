import streamlit as st
from google import genai

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="연애상담 챗봇",
    page_icon="💌"
)

st.title("💌 연애상담 챗봇")

# -----------------------------
# API KEY
# -----------------------------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("GEMINI_API_KEY가 설정되지 않았습니다.")
    st.stop()

# -----------------------------
# Gemini Client
# -----------------------------
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"클라이언트 생성 실패: {e}")
    st.stop()

# -----------------------------
# 채팅 기록
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "안녕하세요 😊 연애 고민을 편하게 말해주세요!"
        }
    ]

# 이전 대화 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 입력창
prompt = st.chat_input("메시지를 입력하세요")

if prompt:
    # 사용자 메시지 저장
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # 사용자 메시지 출력
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI 응답
    with st.chat_message("assistant"):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=[
                    {
                        "role": "user",
                        "parts": [
                            {
                                "text": (
                                    "너는 따뜻한 연애상담 챗봇이다.\n\n"
                                    + prompt
                                )
                            }
                        ]
                    }
                ]
            )

            reply = response.text

            st.markdown(reply)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": reply
                }
            )

        except Exception as e:
            st.error(f"오류 발생: {e}")
