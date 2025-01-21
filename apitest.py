import requests
import json

# API 키 설정
SERVICE_KEY = "khO0xRXeL2lCzz88ljXUxRVC0S7H7E2fg2t0190q0nFsfhmpSwS9DQA2bIdqy2wqGgoJKFYOBNE2SfSnN8vYvQ=="

def get_event_details(content_id, content_type_id):
    # 기본 URL 설정
    BASE_URL = "http://apis.data.go.kr/B551011/KorService1/detailIntro1"

    # 요청 파라미터 설정
    params = {
        "MobileOS": "ETC",
        "MobileApp": "AppTest",
        "_type": "json",
        "contentId": content_id,        # 콘텐츠 ID
        "contentTypeId": content_type_id, # 콘텐츠 타입 ID
        "serviceKey": SERVICE_KEY        # 서비스 키
    }

    # API 요청 보내기
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        # 응답 성공 시 데이터 파싱
        data = response.json()

        # 응답 구조 확인
        items = data.get('response', {}).get('body', {}).get('items', {}).get('item', [])
        
        print(items)
        if items:
            event = items[0]

            print(f"이벤트 시작 날짜: {event.get('eventstartdate', '정보 없음')}")
            print(f"이벤트 종료 날짜: {event.get('eventenddate', '정보 없음')}")
        else:
            print("이벤트 정보가 없습니다.")
    else:
        print(f"API 요청 실패: {response.status_code}")

# 함수 호출 예시
get_event_details(content_id=2777865, content_type_id=12)
 