import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="국가별 MBTI 시각화", layout="wide")
st.title("🌍 국가별 MBTI 비율 시각화")

# CSV 파일 자동 탐색
csv_files = [f for f in os.listdir() if f.endswith(".csv")]
if not csv_files:
    st.error("❌ CSV 파일이 없습니다. 같은 폴더에 'countriesMBTI_16types.csv'를 업로드해주세요.")
    st.stop()

# CSV 불러오기
df = pd.read_csv(csv_files[0])
st.write("📄 불러온 데이터 미리보기:", df.head())

# 컬럼 이름 소문자로 통일
df.columns = [c.strip().lower() for c in df.columns]

# 필요한 컬럼 자동 감지
possible_country_cols = ["country", "nation", "국가"]
possible_mbti_cols = ["mbti", "type", "유형"]
possible_percentage_cols = ["percentage", "ratio", "percent", "비율"]

def find_col(possible_names):
    for name in possible_names:
        if name in df.columns:
            return name
    return None

country_col = find_col(possible_country_cols)
mbti_col = find_col(possible_mbti_cols)
percent_col = find_col(possible_percentage_cols)

# 컬럼이 누락된 경우 경고
if not all([country_col, mbti_col, percent_col]):
    st.error(f"⚠️ 필요한 컬럼이 누락되었습니다.\n"
             f"현재 컬럼 목록: {list(df.columns)}\n"
             f"필요한 컬럼: country, MBTI, percentage (또는 유사 이름)")
    st.stop()

# 국가 선택
countries = sorted(df[country_col].unique())
selected_country = st.selectbox("🌏 국가를 선택하세요:", countries)

# 선택한 국가 필터링
country_df = df[df[country_col] == selected_country].sort_values(by=percent_col, ascending=False)

# 색상 설정
colors = ["red"] + px.colors.sequential.Blues[len(country_df) - 1]

# 그래프 생성
fig = px.bar(
    country_df,
    x=mbti_col,
    y=percent_col,
    text=percent_col,
    color=country_df.index,
    color_discrete_sequence=colors,
)

fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
fig.update_layout(
    title=f"{selected_country}의 MBTI 유형 분포",
    xaxis_title="MBTI 유형",
    yaxis_title="비율 (%)",
    showlegend=False,
    plot_bgcolor="white",
)

st.plotly_chart(fig, use_container_width=True)
