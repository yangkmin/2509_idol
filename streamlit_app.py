import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. 기본 페이지 설정 ---
st.set_page_config(
    page_title="인터랙티브 데이터 세상",
    page_icon="✨",
    layout="wide"
)

# --- 2. 데이터 불러오기 ---
@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    data['release_date'] = pd.to_datetime(data['release_date'])
    return data

data = load_data("kpop_albums.csv")

# --- 3. 대시보드 제목과 설명 추가 ---
st.title("✨ 스트림릿으로 펼치는 인터랙티브 데이터 세상")
st.write("(클릭, 선택, 입력! 나만의 대시보드를 만들고 체험하기)")
st.write("---")

# --- 4. 인터랙티브 위젯 (사이드바) ---
st.sidebar.header("아티스트를 선택하세요")
artist_list = sorted(data['artist'].unique())
selected_artist = st.sidebar.selectbox(
    "보고 싶은 아티스트는?",
    artist_list
)

# --- 5. 선택에 따른 데이터 필터링 ---
filtered_data = data[data['artist'] == selected_artist]

# --- 6. 데이터 시각화 (한 그룹 분석) ---
st.header(f"💽 {selected_artist} 앨범 판매량 분석")
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("앨범 정보")
    st.dataframe(
        filtered_data[['release_date', 'album_title', 'sales']]
        .sort_values(by='release_date')
        .style.format({
            "release_date": "{:%Y-%m-%d}",  # 날짜 형식을 '연-월-일'로 깔끔하게 변경
            "sales": "{:,}장"              # 판매량에 천 단위 콤마와 '장'을 붙임
        }),
        hide_index=True,
        use_container_width=True
    )

with col2:
    st.subheader("앨범별 판매량 그래프")
    fig_bar = px.bar(
        filtered_data.sort_values(by='release_date'),
        x='album_title',
        y='sales',
        labels={'album_title': '앨범 제목', 'sales': '판매량 (단위: 장)'},
        color='album_title'
    )
    fig_bar.update_layout(yaxis_tickformat=',', showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)

st.write("---")

# --- 7. 라이벌 그룹 비교 분석 기능 ---
st.header("⚔️ 라이벌 그룹 비교 분석")

selected_rivals = st.multiselect(
    '비교하고 싶은 아티스트를 2팀 이상 선택하세요.',
    artist_list,
    default=[]
)

if len(selected_rivals) >= 2:
    rival_data = data[data['artist'].isin(selected_rivals)]
    st.subheader("앨범 발매일 기준 판매량 추이 비교")
    fig_line = px.line(
        rival_data.sort_values(by='release_date'),
        x='release_date',
        y='sales',
        color='artist',
        markers=True,
        hover_name='album_title',
        labels={
            'release_date': '발매일',
            'sales': '판매량 (단위: 장)',
            'artist': '아티스트'
        }
    )
    fig_line.update_layout(yaxis_tickformat=',')
    st.plotly_chart(fig_line, use_container_width=True)
else:
    st.info("그래프를 보려면 비교할 아티스트를 2팀 이상 선택해주세요.")

# --- 8. 전체 데이터 보여주기 ---
with st.expander("전체 원본 데이터 보기"):
    st.dataframe(
        data.style.format({"release_date": "{:%Y-%m-%d}"}), # 날짜 형식 동일하게 적용
        hide_index=True,
        use_container_width=True
    )
