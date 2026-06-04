<!--
████████████████████████████████████████████████████████████████████
  seungwoo2000 · voicebot — K-디지털 트레이닝 포트폴리오 README
████████████████████████████████████████████████████████████████████
-->

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:1e3a5f,50:2563eb,100:7c3aed&height=220&section=header&text=🎙️%20AI%20Voice%20Bot&fontSize=52&fontColor=ffffff&fontAlignY=40&desc=말하면%20답해주는%20나만의%20AI%20음성%20비서&descAlignY=62&descColor=bfdbfe&animation=fadeIn" alt="header" width="100%"/>

<br/>

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![Whisper](https://img.shields.io/badge/Whisper-STT-412991?style=for-the-badge&logo=openai&logoColor=white)
![gTTS](https://img.shields.io/badge/gTTS-TTS-4285F4?style=for-the-badge&logo=google&logoColor=white)

<br/>

> **말하면 듣고 · 생각하고 · 다시 말해주는 AI 음성 비서**  
> OpenAI Whisper로 받아쓰고, GPT로 대답하고, Google TTS로 음성 출력까지!

<br/>

**🎧 라이브 서비스 →** [voicebot.streamlit.app](https://voicebot-y5xg8vzse6xwwdob6vg63q.streamlit.app/)

</div>

---

## 📋 훈련 과정 정보

| 항목 | 내용 |
|:---|:---|
| 🏫 **훈련기관** | 아시아경제 교육센터 |
| 📚 **훈련과정명** | 융합\_데이터 기반 차세대 디지털 헬스케어 AI 솔루션 5회차 |
| 🏷️ **훈련유형** | K-디지털 트레이닝 |
| 📅 **훈련기간** | 2026-02-03 ~ 2026-07-30 (6개월) |
| 💡 **프로젝트 분류** | AI 음성 처리 · STT/TTS 파이프라인 실습 |

---

## 🎙️ 프로젝트 소개

```
🎤 사용자가 마이크에 말한다
        ↓  OpenAI Whisper (STT)
📝 음성이 텍스트로 변환된다
        ↓  OpenAI GPT
🤖 GPT가 한국어로 답변을 생성한다
        ↓  Google TTS (gTTS)
🔊 답변이 음성으로 재생된다
```

**"말하면 답해주는"** 흐름을 STT → GPT → TTS 3단계 파이프라인으로 직접 구현한 AI 음성 비서 프로그램입니다.  
Streamlit으로 웹 UI를 만들고, Streamlit Cloud에 배포까지 완료했습니다.

---

## 🛠️ 기술 스택

> 비전공자도 이해할 수 있도록, 각 기술이 **어떤 역할**을 하는지 함께 설명합니다.

| 기술 | 역할 | 키워드 |
|:---:|:---|:---|
| ![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white) | 프로그램 전체를 짜는 언어 | `AI 라이브러리` `생태계` |
| ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white) | 파이썬 코드만으로 웹 UI를 뚝딱 만드는 프레임워크 | `빠른 프로토타이핑` `배포` |
| ![Whisper](https://img.shields.io/badge/Whisper-412991?logo=openai&logoColor=white) | 음성 → 텍스트 변환 (OpenAI STT 모델) | `whisper-1` `음성인식` |
| ![GPT](https://img.shields.io/badge/GPT-412991?logo=openai&logoColor=white) | 질문을 이해하고 한국어로 답변 생성 | `gpt-3.5-turbo` `gpt-4` |
| ![gTTS](https://img.shields.io/badge/gTTS-4285F4?logo=google&logoColor=white) | 텍스트 → 음성 변환 (Google TTS) | `Text To Speech` `한국어` |

---

## ✨ 주요 기능

```
🎤  음성 녹음       →  브라우저 마이크로 바로 녹음
📝  STT            →  OpenAI Whisper가 음성을 텍스트로 변환
🤖  GPT 답변       →  GPT-3.5 / GPT-4 중 선택해서 한국어 답변 생성
🔊  TTS 재생       →  Google gTTS로 답변을 음성으로 자동 재생
💬  채팅 UI        →  말풍선 형태로 대화 내역 시각화
🔁  대화 초기화    →  사이드바 버튼 한 번으로 새 대화 시작
🔑  API 키 입력    →  사이드바에서 OpenAI API 키 직접 설정
```

---

## 🏗️ 동작 흐름

| 단계 | 담당 기술 | 설명 |
|:---:|:---:|:---|
| 1️⃣ **녹음** | Streamlit `audio_input` | 브라우저에서 마이크로 직접 녹음 |
| 2️⃣ **STT** | OpenAI Whisper `whisper-1` | 녹음 파일을 텍스트로 변환 |
| 3️⃣ **질문 전송** | OpenAI Chat API | 변환된 텍스트를 GPT에 전달 |
| 4️⃣ **답변 생성** | GPT-3.5-turbo / GPT-4 | 25 단어 이내 한국어로 답변 |
| 5️⃣ **TTS** | Google gTTS | 답변 텍스트를 MP3 음성으로 변환 |
| 6️⃣ **재생** | Streamlit `audio` | 브라우저에서 자동 재생 |

---

## 📁 파일 구조

```
voicebot/
│
├── ch03_voicebot.py    # 메인 실행 파일 (전체 앱 로직)
├── requirements.txt    # Python 패키지 목록
└── packages.txt        # 시스템 패키지 목록 (Streamlit Cloud 배포용)
```

---

## 📈 배운 점 · 성장 포인트

| 분야 | 배운 것 | 이걸 배워서 뭘 할 수 있게 됐나? |
|:---|:---|:---|
| 🎤 **STT** | OpenAI Whisper API 호출 | 음성 파일을 텍스트로 자동 변환 |
| 🤖 **LLM 연동** | OpenAI Chat Completions API | 시스템 프롬프트로 AI 답변 스타일 제어 |
| 🔊 **TTS** | gTTS 라이브러리 | 텍스트를 자연스러운 한국어 음성으로 변환 |
| 🖥️ **웹 UI** | Streamlit 컴포넌트 | 파이썬만으로 채팅 버블 UI · 사이드바 구성 |
| 🔒 **보안** | API 키 password 처리 | 민감 정보를 안전하게 입력받는 방법 |
| ♻️ **세션 관리** | `st.session_state` | 새로고침 없이 대화 이력을 유지하는 방법 |
| ☁️ **배포** | Streamlit Cloud | `requirements.txt` · `packages.txt`로 클라우드 배포 |

---

## ⚙️ 실행 방법

> 로컬(내 컴퓨터)에서 직접 실행해보고 싶다면 아래 순서를 따라주세요.

**1️⃣ 저장소 클론**
```bash
git clone https://github.com/seungwoo2000/voicebot.git
cd voicebot
```

**2️⃣ 패키지 설치**
```bash
pip install -r requirements.txt
```

**3️⃣ 앱 실행**
```bash
streamlit run ch03_voicebot.py
```

**4️⃣ 브라우저에서 접속 후**  
사이드바에 **OpenAI API 키**를 입력하고 마이크 버튼을 눌러 말하면 끝!

---

<div align="center">

<br/>

*"말하면 듣고, 생각하고, 다시 말해주는 AI 음성 비서"*

<br/>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:7c3aed,50:2563eb,100:1e3a5f&height=130&section=footer&text=K-디지털%20트레이닝%20|%20아시아경제%20교육센터&fontSize=15&fontColor=ffffff&fontAlignY=65" width="100%"/>

**📅 2026.02 ~ 2026.07** &nbsp;|&nbsp; Made with 🎙️ during K-Digital Training

</div>
