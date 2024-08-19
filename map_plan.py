import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

# GitHub raw content URL의 data.csv 파일 경로
file_path = 'data.csv'

# Streamlit 설정
st.set_page_config(layout="wide")

# 데이터 파일 경로
shp_file_path_1f = 'https://raw.githubusercontent.com/cdshadow/map_plan/main/1f_2.shp'
shp_file_path_3f = 'https://raw.githubusercontent.com/cdshadow/map_plan/main/3f_2.shp'

# 지오코딩을 위한 Nominatim 초기화
geolocator = Nominatim(user_agent="geoapiExercises")

# 주소를 입력받는 입력창 생성
address = st.text_input("주소를 입력하세요:", "대전 유성구 전민로38번길 7")

# 주소를 지오코딩하여 위도와 경도를 얻는 함수
def geocode_address(address):
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    else:
        st.error("주소를 찾을 수 없습니다.")
        return None, None

# 입력된 주소를 지오코딩하여 지도 중심 좌표 설정
latitude, longitude = geocode_address(address)

# Folium 지도 생성 함수
def create_map(lat, lon):
    # Folium 지도 설정 (입력된 주소를 중심으로)
    map_obj = folium.Map(
        location=[lat, lon],
        zoom_start=16,  # 줌 레벨 조정
    )

    # 1f.shp 파일 불러오기
    gdf_1f = gpd.read_file(shp_file_path_1f)

    # EPSG 5179에서 EPSG 4326으로 좌표계 변환
    gdf_1f = gdf_1f.to_crs(epsg=4326)

    # 1f 레이어 추가 (검정색 선, 두께 0.5)
    folium.GeoJson(
        gdf_1f,
        name='1f 레이어',
        style_function=lambda feature: {
            'color': 'red',
            'weight': 0.5,
        }
    ).add_to(map_obj)

    # 3f.shp 파일 불러오기
    gdf_3f = gpd.read_file(shp_file_path_3f)

    # EPSG 5179에서 EPSG 4326으로 좌표계 변환
    gdf_3f = gdf_3f.to_crs(epsg=4326)

    # 3f 레이어 추가 (검정색 선, 두께 0.5)
    folium.GeoJson(
        gdf_3f,
        name='3f 레이어',
        style_function=lambda feature: {
            'color': 'red',
            'weight': 0.5,
        }
    ).add_to(map_obj)

    # 레이어 컨트롤 추가
    folium.LayerControl().add_to(map_obj)

    return map_obj

# 주소가 유효한 경우에만 지도를 생성하고 표시
if latitude and longitude:
    st.header('대전광역시 지도')
    map_display = create_map(latitude, longitude)
    st_folium(map_display, width=1200, height=700)
