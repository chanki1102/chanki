# app.py
import streamlit as st
from google import genai
from google.genai import types

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="연애상담 챗봇",
    page_icon="💌",
    layout="centered"
)

st.title("💌 연애상담 챗봇")
st.caption("Gemini 2.5 Flash Lite 기반 상담 챗봇")

# -----------------------------
# API 키 불러오기
# -----------------------------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("❌ secrets.toml에 GEMINI_API_KEY가 설정되지 않았습니다.")
    st.stop()

# -----------------------------
# Gemini 클라이언트 생성
# -----------------------------
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"❌ Gemini 클라이언트 생성 실패: {e}")
    st.stop()

# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "안녕하세요 😊\n"
                "연애 고민, 썸, 이별, 재회, 인간관계 등 편하게 이야기해 주세요!"
            )
        }
    ]

# -----------------------------
# 이전 채팅 출력
# -----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# 사용자 입력
# -----------------------------
user_input = st.chat_input("고민을 입력해 주세요...")

if user_input:
    # 사용자 메시지 저장
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # 사용자 메시지 출력
    with st.chat_message("user"):
        st.markdown(user_input)

    # AI 응답 생성
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        try:
            # Gemini 형식으로 변환
            contents = []

            for msg in st.session_state.messages:
                role = "user" if msg["role"] == "user" else "model"

                contents.append(
                    types.Content(
                        role=role,
                        parts=[types.Part(text=msg["content"])]
                    )
                )

            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=(
                        "너는 공감 능력이 뛰어난 연애 상담 챗봇이다. "
                        "사용자의 감정을 존중하며 따뜻하고 현실적인 조언을 제공해라. "
                        "답변은 너무 길지 않게 자연스럽게 작성해라."
                    ),
                    temperature=0.8,
                    max_output_tokens=1000
                )
            )

            bot_reply = response.text

            # 응답 출력
            message_placeholder.markdown(bot_reply)

            # 채팅 기록 저장
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": bot_reply
                }
            )

        except Exception as e:
            error_message = f"❌ 오류가 발생했습니다:\n\n{str(e)}"
            message_placeholder.error(error_message)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": "죄송해요 😢 오류가 발생했어요. 잠시 후 다시 시도해주세요."
                }
            )
