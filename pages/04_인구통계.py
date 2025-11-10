import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# 페이지 설정
st.set_page_config(page_title="지역별 인구 연령 분포", layout="wide")

st.title("👶 지역별 세밀한 인구 연령 분포")
st.write("지역을 선택하면 **1살 단위로 나눈 인구 분포**를 꺾은선 그래프로 보여드려요 💫")

# CSV 파일 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("population.csv", encoding="cp949")
    return df

df = load_data()

# 숫자형 변환
cols_to_convert = [col for col in df.columns if "계_" in col and "~" in col]
for col in cols_to_convert:
    df[col] = df[col].astype(str).str.replace(",", "").astype(int)

# 지역 선택
region = st.selectbox("📍 지역을 선택하세요:", df["행정구역"].unique())

# 선택한 지역 데이터
region_data = df[df["행정구역"] == region].iloc[0]

# 그래프용 데이터 구성
age_groups = [col.split("_")[-1] for col in cols_to_convert]
populations = [region_data[col] for col in cols_to_convert]

# 1살 단위로 세분화 (0~9세 → 0~9, 각각 동일 분포로 나눔)
fine_ages = []
fine_pops = []

for group, pop in zip(age_groups, populations):
    if "~" in group:
        start, end = map(int, group.replace("세", "").split("~"))
        ages = list(range(start, end + 1))
        # 각 나이에 동일하게 인구 분포 (단순 분할)
        per_age = pop / len(ages)
        fine_ages.extend(ages)
        fine_pops.extend([per_age] * len(ages))
    else:
        fine_ages.append(int(group.replace("세", "").replace("이상", "")))
        fine_pops.append(pop)

# Plotly 그래프
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=fine_ages,
    y=fine_pops,
    mode="lines+markers",
    line=dict(color="#FF7F50", width=2),
    marker=dict(size=4),
    name="총 인구 (1살 단위)"
))

fig.update_layout(
    title=f"📊 {region}의 1살 단위 인구 분포",
    xaxis_title="나이 (세)",
    yaxis_title="인구 수",
    template="plotly_white",
    hovermode="x unified",
    width=900,   # 🔹 그래프 폭을 기본의 1/3 수준으로 줄임
    height=500,
    margin=dict(l=40, r=40, t=80, b=40)
)

st.plotly_chart(fig, use_container_width=False)

st.caption("데이터 출처: 행정안전부 주민등록 인구통계 (2025년 10월 기준)")
