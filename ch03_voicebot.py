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

# ── CSS 스타일 ─────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&family=Space+Mono:wght@400;700&display=swap');

    /* 전체 배경 */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f0c29, #1a1a2e, #16213e);
        min-height: 100vh;
    }
    [data-testid="stHeader"] { background: transparent; }

    /* 사이드바 */
    [data-testid="stSidebar"] {
        background: rgba(255,255,255,0.04);
        border-right: 1px solid rgba(255,255,255,0.08);
    }
    [data-testid="stSidebar"] * { color: #c9d1d9 !important; font-family: 'Noto Sans KR', sans-serif; }

    /* 헤더 */
    .hero-header {
        text-align: center;
        padding: 2.5rem 0 1.5rem;
    }
    .hero-title {
        font-family: 'Space Mono', monospace;
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.5px;
        margin-bottom: 0.4rem;
    }
    .hero-sub {
        font-family: 'Noto Sans KR', sans-serif;
        font-size: 0.85rem;
        color: rgba(255,255,255,0.35);
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    /* 구분선 */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(167,139,250,0.4), transparent);
        margin: 0.5rem 0 2rem;
    }

    /* 카드 컨테이너 */
    .card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 1.5rem;
        backdrop-filter: blur(12px);
    }
    .card-title {
        font-family: 'Space Mono', monospace;
        font-size: 0.75rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: rgba(167,139,250,0.8);
        margin-bottom: 1rem;
    }

    /* expander */
    [data-testid="stExpander"] {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.07) !important;
        border-radius: 12px !important;
        margin-bottom: 1.5rem;
    }
    [data-testid="stExpander"] summary {
        color: rgba(255,255,255,0.5) !important;
        font-family: 'Noto Sans KR', sans-serif !important;
        font-size: 0.85rem !important;
    }
    [data-testid="stExpander"] p,
    [data-testid="stExpander"] li {
        color: rgba(255,255,255,0.4) !important;
        font-family: 'Noto Sans KR', sans-serif !important;
        font-size: 0.82rem !important;
        line-height: 1.8 !important;
    }

    /* 채팅 말풍선 */
    .bubble-user {
        display: flex;
        justify-content: flex-end;
        align-items: flex-end;
        gap: 8px;
        margin-bottom: 12px;
    }
    .bubble-bot {
        display: flex;
        justify-content: flex-start;
        align-items: flex-end;
        gap: 8px;
        margin-bottom: 12px;
    }
    .bubble-text-user {
        background: linear-gradient(135deg, #6d28d9, #4f46e5);
        color: white;
        border-radius: 18px 18px 4px 18px;
        padding: 10px 16px;
        max-width: 75%;
        font-family: 'Noto Sans KR', sans-serif;
        font-size: 0.9rem;
        line-height: 1.6;
        box-shadow: 0 4px 15px rgba(109,40,217,0.3);
    }
    .bubble-text-bot {
        background: rgba(255,255,255,0.08);
        color: rgba(255,255,255,0.88);
        border-radius: 18px 18px 18px 4px;
        padding: 10px 16px;
        max-width: 75%;
        font-family: 'Noto Sans KR', sans-serif;
        font-size: 0.9rem;
        line-height: 1.6;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .bubble-time {
        font-size: 0.68rem;
        color: rgba(255,255,255,0.25);
        font-family: 'Space Mono', monospace;
        margin-bottom: 4px;
    }
    .avatar {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        flex-shrink: 0;
    }
    .avatar-bot {
        background: linear-gradient(135deg, #34d399, #059669);
    }
    .avatar-user {
        background: linear-gradient(135deg, #a78bfa, #6d28d9);
    }
    .empty-chat {
        text-align: center;
        padding: 3rem 1rem;
        color: rgba(255,255,255,0.15);
        font-family: 'Space Mono', monospace;
        font-size: 0.8rem;
        letter-spacing: 1px;
    }
    .empty-icon { font-size: 2.5rem; margin-bottom: 0.75rem; opacity: 0.3; }

    /* 사이드바 버튼 */
    [data-testid="stSidebar"] .stButton > button {
        width: 100%;
        background: rgba(239,68,68,0.15) !important;
        border: 1px solid rgba(239,68,68,0.3) !important;
        color: #fca5a5 !important;
        border-radius: 8px !important;
        font-family: 'Noto Sans KR', sans-serif !important;
        font-size: 0.85rem !important;
        padding: 0.5rem !important;
        transition: all 0.2s;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(239,68,68,0.25) !important;
        border-color: rgba(239,68,68,0.5) !important;
    }

    /* 사이드바 라디오 */
    [data-testid="stSidebar"] .stRadio label {
        color: rgba(255,255,255,0.6) !important;
        font-size: 0.85rem !important;
    }

    /* 사이드바 레이블 */
    [data-testid="stSidebar"] label {
        color: rgba(255,255,255,0.5) !important;
        font-size: 0.78rem !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
    }

    /* warning */
    [data-testid="stAlert"] {
        background: rgba(251,191,36,0.1) !important;
        border: 1px solid rgba(251,191,36,0.2) !important;
        border-radius: 10px !important;
        color: #fde68a !important;
        font-family: 'Noto Sans KR', sans-serif !important;
    }

    /* audio player */
    audio { width: 100%; border-radius: 8px; margin-top: 8px; }

    /* 사이드바 입력창 */
    [data-testid="stSidebar"] input {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 8px !important;
        color: white !important;
        font-size: 0.85rem !important;
    }

    /* 사이드바 로고 */
    .sidebar-logo {
        text-align: center;
        padding: 1.5rem 0 1rem;
    }
    .sidebar-logo-icon {
        font-size: 2.5rem;
        display: block;
        margin-bottom: 0.4rem;
    }
    .sidebar-logo-text {
        font-family: 'Space Mono', monospace;
        font-size: 0.7rem;
        letter-spacing: 2px;
        color: rgba(255,255,255,0.2);
        text-transform: uppercase;
    }

    /* audio_input 위젯 */
    [data-testid="stAudioInput"] {
        background: rgba(255,255,255,0.03) !important;
        border: 1px dashed rgba(167,139,250,0.3) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }
    </style>
    """, unsafe_allow_html=True)


# ── 기능 함수 ──────────────────────────────────────────

def STT(audio_file, api_key: str) -> str:
    client = openai.OpenAI(api_key=api_key)
    response = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
    return response.text


def ask_gpt(messages: list, model: str, api_key: str) -> str:
    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content


def TTS(text: str) -> None:
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
    defaults = {
        "chat": [],
        "messages": [SYSTEM_PROMPT],
        "OPENAI_API": "",
        "last_audio_hash": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def reset_session() -> None:
    st.session_state.chat = []
    st.session_state.messages = [SYSTEM_PROMPT]
    st.session_state.last_audio_hash = None


# ── UI 헬퍼 ───────────────────────────────────────────

def render_chat(chat: list) -> None:
    if not chat:
        st.markdown(
            '<div class="empty-chat">'
            '<div class="empty-icon">🎙️</div>'
            '아직 대화가 없습니다<br>녹음 버튼을 눌러 시작하세요'
            '</div>',
            unsafe_allow_html=True,
        )
        return

    for sender, time, message in chat:
        if sender == "user":
            st.markdown(
                f'<div class="bubble-user">'
                f'<div class="bubble-time">{time}</div>'
                f'<div class="bubble-text-user">{message}</div>'
                f'<div class="avatar avatar-user">나</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="bubble-bot">'
                f'<div class="avatar avatar-bot">AI</div>'
                f'<div class="bubble-text-bot">{message}</div>'
                f'<div class="bubble-time">{time}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )


# ── 메인 ──────────────────────────────────────────────

def main() -> None:
    st.set_page_config(
        page_title="승우의 음성 비서",
        page_icon="🎙️",
        layout="wide",
    )
    init_session()
    inject_css()

    # ── 사이드바 ──
    with st.sidebar:
        st.markdown(
            '<div class="sidebar-logo">'
            '<span class="sidebar-logo-icon">🎙️</span>'
            '<span class="sidebar-logo-text">Voice Assistant</span>'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown("---")
        st.session_state.OPENAI_API = st.text_input(
            label="OPENAI API KEY",
            placeholder="sk-...",
            value=st.session_state.OPENAI_API,
            type="password",
        )
        st.markdown("---")
        model = st.radio(
            label="GPT MODEL",
            options=["gpt-3.5-turbo", "gpt-4"],
        )
        st.markdown("---")
        if st.button("🗑️  대화 초기화"):
            reset_session()
            st.rerun()

    # ── 헤더 ──
    st.markdown(
        '<div class="hero-header">'
        '<div class="hero-title">승우의 음성 비서 프로그램</div>'
        '<div class="hero-sub">Powered by Whisper · GPT · gTTS</div>'
        '</div>'
        '<div class="divider"></div>',
        unsafe_allow_html=True,
    )

    # ── 안내 expander ──
    with st.expander("서비스 안내", expanded=False):
        st.write(
            """
            - 음성 비서 프로그램의 UI는 스트림릿을 활용했습니다.
            - STT(Speech To Text)는 OpenAI의 Whisper AI를 활용했습니다.
            - 답변은 OpenAI의 GPT 모델을 활용했습니다.
            - TTS(Text To Speech)는 구글의 Google Translate TTS를 활용했습니다.
            """
        )

    # ── 메인 컬럼 ──
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown('<div class="card"><div class="card-title">🎤 질문하기</div>', unsafe_allow_html=True)
        audio_file = st.audio_input("마이크 버튼을 눌러 녹음하세요")
        st.markdown('</div>', unsafe_allow_html=True)

    # 새 녹음 감지
    if audio_file is not None:
        audio_hash = hashlib.md5(audio_file.read()).hexdigest()
        audio_file.seek(0)
    else:
        audio_hash = None

    is_new_audio = audio_hash is not None and audio_hash != st.session_state.last_audio_hash

    with col2:
        st.markdown('<div class="card"><div class="card-title">💬 질문 / 답변</div>', unsafe_allow_html=True)

        if is_new_audio:
            with col1:
                st.audio(audio_file)

            if not st.session_state.OPENAI_API:
                st.warning("⚠️ 사이드바에 OpenAI API 키를 먼저 입력해주세요.")
            else:
                st.session_state.last_audio_hash = audio_hash

                with st.spinner("🎧 음성 인식 중..."):
                    question = STT(audio_file, st.session_state.OPENAI_API)

                now = datetime.now().strftime("%H:%M")
                st.session_state.chat.append(("user", now, question))
                st.session_state.messages.append({"role": "user", "content": question})

                with st.spinner("🤖 답변 생성 중..."):
                    response = ask_gpt(st.session_state.messages, model, st.session_state.OPENAI_API)

                st.session_state.messages.append({"role": "assistant", "content": response})
                st.session_state.chat.append(("bot", now, response))
                TTS(response)

        render_chat(st.session_state.chat)
        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()