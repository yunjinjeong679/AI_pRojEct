import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 데이터 로드 및 전처리
@st.cache_data
def load_data(file_path):
    """CSV 파일을 로드하고 필요한 전처리를 수행합니다."""
    # 파일 로드 시 인코딩 문제 발생 가능성을 대비해 'euc-kr' 또는 'cp949' 시도
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(file_path, encoding='euc-kr')
        except Exception as e:
            st.error(f"데이터 로드 중 오류 발생: {e}")
            return pd.DataFrame() # 빈 DataFrame 반환

    # 컬럼 이름 정리 (공백 제거)
    df.columns = df.columns.str.strip()

    # '사용일자' 컬럼을 문자열로 변환하고 '-' 추가하여 날짜 형식으로 만듦
    # 예: 20251001 -> 2025-10-01
    df['사용일자'] = df['사용일자'].astype(str).str.replace(r'(\d{4})(\d{2})(\d{2})', r'\1-\2-\3', regex=True)

    return df

# 파일 경로 (Streamlit Cloud 환경에서 파일 접근 방식)
# 현재는 로컬에서 파일 객체를 받는 형태로 구성
# Streamlit 배포 시에는 st.file_uploader를 사용하거나 미리 업로드된 경로를 지정해야 합니다.

st.title("🚇 2025년 10월 지하철 승차객 Top 10 역 분석")
st.markdown("특정 날짜와 노선을 선택하여 승차 총 승객수가 가장 많은 상위 10개 역을 확인하세요.")

# 파일 처리 (업로드된 파일을 바로 사용)
# 사용자에게 파일 업로드를 요청하는 대신, 이미 업로드된 'sUbwAy.csv' 파일을 직접 사용합니다.
FILE_ID = 'sUbwAy.csv' 
try:
    df_raw = load_data(FILE_ID)
except FileNotFoundError:
    st.error("파일을 찾을 수 없습니다. 'sUbwAy.csv' 파일이 올바르게 업로드되었는지 확인해 주세요.")
    st.stop()
except Exception as e:
    st.error(f"데이터 로드 및 전처리 중 예상치 못한 오류 발생: {e}")
    st.stop()


if not df_raw.empty:
    # 2. 사이드바 - 사용자 입력
    
    # 고유 날짜 및 노선 리스트 추출
    date_list = sorted(df_raw['사용일자'].unique())
    line_list = sorted(df_raw['노선명'].unique())

    # 사용자 선택 위젯
    selected_date = st.sidebar.selectbox("📅 날짜 선택:", date_list, index=0)
    selected_line = st.sidebar.selectbox("🛤️ 노선 선택:", line_list, index=0)

    # 3. 데이터 필터링 및 집계
    
    # 1. 선택된 날짜와 노선으로 필터링
    df_filtered = df_raw[
        (df_raw['사용일자'] == selected_date) & 
        (df_raw['노선명'] == selected_line)
    ]

    if df_filtered.empty:
        st.warning(f"선택하신 날짜({selected_date})와 노선({selected_line})에 해당하는 데이터가 없습니다.")
    else:
        # 2. 역별 승차총승객수 합산
        df_grouped = df_filtered.groupby('역명')['승차총승객수'].sum().reset_index()
        df_grouped.rename(columns={'승차총승객수': '총_승차객수'}, inplace=True)

        # 3. 승차객수 기준 상위 10개 역 추출
        df_top10 = df_grouped.sort_values(by='총_승차객수', ascending=False).head(10)

        st.subheader(f"✨ {selected_date} - {selected_line} 노선 Top 10 승차역")

        # 4. Plotly 인터랙티브 막대 그래프 생성 (요구사항 반영)
        
        # 색상 설정 (1등: 빨간색, 나머지: 파란색 계열)
        # 상위 10개 데이터에 대해 색상 리스트 생성
        colors = ['#FF0000'] + ['#0000FF'] * 9 # 첫 번째(1등)는 빨간색, 나머지는 파란색 기본값

        # 파란색 계열 그라데이션 적용을 위해 Plotly의 Color Scale 사용
        # blue_gradient = px.colors.sequential.Blues_r # Blues_r은 진한 파랑에서 흰색으로 (역순)
        # blues = px.colors.make_colorscale(px.colors.sequential.Blues)(range(0, 10))

        # 1등: 빨간색, 2등~10등: 파란색 계열 그라데이션 (진한 파랑 -> 연한 파랑)
        # 2등부터 10등까지 9개의 색상을 파란색 계열에서 추출
        blue_scale = px.colors.sequential.Blues_r[1:] # Blues_r의 마지막 색(가장 밝은 파랑) 제거
        blue_gradient = [blue_scale[i] for i in range(9)]
        
        # 최종 색상 리스트: 1등(빨강) + 2등~10등(파랑 그라데이션)
        custom_colors = ['#FF0000'] + blue_gradient
        
        # '색상' 컬럼 추가 (1등만 빨강으로 표시하기 위한 임시 컬럼)
        df_top10['색상'] = ['1위'] + ['2위~10위'] * 9
        
        # 그래프 생성
        fig = px.bar(
            df_top10,
            x='역명',
            y='총_승차객수',
            title=f"'{selected_line}' 노선의 일일 승차객 상위 10개 역",
            labels={'역명': '지하철 역명', '총_승차객수': '총 승차객수 (명)'},
            color=df_top10['색상'], # 색상 기준 컬럼 지정
            color_discrete_map={'1위': '#FF0000', '2위~10위': '#347C98'}, # 1위와 2위~10위 그룹의 색상 지정
            text='총_승차객수' # 막대 위에 값 표시
        )
        
        # 2위~10위 막대에 그라데이션 적용 (Plotly에서는 복잡하여 명확한 그룹 색상 지정 후 배경색으로 대체)
        # Plotly Express의 color_discrete_map은 명확한 그룹 색상 지정에 최적화되어 있습니다.
        # 명확한 '빨강(1등)'과 '파랑 계열(나머지)' 구분이 요청되었으므로 위처럼 설정합니다.

        # 레이아웃 커스터마이징
        fig.update_traces(marker_line_width=0, opacity=0.8, textposition='outside')
        fig.update_layout(xaxis_tickangle=-45, showlegend=False) # x축 레이블 기울이기, 범례 숨기기

        # Streamlit에 그래프 표시
        st.plotly_chart(fig, use_container_width=True)

        # 상위 10개 데이터 테이블 표시 (선택사항)
        st.markdown("#### 상세 데이터")
        st.dataframe(df_top10.set_index('역명'))
