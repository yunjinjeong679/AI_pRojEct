import streamlit as st

st.set_page_config(page_title="MBTI 뮤지컬 추천", layout="centered")

st.title("🎭 MBTI 유형별 뮤지컬 추천")

# MBTI별 추천 뮤지컬 데이터
mbti_musicals = {
    "INTJ": ["레미제라블", "지킬앤하이드", "스위니 토드"],
    "INTP": ["데스노트", "드라큘라", "호프"],
    "ENTJ": ["아이다", "노트르담 드 파리", "프랑켄슈타인"],
    "ENTP": ["시카고", "젠틀맨스 가이드", "그레이트 코멧"],
    "INFJ": ["위키드", "레베카", "만달라"],
    "INFP": ["베르테르", "웃는 남자", "마리 앙투아네트"],
    "ENFJ": ["맘마미아", "시스터 액트", "미스 사이공"],
    "ENFP": ["헤드윅", "뮤지컬 광염소나타", "킹키부츠"],
    "ISTJ": ["팬텀", "맨 오브 라만차", "모차르트!"],
    "ISFJ": ["메디슨 카운티의 다리", "빨래", "포미니츠"],
    "ESTJ": ["맘마미아", "렌트", "올 슉 업"],
    "ESFJ": ["디어 에반 핸슨", "웨스트사이드 스토리", "그리스"],
    "ISTP": ["타이타닉", "미아 파밀리아", "쓰릴 미"],
    "ISFP": ["스위니토드", "물랑루즈!", "지킬앤하이드"],
    "ESTP": ["락 오브 에이지", "빌리 엘리어트", "저지 보이스"],
    "ESFP": ["레드북", "킹키부츠", "맘마미아"]
}

# MBTI 선택
mbti_list = list(mbti_musicals.keys())
selected = st.selectbox("🧬 MBTI 를 선택하세요", mbti_list)

# 추천 뮤지컬 출력
st.subheader(f"✨ {selected} 유형에게 딱 맞는 뮤지컬 3선 ✨")
for musical in mbti_musicals[selected]:
    st.write(f"- 🎶 **{musical}**")
