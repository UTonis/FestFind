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
async def get_main_festival():
    # 기본 URL 설정
    BASE_URL = "http://apis.data.go.kr/B551011/KorService1/searchFestival1"

    # 요청 파라미터 설정
    params = {
        "numOfRows": 50,
        "MobileOS": "ETC",
        "MobileApp": "AppTest",
        "_type": "json",
        "arrange": "A",
        "eventStartDate": 20250121,
        "serviceKey": SERVICE_KEY
    }

    # API 요청 보내기
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        # 응답 성공 시 데이터 파싱
        data = response.json()

        # JSON 데이터를 보기 좋게 출력
        #print(json.dumps(data, indent=4, ensure_ascii=False))

        # 특정 정보만 추출해서 보기 좋게 출력 (예시)
        if "response" in data and "body" in data["response"]:
            festivals = data["response"]["body"].get("items", {}).get("item", [])
            refined_festivals = []
            if festivals:
                for festival in festivals:
                    title = festival.get("title", "제목 없음")
                    start_date = festival.get("eventstartdate", "시작일 미제공")
                    end_date = festival.get("eventenddate", "종료일 미제공")
                    addr1 = festival.get("addr1", "주소 미제공")
                    addr2 = festival.get("addr2", "주소 미제공")
                    firstimage = festival.get("firstimage", "원본 이미지 미제공")
                    firstimage2 = festival.get("firstimage2", "썸네일 대표 이미지 미제공")
                    areacode = festival.get("areacode", "지역코드 미제공")
                    contentid = festival.get("contentid", "컨텐츠아이디 미제공")

                    refined_festival = {
                        "addr1": addr1,
                        "addr2": addr2,
                        "eventstartdate": start_date,
                        "eventenddate": end_date,
                        "title": title,
                        "firstimage" : firstimage,
                        "firstimage2" : firstimage2,
                        "areacode" : areacode,
                        "contentid" : contentid
                    }
                    refined_festivals.append(refined_festival)    
                return refined_festivals        
            else:
                return {"message": "검색된 항목이 없습니다."}
        else:
            return {"message" : "응답에 축제 정보가 포함되어 있지 않습니다."}
    else:
        return {"message" : "API 요청 실패"}

@router.post("/SearchPage")
async def search_keyword(stdo: SearchDTO):
    BASE_URL = "http://apis.data.go.kr/B551011/KorService1/searchKeyword1"

    params = {
        "numOfRows": stdo.numOfRows,
        "pageNo": stdo.pageNo,
        "MobileOS": "ETC",
        "MobileApp": "AppTest",
        "_type": "json",
        "listYN": "Y",
        "arrange": "A",
        "keyword": stdo.keyword,
        "contentTypeId": 15,
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
                    eventStartDate, eventEndDate = contentID(contentid)  # contentID 함수 호출
                    festival = {
                        "title": item.get('title', '이름 없음'),
                        "address": item.get('addr1', '주소 없음'),
                        "image": item.get('firstimage', '이미지 없음'),
                        "contentid": item.get('contentid', '컨텐츠아이디 없음'),
                        "contenttypeid": item.get('contenttypeid', '컨텐츠타입 없음'),
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
    



def contentID(contentid):
    BASE_URL = "http://apis.data.go.kr/B551011/KorService1/detailIntro1"

    params = {
        "MobileOS": "ETC",
        "MobileApp": "AppTest",
        "_type": "json",
        "contentId": contentid,        # 콘텐츠 ID
        "contentTypeId": 15, # 콘텐츠 타입 ID
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
