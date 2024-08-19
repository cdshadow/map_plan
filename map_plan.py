import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import requests

# 브이월드 API 키 설정
apikey = 'DB7E4D5F-219B-3F5A-8E2F-EC32EED95A2C'

# GitHub raw content URL의 data.csv 파일 경로
file_path = 'data.csv'

# Streamlit 설정
st.set_page_config(layout="wide")

# 데이터 파일 경로
shp_file_path_1f = 'https://raw.githubusercontent.com/cdshadow/map_plan/main/1f_2.shp'
shp_file_path_3f = 'https://raw.githubusercontent.com/cdshadow/map_plan/main/3f_2.shp'

# 주소를 입력받는 입력창 생성
address = st.text_input("주소를 입력하세요:", "대전광역시 유성구 전민로 37")

# 브이월드 API를 통해 주소를 지오코딩하는 함수
def geocode_address_vworld(address):
    apiurl = 'https://api.vworld.kr/req/address?'
    params = {
        'service': 'address',
        'request': 'getcoord',
        'crs': 'epsg:4326',
        'address': address,
        'format': 'json',
        'type': 'PARCEL',  # 'PARCEL'은 도로명 주소, 'ROAD'는 지번 주소
        'key': apikey
    }
    
    response = requests.get(apiurl, params=params)
    st.write("API Response Status Code:", response.status_code)
    st.write("API Response Content:", response.text)  # JSON으로 파싱하기 전에 응답 내용을 출력
    
    if response.status_code == 200:
        try:
            data = response.json()
            if data['response']['status'] == 'OK':
                x = data['response']['result']['point']['x']
                y = data['response']['result']['point']['y']
                return float(y), float(x)  # 브이월드는 (x, y) 순서로 좌표를 반환
            else:
                st.error("주소를 찾을 수 없습니다.")
                return None, None
        except requests.exceptions.JSONDecodeError:
            st.error("JSON 파싱에 실패했습니다.")
            return None, None
    else:
        st.error("API 요청이 실패했습니다.")
        return None, None

# 입력된 주소를 지오코딩하여 지도 중심 좌표 설정
latitude, longitude = geocode_address_vworld(address)

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

    # 입력된 주소에 마커 추가
    folium.Marker([lat, lon],
                  popup=folium.Popup(f'<b>{address}</b>', max_width=200),
                  icon=folium.Icon(color='red', icon='bookmark')
                 ).add_to(map_obj)
    
    # 레이어 컨트롤 추가
    folium.LayerControl().add_to(map_obj)

    return map_obj

# 주소가 유효한 경우에만 지도를 생성하고 표시
if latitude and longitude:
    st.header('대전광역시 지도')
    map_display = create_map(latitude, longitude)
    st_folium(map_display, width=1200, height=700)
