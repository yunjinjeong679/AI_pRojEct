import streamlit as st
import folium
from streamlit.components.v1 import html

# 🌟 페이지 기본 설정
st.set_page_config(page_title="서울 관광지 TOP10 지도", page_icon="🗺️", layout="wide")

st.title("🗺️ 외국인들이 좋아하는 서울 관광지 TOP10")
st.markdown("서울의 인기 명소를 지도에서 한눈에 확인해보세요!")

# 📍 서울 인기 관광지 데이터
locations = [
    {"name": "경복궁 (Gyeongbokgung Palace)", "lat": 37.579617, "lon": 126.977041, "desc": "조선시대의 대표 궁궐로 전통문화의 중심지!"},
    {"name": "명동 (Myeongdong)", "lat": 37.563757, "lon": 126.982684, "desc": "쇼핑과 길거리 음식의 천국 🇰🇷"},
    {"name": "남산타워 (Namsan Seoul Tower)", "lat": 37.551169, "lon": 126.988227, "desc": "서울 전경을 한눈에! 연인들의 데이트 명소 💕"},
    {"name": "홍대 (Hongdae)", "lat": 37.556318, "lon": 126.922651, "desc": "젊음과 예술이 넘치는 거리 🎨"},
    {"name": "북촌 한옥마을 (Bukchon Hanok Village)", "lat": 37.582604, "lon": 126.983998, "desc": "전통과 현대가 공존하는 아름다운 한옥 거리 🏠"},
    {"name": "이태원 (Itaewon)", "lat": 37.534773, "lon": 126.994097, "desc": "다양한 문화와 외국인들이 즐겨 찾는 거리 🌏"},
    {"name": "동대문디자인플라자 (DDP)", "lat": 37.566479, "lon": 127.009071, "desc": "미래적인 디자인의 랜드마크 💡"},
    {"name": "롯데월드 (Lotte World)", "lat": 37.511000, "lon": 127.098000, "desc": "실내외 놀이공원과 쇼핑몰이 함께! 🎡"},
    {"name": "잠실 롯데타워 (Lotte World Tower)", "lat": 37.513068, "lon": 127.102503, "desc": "대한민국에서 가장 높은 빌딩 🏙️"},
    {"name": "청계천 (Cheonggyecheon Stream)", "lat": 37.569228, "lon": 126.977103, "desc": "도심 속 힐링 산책로 🌿"},
]

# 🗺️ 지도 생성
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)

# 📍 마커 추가
for place in locations:
    folium.Marker(
        location=[place["lat"], place["lon"]],
        popup=f"<b>{place['name']}</b><br>{place['desc']}",
        tooltip=place["name"],
        icon=folium.Icon(color="red", icon="star")
    ).add_to(m)

# 🌍 지도 표시
html(m._repr_html_(), height=600)
