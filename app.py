import streamlit as st
import random

# 운세 리스트
fortune_list = [
    "오늘은 행운의 날이에요!",
    "힘든 하루가 예상되니 조심하세요.",
    "새로운 기회가 찾아올 거예요!",
    "건강을 잘 챙기세요.",
    "오늘은 편안한 하루가 될 거예요."
]

# 앱 제목
st.title("오늘의 운세 확인")

# 날짜 입력 받기
user_date = st.date_input("오늘의 날짜를 선택하세요:")

# 운세 추천 버튼
if st.button("오늘의 운세 보기"):
    st.write(f"{user_date}의 운세는:")
    st.success(random.choice(fortune_list))