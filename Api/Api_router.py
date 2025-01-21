import requests
from fastapi import APIRouter
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from .Api_schema import SearchDTO

router = APIRouter(
    prefix="/api",
    tags=["api"]
)

SERVICE_KEY = "khO0xRXeL2lCzz88ljXUxRVC0S7H7E2fg2t0190q0nFsfhmpSwS9DQA2bIdqy2wqGgoJKFYOBNE2SfSnN8vYvQ=="

@router.post("/MainPage")
async def info_festival():
    return search_festival()

@router.post("/SearchPage")
async def search_keyword_festival(SDTO: SearchDTO):
    return search_keyword(SDTO.numOfRows, SDTO.pageNo, SDTO.contentTypeld, SDTO.keyword)

def search_festival():
    BASE_URL = "http://apis.data.go.kr/B551011/KorService1/searchFestival1"

    # 지역 코드 매핑
    area_codes = [1, 2, 3, 4, 5, 6, 7, 8, 31, 32, 33, 34, 35, 36, 37, 38, 39]

    # 결과를 저장할 딕셔너리
    all_festivals = {}

    today = datetime.now()
    two_week_later = today + timedelta(days=14)

    # 날짜 포맷팅 (yyyyMMdd 형식)
    event_start_date = today.strftime("%Y%m%d")
    event_end_date = two_week_later.strftime("%Y%m%d")

    # API 요청 파라미터
    for area_code in area_codes:
        params = {
            "serviceKey": SERVICE_KEY,  # 서비스 키
            "numOfRows": 5,           # 한 번에 가져올 데이터 수 **(수정된 부분)**
            "pageNo": 1,               # 페이지 번호
            "MobileOS": "ETC",         # OS 정보 (ETC: 기타)
            "MobileApp": "AppTest",    # 어플리케이션 이름
            "areaCode": area_code,     # 지역 코드
            "eventStartDate": event_start_date,
            "eventEndDate": event_end_date,
            "_type": "json"            # JSON 형식으로 응답
        }

        # API 요청
        try:
            response = requests.get(BASE_URL, params=params)

            # JSON 변환 시도
            try:
                data = response.json()

                # 축제 정보 저장
                if "response" in data and "body" in data["response"]:
                    festivals = data["response"]["body"].get("items", {}).get("item", [])

                    # 필요한 데이터만 추출
                    refined_festivals = []
                    for festival in festivals:
                        refined_festival = {
                            "addr1": festival.get("addr1"),
                            "contentid": festival.get("contentid"),
                            "contenttypeid": festival.get("contenttypeid"),
                            "eventstartdate": festival.get("eventstartdate"),
                            "eventenddate": festival.get("eventenddate"),
                            "firstimage": festival.get("firstimage"),
                            "firstimage2": festival.get("firstimage2"),
                            "tel": festival.get("tel"),
                            "title": festival.get("title")
                        }
                        refined_festivals.append(refined_festival)

                    all_festivals[area_code] = refined_festivals
                else:
                    all_festivals[area_code] = []  # 해당 지역에 축제가 없으면 빈 리스트 추가

            except Exception as e:
                all_festivals[area_code] = {"error": f"JSON 변환 에러: {str(e)}"}

        except requests.exceptions.RequestException as e:
            all_festivals[area_code] = {"error": f"Request 에러: {str(e)}"}

    # 결과 반환 **(수정된 부분)**
    return JSONResponse(content=all_festivals)

def image_festival(contentID):
    BASE_URL = "http://apis.data.go.kr/B551011/KorService1/detailImage1"

    # API 요청 파라미터
    params = {
        "MobileOS": "ETC",
        "MobileApp": "AppTest",
        "_type": "json",
        "contentId": contentID,
        "imageYN": "Y",
        "subImageYN": "Y",
        "numOfRows": 10,
        "pageNo": 1,
        "serviceKey": SERVICE_KEY
    }

    # API 요청
    try:
        response = requests.get(BASE_URL, params=params)

    # 응답 상태 코드 확인
        if response.status_code == 200:
            # JSON 응답을 파싱
            data = response.json()

            # 결과 확인 및 처리
            if 'response' in data and 'body' in data['response'] and 'items' in data['response']['body']:
                # items는 딕셔너리 내에 'item' 키로 있음
                images = data['response']['body']['items']['item']

                # 포스터 이미지를 먼저 분리
                poster_image = None
                other_images = []

                for img in images:
                    if "포스터" in img['imgname']:
                        poster_image = img  # 포스터 이미지 찾으면 따로 저장
                    else:
                        other_images.append(img)  # 나머지 이미지는 다른 리스트에 저장

                # 포스터 이미지를 첫 번째로 추가하고 나머지 이미지를 뒤에 추가
                if poster_image:
                    images = [poster_image] + other_images
                else:
                    images = other_images

                
                #for img in images:
                    #print(f"이미지 이름: {img['imgname']}")
                    #print(f"원본 이미지 URL: {img['originimgurl']}")
                    #print(f"작은 이미지 URL: {img['smallimageurl']}")
                    #print(f"저작권 구분 코드: {img['cpyrhtDivCd']}")
                    #print("-" * 50)
                return JSONResponse(content=images)

            else:
                JSONResponse(status_code=500, content={"message": f"이미지를 찾을 수 없습니다."})
        else:
            return JSONResponse(status_code=500, content={"message": f"API 요청 실패, 상태 코드 {response.status_code}"})

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"에러 발생: {str(e)}"})
    

def search_keyword(numOfRows, pageNo, contentTypeld, keyword):
    BASE_URL = "http://apis.data.go.kr/B551011/KorService1/searchKeyword1"

    params = {
        "numOfRows": numOfRows,
        "pageNo": pageNo,
        "MobileOS": "ETC",
        "MobileApp": "AppTest",
        "_type": "json",
        "listYN": "Y",
        "arrange": "O",
        "keyword": keyword,
        "contentTypeId": contentTypeld,
        "serviceKey": SERVICE_KEY
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 처리

        try:
            data = response.json()  # 응답이 JSON 형식이어야 함
        except ValueError:
            return {"message": "응답 데이터가 JSON 형식이 아닙니다."}

        if data.get("response", {}).get("header", {}).get("resultCode") == "0000":
            items = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])
            if isinstance(items, list) and items:
                festivals = []
                for item in items:
                    contentid = item.get('contentid')
                    contenttypeid = item.get('contenttypeid')
                    eventStartDate, eventEndDate = contentID(contentid, contenttypeid)  # contentID 함수 호출
                    festival = {
                        "title": item.get('title', '이름 없음'),
                        "address": item.get('addr1', '주소 없음'),
                        "image": item.get('firstimage', '이미지 없음'),
                        "contentid": item.get('contentid', '이미지 없음'),
                        "contenttypeid": item.get('contenttypeid', '이미지 없음'),
                        "eventStartDate": eventStartDate,
                        "eventEndDate": eventEndDate,
                    }
                    festivals.append(festival)
                return festivals  # JSONResponse 대신 일반적으로 리스트 반환
            else:
                return {"message": "검색된 항목이 없습니다."}

        else:
            result_msg = data.get("response", {}).get("header", {}).get("resultMsg", "알 수 없는 오류")
            return {"message": f"API 호출 오류: {result_msg}"}

    except requests.exceptions.RequestException as e:
        return {"message": f"API 요청 중 오류 발생: {e}"}
    except Exception as e:
        return {"message": f"에러 발생: {e}"}


def contentID(contentid, contenttypeid):
    BASE_URL = "http://apis.data.go.kr/B551011/KorService1/detailIntro1"

    params = {
        "MobileOS": "ETC",
        "MobileApp": "AppTest",
        "_type": "json",
        "contentId": contentid,        # 콘텐츠 ID
        "contentTypeId": contenttypeid, # 콘텐츠 타입 ID
        "serviceKey": SERVICE_KEY        # 서비스 키
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 처리

        data = response.json()

        # 응답 구조 확인
        items = data.get('response', {}).get('body', {}).get('items', {}).get('item', [])
        if items:
            event = items[0]
            eventStartDate = event.get('eventstartdate', '정보 없음')
            eventEndDate = event.get('eventenddate', '정보 없음')
            return eventStartDate, eventEndDate
        else:
            return '정보 없음', '정보 없음'  # items가 비었을 경우 처리
    except requests.exceptions.RequestException as e:
        return '정보 없음', '정보 없음'  # API 요청 실패 시 처리
    except Exception as e:
        return '정보 없음', '정보 없음'  # 예외 발생 시 처리
