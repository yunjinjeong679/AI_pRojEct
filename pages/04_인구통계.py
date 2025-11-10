import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(page_title="지역별 인구 연령 분포", layout="wide")

st.title("👩‍👩‍👧‍👦 지역별 인구 연령 분포 대시보드")
st.write("지역을 선택하면 연령대별 인구 분포를 꺾은선 그래프로 보여드려요 💫")

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
ages = [col.split("_")[-1] for col in cols_to_convert]
populations = [region_data[col] for col in cols_to_convert]

# Plotly 꺾은선 그래프
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=ages,
    y=populations,
    mode="lines+markers",
    line=dict(color="#4B9CD3", width=3),
    marker=dict(size=8),
    name="총 인구"
))

fig.update_layout(
    title=f"📊 {region}의 연령별 인구 분포",
    xaxis_title="연령대",
    yaxis_title="인구 수",
    template="plotly_white",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

st.caption("데이터 출처: 행정안전부 주민등록 인구통계 (2025년 10월 기준)")
