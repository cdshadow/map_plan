import streamlit as st
import pandas as pd
import plotly.express as px

tab1, tab2, tab3, tab4 = st.tabs(['대전시 년도별 순이동', '대전시 년도별·지역별 순이동', '세종시 년도별 순이동', '세종시 년도별·지역별 순이동'])

# GitHub raw content URL의 data.csv 파일 경로
file_path = 'https://raw.githubusercontent.com/cdshadow/dj_move/main/data.csv'
file_path2 = 'https://raw.githubusercontent.com/cdshadow/dj_move/main/data2.csv'
file_path3 = 'https://raw.githubusercontent.com/cdshadow/dj_move/main/data3.csv'
file_path4 = 'https://raw.githubusercontent.com/cdshadow/dj_move/main/data4.csv'

# 데이터를 캐시하여 로딩
@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path, encoding='cp949')
    # 년도를 문자열로 변환
    data['년도'] = data['년도'].astype(str)
    return data

# data.csv 파일 로드
data = load_data(file_path)

# data2.csv 파일 로드
data2 = load_data(file_path2)

# data3.csv 파일 로드
@st.cache_data
def load_data3(file_path3):
    data3 = pd.read_csv(file_path3, encoding='cp949')
    # 년도를 문자열로 변환
    data3['년도'] = data3['년도'].astype(str)
    return data3

data3 = load_data3(file_path3)

# data4.csv 파일 로드
@st.cache_data
def load_data4(file_path4):
    data4 = pd.read_csv(file_path4, encoding='cp949')
    # 년도를 문자열로 변환
    data4['년도'] = data4['년도'].astype(str)
    return data4

data4 = load_data4(file_path4)

with tab1:
    # Plotly를 이용한 꺾은선 그래프
    fig = px.line(data, x='년도', y='순이동 인구수', title='2001년~2023년 대전시 순이동 변화', markers=True)
    
    # x축의 모든 연도를 표시하도록 수정
    fig.update_xaxes(tickmode='linear', tick0=data['년도'].min(), dtick=1)
    
    # y축의 간격을 5,000 단위로 설정
    fig.update_yaxes(tick0=0, dtick=5000)
    
    # 그래프 커스터마이징 (선택 사항)
    fig.update_traces(line=dict(width=2))
    fig.update_layout(xaxis_title='년도', yaxis_title='순이동 인구수')
    
    # Streamlit에서 Plotly 그래프를 표시
    st.plotly_chart(fig)
    
    # 데이터 확인
    st.table(data)

with tab2:
    # Plotly를 이용한 꺾은선 그래프
    fig = px.line(data2, x='년도', y='순이동 인구수', color='지역', title='2001년~2023년 대전시 지역별 순이동 변화', markers=True)
    
    # x축의 모든 연도를 표시하도록 수정
    fig.update_xaxes(tickmode='linear', tick0=data2['년도'].min(), dtick=1)
    
    # y축의 간격을 5,000 단위로 설정
    fig.update_yaxes(tick0=0, dtick=5000)
    
    # 그래프 커스터마이징 (선택 사항)
    fig.update_traces(line=dict(width=2))
    fig.update_layout(xaxis_title='년도', yaxis_title='순이동 인구수')
    
    # Streamlit에서 Plotly 그래프를 표시
    st.plotly_chart(fig)
    
    # 데이터 확인
    st.table(data2.groupby(['년도', '지역'])['순이동 인구수'].sum().reset_index())

with tab3:
    # Plotly를 이용한 꺾은선 그래프
    fig = px.line(data3, x='년도', y='순이동 인구수', title='2001년~2023년 세종시 순이동 변화', markers=True)
    
    # x축의 모든 연도를 표시하도록 수정
    fig.update_xaxes(tickmode='linear', tick0=data3['년도'].min(), dtick=1)
    
    # y축의 간격을 5,000 단위로 설정
    fig.update_yaxes(tick0=0, dtick=5000)
    
    # 그래프 커스터마이징 (선택 사항)
    fig.update_traces(line=dict(width=2))
    fig.update_layout(xaxis_title='년도', yaxis_title='순이동 인구수')
    
    # Streamlit에서 Plotly 그래프를 표시
    st.plotly_chart(fig)
    
    # 데이터 확인
    st.table(data3)

with tab4:
    # Plotly를 이용한 꺾은선 그래프
    fig = px.line(data4, x='년도', y='순이동 인구수', color='지역', title='2001년~2023년 세종시 지역별 순이동 변화', markers=True)
    
    # x축의 모든 연도를 표시하도록 수정
    fig.update_xaxes(tickmode='linear', tick0=data4['년도'].min(), dtick=1)
    
    # y축의 간격을 5,000 단위로 설정
    fig.update_yaxes(tick0=0, dtick=5000)
    
    # 그래프 커스터마이징 (선택 사항)
    fig.update_traces(line=dict(width=2))
    fig.update_layout(xaxis_title='년도', yaxis_title='순이동 인구수')
    
    # Streamlit에서 Plotly 그래프를 표시
    st.plotly_chart(fig)
    
    # 데이터 확인
    st.table(data4.groupby(['년도', '지역'])['순이동 인구수'].sum().reset_index())
