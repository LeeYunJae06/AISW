# app.py

import streamlit as st
import openai

# -----------------------------
# OpenAI API 키 직접 입력
# -----------------------------
OPENAI_API_KEY = "본인_API_KEY_여기에_넣기"

# OpenAI 1.x 방식 클라이언트 생성
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(page_title="AI 루틴 추천 & 회고", layout="wide")
st.title("🧠 오늘의 AI 시간대별 루틴 추천 & 회고")

# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "routine_result" not in st.session_state:
    st.session_state.routine_result = ""
if "feedback_result" not in st.session_state:
    st.session_state.feedback_result = ""

# -----------------------------
# 1️⃣ 사용자 입력
# -----------------------------
st.header("1️⃣ 현재 상태 입력")
emotion = st.selectbox("현재 기분을 선택하세요", ["😃 기쁨", "😐 보통", "😢 슬픔", "😡 화남", "😴 피곤"])
energy = st.slider("현재 에너지 수준 (1-10)", 1, 10, 5)

# -----------------------------
# 2️⃣ 오늘 루틴 추천
# -----------------------------
st.header("2️⃣ 오늘의 시간대별 추천 루틴")
if st.button("추천 받기"):
    prompt = f"""
    사용자의 현재 감정은 '{emotion}', 에너지 수준은 {energy}입니다.
    오늘 하루를 아침(06-10), 점심(11-14), 오후(15-18), 저녁(19-22) 4개 시간대로 나누어,
    각 시간대에 맞는 활동 1~2개씩 추천하고, 간단한 이유를 알려주세요.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=400
        )
        st.session_state.routine_result = response.choices[0].message.content
    except Exception as e:
        st.error(f"추천 루틴 생성 중 오류 발생: {e}")

# 루틴 출력
if st.session_state.routine_result:
    st.success(st.session_state.routine_result)

# -----------------------------
# 3️⃣ 하루 회고
# -----------------------------
st.header("3️⃣ 하루 회고")
today_feedback = st.text_area("오늘 하루를 돌아보며 느낀 점과 성장을 입력하세요.")

if st.button("회고 저장"):
    if not st.session_state.routine_result:
        st.warning("먼저 루틴 추천을 받아주세요.")
    elif not today_feedback.strip():
        st.warning("회고 내용을 입력해주세요.")
    else:
        st.success("회고가 저장되었습니다!")

# -----------------------------
# 4️⃣ AI 회고 분석
# -----------------------------
st.header("4️⃣ AI 피드백")
if today_feedback.strip():
    feedback_prompt = f"""
    사용자가 작성한 오늘 회고: {today_feedback}
    감정과 에너지 수준: {emotion}, {energy}
    이 정보를 바탕으로 오늘 잘한 점과 개선할 점을 요약하고,
    내일 시도할 수 있는 시간대별 루틴을 추천해 주세요.
    """
    try:
        feedback_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": feedback_prompt}],
            temperature=0.7,
            max_tokens=400
        )
        st.session_state.feedback_result = feedback_response.choices[0].message.content
    except Exception as e:
        st.error(f"AI 피드백 생성 중 오류 발생: {e}")

# 피드백 출력
if st.session_state.feedback_result:
    st.info(st.session_state.feedback_result)
