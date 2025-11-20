import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="범죄 장소 비율 시각화", layout="wide")

st.title("🚓 범죄 종류별 발생 장소 비율 분석")

# CSV 파일 로드 (루트 폴더)
df = pd.read_csv("경찰청_범죄 발생 장소별 통계_20241231.csv")

# 컬럼 구조 가정: [범죄종류, 장소, 비율]
# 실제 컬럼명에 따라 아래 부분을 수정해야 함
crime_col = "범죄종류"
place_col = "장소"
value_col = "비율"

# 범죄 종류 선택
crime_list = df[crime_col].unique()
select_crime = st.selectbox("📌 범죄 종류를 선택하세요", crime_list)

# 선택한 범죄 필터링
data = df[df[crime_col] == select_crime]

# 정렬
data = data.sort_values(value_col, ascending=False)

# Plotly 색 설정: 1등 보라색, 나머지는 회색 그라데이션
colors = ["#8e44ad"] + [f"rgba(149, 165, 166, {0.3 + 0.7*(i/len(data))})" for i in range(1, len(data)+1)]

fig = px.bar(
    data,
    x=place_col,
    y=value_col,
    title=f"🏙️ '{select_crime}' 발생 장소 비율",
)

fig.update_traces(marker_color=colors)
fig.update_layout(
    xaxis_title="장소",
    yaxis_title="비율 (%)",
    title_x=0.5,
)

st.plotly_chart(fig, use_container_width=True)

