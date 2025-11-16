# app.py
import streamlit as st
import openai
import os

# -----------------------------
# OpenAI API 키 설정
# -----------------------------
openai.api_key = os.getenv("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")

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(page_title="AI 루틴 추천 & 회고", layout="wide")
st.title("🧠 오늘의 AI 시간대별 루틴 추천 & 회고")

# -----------------------------
# 사용자 입력
# -----------------------------
st.header("1️⃣ 현재 상태 입력")
emotion = st.selectbox("현재 기분을 선택하세요", ["😃 기쁨", "😐 보통", "😢 슬픔", "😡 화남", "😴 피곤"])
energy = st.slider("현재 에너지 수준 (1-10)", 1, 10, 5)

# -----------------------------
# 시간대별 루틴 추천
# -----------------------------
st.header("2️⃣ 오늘의 시간대별 추천 루틴")
result = ""
if st.button("추천 받기"):
    prompt = f"""
    사용자의 현재 감정은 {emotion}, 에너지 수준은 {energy}입니다.
    오늘 하루를 아침(06-10), 점심(11-14), 오후(15-18), 저녁(19-22) 4개 시간대로 나누어,
    각 시간대에 맞는 활동 1~2개씩 추천하고, 간단한 이유를 알려주세요.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # gpt-4 권한 없으면 gpt-3.5-turbo 사용
            messages=[{"role":"user","content":prompt}],
            max_tokens=400,
            temperature=0.7
        )
        result = response.choices[0].message.content
        st.success(result)
    except Exception as e:
        st.error(f"추천 루틴 생성 중 오류 발생: {e}")

# -----------------------------
# 하루 회고
# -----------------------------
st.header("3️⃣ 하루 회고")
today_feedback = st.text_area("오늘 하루를 돌아보며 느낀 점과 성장을 입력하세요.")

if st.button("회고 저장"):
    if result == "":
        st.warning("먼저 루틴 추천을 받아주세요.")
    else:
        st.success("회고가 저장되었습니다!")

# -----------------------------
# AI 회고 분석
# -----------------------------
st.header("4️⃣ AI 피드백")
if today_feedback:
    feedback_prompt = f"""
    사용자가 작성한 오늘 회고: {today_feedback}
    위 회고를 바탕으로 오늘 잘한 점과 개선할 점을 요약하고,
    내일 시도할 수 있는 시간대별 루틴을 추천해 주세요.
    """
    try:
        feedback_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"user","content":feedback_prompt}],
            max_tokens=400,
            temperature=0.7
        )
        feedback_result = feedback_response.choices[0].message.content
        st.info(feedback_result)
    except Exception as e:
        st.error(f"AI 피드백 생성 중 오류 발생: {e}")
