import streamlit as st
import openai
import os
import hashlib
from datetime import datetime
from gtts import gTTS

# ── 상수 ──────────────────────────────────────────────
SYSTEM_PROMPT = {
    "role": "system",
    "content": "You are a thoughtful assistant. Respond to all input in 25 words and answer in Korean.",
}

# ── 기능 함수 ──────────────────────────────────────────

def STT(audio_file, api_key: str) -> str:
    """UploadedFile을 텍스트로 변환 (OpenAI Whisper)."""
    client = openai.OpenAI(api_key=api_key)
    response = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
    )
    return response.text


def ask_gpt(messages: list, model: str, api_key: str) -> str:
    """GPT 모델에 메시지를 보내고 응답을 반환."""
    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content


def TTS(text: str) -> None:
    """텍스트를 음성으로 변환하여 재생 (gTTS)."""
    filename = "output.mp3"
    gTTS(text=text, lang="ko").save(filename)
    try:
        with open(filename, "rb") as f:
            audio_bytes = f.read()
        st.audio(audio_bytes, format="audio/mp3", autoplay=True)
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
    if "last_audio_hash" not in st.session_state:
        st.session_state.last_audio_hash = None


def reset_session() -> None:
    st.session_state.chat = []
    st.session_state.messages = [SYSTEM_PROMPT]
    st.session_state.last_audio_hash = None


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
        audio_file = st.audio_input("마이크 버튼을 눌러 녹음하세요")

    # 파일 내용의 hash로 새 녹음 여부 판단
    if audio_file is not None:
        audio_hash = hashlib.md5(audio_file.read()).hexdigest()
        audio_file.seek(0)
    else:
        audio_hash = None

    is_new_audio = audio_hash is not None and audio_hash != st.session_state.last_audio_hash

    with col2:
        st.subheader("질문/답변")

        if is_new_audio:
            with col1:
                st.audio(audio_file)

            if not st.session_state.OPENAI_API:
                st.warning("⚠️ 사이드바에 OpenAI API 키를 먼저 입력해주세요.")
            else:
                # 처리 시작 전에 hash 저장 → rerun 중 중복 처리 방지
                st.session_state.last_audio_hash = audio_hash

                with st.spinner("음성을 인식하는 중..."):
                    question = STT(audio_file, st.session_state.OPENAI_API)

                now = datetime.now().strftime("%H:%M")
                st.session_state.chat.append(("user", now, question))
                st.session_state.messages.append({"role": "user", "content": question})

                with st.spinner("답변을 생성하는 중..."):
                    response = ask_gpt(st.session_state.messages, model, st.session_state.OPENAI_API)

                st.session_state.messages.append({"role": "assistant", "content": response})
                st.session_state.chat.append(("bot", now, response))
                TTS(response)

        render_chat(st.session_state.chat)


if __name__ == "__main__":
    main()