import streamlit as st
from st_audiorec import st_audiorec
import openai
import os
from datetime import datetime
from gtts import gTTS
import base64
import io

# ── 상수 ──────────────────────────────────────────────
SYSTEM_PROMPT = {
    "role": "system",
    "content": "You are a thoughtful assistant. Respond to all input in 25 words and answer in Korean.",
}

# ── 기능 함수 ──────────────────────────────────────────

def STT(audio_bytes: bytes, api_key: str) -> str:
    """오디오 바이트를 텍스트로 변환 (OpenAI Whisper)."""
    filename = "input.wav"
    with open(filename, "wb") as f:
        f.write(audio_bytes)
    try:
        client = openai.OpenAI(api_key=api_key)
        with open(filename, "rb") as f:
            response = client.audio.transcriptions.create(model="whisper-1", file=f)
        return response.text
    finally:
        if os.path.exists(filename):
            os.remove(filename)


def ask_gpt(messages: list, model: str, api_key: str) -> str:
    """GPT 모델에 메시지를 보내고 응답을 반환."""
    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content


def TTS(text: str) -> None:
    """텍스트를 음성으로 변환하여 자동 재생 (gTTS)."""
    filename = "output.mp3"
    gTTS(text=text, lang="ko").save(filename)
    try:
        with open(filename, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        st.markdown(
            f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>',
            unsafe_allow_html=True,
        )
    finally:
        if os.path.exists(filename):
            os.remove(filename)


# ── 세션 초기화 ────────────────────────────────────────

def init_session() -> None:
    if "chat" not in st.session_state:
        st.session_state.chat = []
    if "messages" not in st.session_state:
        st.session_state.messages = [SYSTEM_PROMPT]
    if "OPENAI_API" not in st.session_state:
        st.session_state.OPENAI_API = ""
    if "last_audio" not in st.session_state:
        st.session_state.last_audio = None


def reset_session() -> None:
    st.session_state.chat = []
    st.session_state.messages = [SYSTEM_PROMPT]
    st.session_state.last_audio = None


# ── UI 헬퍼 ───────────────────────────────────────────

def render_chat(chat: list) -> None:
    for sender, time, message in chat:
        if sender == "user":
            bubble_style = "background-color:#007AFF;color:white;"
        else:
            bubble_style = "background-color:#E5E5EA;color:black;"

        st.write(
            f'<div style="display:flex;align-items:center;">'
            f'<div style="{bubble_style}border-radius:12px;padding:8px 12px;margin-right:8px;">{message}</div>'
            f'<div style="font-size:0.8rem;color:gray;margin-left:8px;">{time}</div>'
            f"</div>",
            unsafe_allow_html=True,
        )
        st.write("")


# ── 메인 ──────────────────────────────────────────────

def main() -> None:
    st.set_page_config(page_title="음성 비서 프로그램", layout="wide")
    init_session()

    st.header("음성 비서 프로그램")
    st.markdown("---")

    with st.expander("음성비서 프로그램에 관하여", expanded=True):
        st.write(
            """
            - 음성 비서 프로그램의 UI는 스트림릿을 활용했습니다.
            - STT(Speech To Text)는 OpenAI의 Whisper AI를 활용했습니다.
            - 답변은 OpenAI의 GPT 모델을 활용했습니다.
            - TTS(Text To Speech)는 구글의 Google Translate TTS를 활용했습니다.
            """
        )
        st.markdown("")

    # ── 사이드바: 설정 ──
    with st.sidebar:
        st.session_state.OPENAI_API = st.text_input(
            label="OPENAI API 키",
            placeholder="Enter Your API Key",
            value="",
            type="password",
        )
        st.markdown("---")
        model = st.radio(label="GPT 모델 선택", options=["gpt-3.5-turbo", "gpt-4"])
        st.markdown("---")
        if st.button(label="초기화"):
            reset_session()

    # ── 메인 영역 ──
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("질문하기")
        # st_audiorec는 bytes 또는 None을 반환
        audio_bytes = st_audiorec()

    # 새로운 녹음인지 확인 (이전과 동일한 데이터면 재처리 방지)
    is_new_audio = (
        audio_bytes is not None
        and audio_bytes != st.session_state.last_audio
    )

    if is_new_audio:
        st.session_state.last_audio = audio_bytes

        with col1:
            st.audio(audio_bytes, format="audio/wav")

        with st.spinner("음성을 인식하는 중..."):
            question = STT(audio_bytes, st.session_state.OPENAI_API)

        now = datetime.now().strftime("%H:%M")
        st.session_state.chat.append(("user", now, question))
        st.session_state.messages.append({"role": "user", "content": question})

        with st.spinner("답변을 생성하는 중..."):
            response = ask_gpt(st.session_state.messages, model, st.session_state.OPENAI_API)

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.chat.append(("bot", now, response))

        with col2:
            st.subheader("질문/답변")
            render_chat(st.session_state.chat)
            TTS(response)

    else:
        with col2:
            st.subheader("질문/답변")
            render_chat(st.session_state.chat)


if __name__ == "__main__":
    main()