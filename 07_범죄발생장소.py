import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------
# Streamlit app: pages/crime_place_chart.py
# CSV (root): 경찰청_범죄 발생 장소별 통계_20241231.csv
# encoding: cp949 (euc-kr)
# ---------------------------

st.set_page_config(page_title="범죄 장소 비율 시각화", layout="wide")

st.title("🚓 범죄 종류별 발생 장소 비율 분석")

@st.cache_data
def load_data(path: str):
    # 여러 인코딩 시도
    for enc in ("cp949", "euc-kr", "utf-8", "latin1"):
        try:
            df = pd.read_csv(path, encoding=enc)
            return df
        except Exception:
            continue
    raise UnicodeDecodeError("Unable to decode CSV with tried encodings.")

# 파일 경로 (루트 폴더)
CSV_PATH = "경찰청_범죄 발생 장소별 통계_20241231.csv"

try:
    df_raw = load_data(CSV_PATH)
except Exception as e:
    st.error(f"CSV 파일을 읽는 중 오류가 발생했습니다: {e}")
    st.stop()

# 확인용
# st.write(df_raw.head())

# 컬럼 명 추출
cols = df_raw.columns.tolist()

# 앞의 두 컬럼이 범죄 분류라고 가정 (데이터에 따라 달라질 수 있음)
crime_cols = cols[:2]
place_cols = cols[2:]

# 범죄 표시용 라벨 생성
df = df_raw.copy()
if len(crime_cols) == 2:
    df["범죄종류"] = df[crime_cols[0]].astype(str) + " - " + df[crime_cols[1]].astype(str)
else:
    df["범죄종류"] = df[crime_cols[0]].astype(str)

# 장소별 컬럼들을 행으로 녹이기
melted = df.melt(id_vars=["범죄종류"], value_vars=place_cols, var_name="장소", value_name="건수")

# 건수가 숫자가 아닐 수 있으니 정리
melted["건수"] = pd.to_numeric(melted["건수"], errors="coerce").fillna(0)

# 범죄 종류 선택
crime_list = melted["범죄종류"].unique().tolist()
select_crime = st.selectbox("📌 범죄 종류를 선택하세요", crime_list)

# 선택한 범죄 필터
data = melted[melted["범죄종류"] == select_crime].copy()

# 장소별 합계 (혹시 중복 행이 있을 경우)
agg = data.groupby("장소", as_index=False)["건수"].sum()
agg = agg.sort_values("건수", ascending=False).reset_index(drop=True)

# 비율 계산
total = agg["건수"].sum()
if total == 0:
    st.warning("선택한 범죄에 대한 발생 건수가 0입니다. 다른 범죄를 선택해 보세요.")
    st.stop()
agg["비율"] = agg["건수"] / total * 100

# 색상: 1등 보라색, 나머지는 회색 그라데이션
n = len(agg)
colors = []
for i in range(n):
    if i == 0:
        colors.append("#8e44ad")  # 보라색
    else:
        if n == 1:
            gray_val = 200
        else:
            # 그라데이션을 연한 회색(230) -> 진한 회색(120)
            fraction = (i - 1) / max(1, n - 2)
            gray_val = int(230 - fraction * 110)
        hex_gray = f"#{gray_val:02x}{gray_val:02x}{gray_val:02x}"
        colors.append(hex_gray)

# Plotly bar
fig = px.bar(
    agg,
    x="장소",
    y="비율",
    text=agg["비율"].map(lambda v: f"{v:.1f}%"),
    title=f"🏙️ '{select_crime}' 발생 장소 비율",
)

# marker_color expects a single color or list matching number of bars
fig.update_traces(marker_color=colors, textposition="outside")
fig.update_layout(
    xaxis_title="장소",
    yaxis_title="비율 (%)",
    title_x=0.5,
    uniformtext_minsize=8,
    uniformtext_mode='hide',
    yaxis=dict(range=[0, max(agg['비율'].max()*1.15, 10)])
)

st.plotly_chart(fig, use_container_width=True)

# 하단에 테이블 표시 (원하면 숨길 수 있음)
with st.expander("원본 데이터(선택한 범죄) 보기", expanded=False):
    st.dataframe(agg)


# 사용법 안내
st.markdown("---")
st.markdown("**설치(로컬 테스트용)**: `pip install -r requirements.txt`

requirements.txt 파일에 `streamlit`, `pandas`, `plotly` 를 적어 주세요.")
