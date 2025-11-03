import streamlit as st

st.set_page_config(page_title="MBTI 책 & 영화 추천", page_icon="🎭")

st.title("🎭 MBTI별 책 & 영화 추천 🎬")
st.write("안녕! 😊 너의 MBTI를 선택하면, 그 성격에 어울리는 **책 2권**과 **영화 2편**을 추천해줄게!")  

# MBTI 목록
mbti_list = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

mbti = st.selectbox("👇 너의 MBTI를 골라봐!", mbti_list)

# MBTI별 추천 데이터
recommendations = {
    "INTJ": {
        "books": ["《1984》 - 조지 오웰", "《총, 균, 쇠》 - 재레드 다이아몬드"],
        "movies": ["인셉션", "인터스텔라"]
    },
    "INTP": {
        "books": ["《이기적 유전자》 - 리처드 도킨스", "《사피엔스》 - 유발 하라리"],
        "movies": ["이터널 선샤인", "매트릭스"]
    },
    "ENTJ": {
        "books": ["《7가지 습관》 - 스티븐 코비", "《제로 투 원》 - 피터 틸"],
        "movies": ["더 소셜 네트워크", "월 스트리트"]
    },
    "ENTP": {
        "books": ["《괴짜경제학》 - 스티븐 레빗", "《생각의 탄생》 - 루트번스타인 부부"],
        "movies": ["아이언맨", "캐치 미 이프 유 캔"]
    },
    "INFJ": {
        "books": ["《데미안》 - 헤르만 헤세", "《작은 아씨들》 - 루이자 메이 올컷"],
        "movies": ["어바웃 타임", "월-E"]
    },
    "INFP": {
        "books": ["《연금술사》 - 파울로 코엘료", "《나미야 잡화점의 기적》 - 히가시노 게이고"],
        "movies": ["업", "월터의 상상은 현실이 된다"]
    },
    "ENFJ": {
        "books": ["《피터팬 죽이기》 - 김한민", "《모든 순간이 너였다》 - 하태완"],
        "movies": ["인사이드 아웃", "굿 윌 헌팅"]
    },
    "ENFP": {
        "books": ["《달러구트 꿈 백화점》 - 이미예", "《아몬드》 - 손원평"],
        "movies": ["라라랜드", "주토피아"]
    },
    "ISTJ": {
        "books": ["《공정하다는 착각》 - 마이클 샌델", "《성실한 나라의 앨리스》 - 이지수"],
        "movies": ["셜록 홈즈", "머니볼"]
    },
    "ISFJ": {
        "books": ["《어린 왕자》 - 생텍쥐페리", "《미움받을 용기》 - 기시미 이치로"],
        "movies": ["빅 히어로", "히든 피겨스"]
    },
    "ESTJ": {
        "books": ["《원씽》 - 게리 켈러", "《린 인》 - 셰릴 샌드버그"],
        "movies": ["크루엘라", "인턴"]
    },
    "ESFJ": {
        "books": ["《하루 1분 행복》 - 존 가든", "《말 그릇》 - 김윤나"],
        "movies": ["러브 액츄얼리", "미녀와 야수"]
    },
    "ISTP": {
        "books": ["《코딩의 신》 - 스티브 맥코넬", "《나는 왜 이 일을 하는가》 - 사이먼 시넥"],
        "movies": ["킹스맨", "테넷"]
    },
    "ISFP": {
        "books": ["《무례한 사람에게 웃으며 대처하는 법》 - 정문정", "《걷는 사람, 하정우》 - 하정우"],
        "movies": ["소울", "말할 수 없는 비밀"]
    },
    "ESTP": {
        "books": ["《트렌드 코리아》 - 김난도", "《나는 나로 살기로 했다》 - 김수현"],
        "movies": ["분노의 질주", "탑건: 매버릭"]
    },
    "ESFP": {
        "books": ["《지금, 이 순간》 - 에크하르트 톨레", "《죽고 싶지만 떡볶이는 먹고 싶어》 - 백세희"],
        "movies": ["맘마미아!", "엔칸토"]
    }
}

if mbti:
    st.subheader(f"✨ {mbti}에게 어울리는 추천 ✨")

    rec = recommendations[mbti]
    st.write("📚 **책 추천:**")
    for book in rec["books"]:
        st.write(f"- {book}")

    st.write("🎬 **영화 추천:**")
    for movie in rec["movies"]:
        st.write(f"- {movie}")

    st.write("---")
    st.success("📖 마음에 드는 책 한 권, 🎥 끌리는 영화 한 편 골라서 오늘은 감성 충전 어때? 💫")
