import streamlit as st
import pandas as pd
import plotly.express as px

# 제목
st.title("🌍 국가별 MBTI 비율 시각화")

# CSV 파일 불러오기
df = pd.read_csv("countriesMBTI_16types.csv")

# 국가 목록
countries = df["country"].unique()
selected_country = st.selectbox("국가를 선택하세요:", countries)

# 선택한 국가 데이터만 필터링
country_df = df[df["country"] == selected_country]

# MBTI별 비율 정렬
country_df = country_df.sort_values(by="percentage", ascending=False)

# 색상 설정: 1등은 빨간색, 나머지는 그라데이션 (파란색 → 회색)
colors = ["red"] + px.colors.sequential.Blues[len(country_df) - 1]

# Plotly 막대그래프 생성
fig = px.bar(
    country_df,
    x="MBTI",
    y="percentage",
    text="percentage",
    color=country_df.index,  # 색상 구분용 (dummy)
    color_discrete_sequence=colors,
)

# 그래프 꾸미기
fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
fig.update_layout(
    title=f"{selected_country}의 MBTI 유형 분포",
    xaxis_title="MBTI 유형",
    yaxis_title="비율 (%)",
    showlegend=False,
    plot_bgcolor="white",
)

# 그래프 출력
st.plotly_chart(fig, use_container_width=True)
