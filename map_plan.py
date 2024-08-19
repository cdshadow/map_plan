import streamlit as st
import requests

# 브이월드 API 키 설정
apikey = 'DB7E4D5F-219B-3F5A-8E2F-EC32EED95A2C'

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
            st.error("JSON 파싱에 실패했습니다. 응답이 JSON 형식이 아닐 수 있습니다.")
            st.write("Raw Response Content (HTML):", response.text)
            return None, None
    else:
        st.error("API 요청이 실패했습니다.")
        return None, None

# 주소 입력
address = st.text_input("주소를 입력하세요:", "대전광역시 유성구 전민로 37")

# 좌표 반환 및 출력
latitude, longitude = geocode_address_vworld(address)
if latitude and longitude:
    st.write(f"위도: {latitude}, 경도: {longitude}")
else:
    st.write("좌표를 찾을 수 없습니다.")
