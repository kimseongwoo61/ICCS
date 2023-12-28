# 
from google.cloud import vision

# 동작 로깅용도
import logging
logger = logging.getLogger('django')

# 이미지의 유해성 여부를 판별한다.
# input : 검사할 이미지의 경로, 구글 비전 API 사용을 위한 토큰 파일경로
# output : 유해 의심 항목이 없으면 False, 있으면 검사 결과 safe 정보
def detect_safe_search(imageDir, jsonToken_dir):
    logger.info("[*] detect_safe_search - START")
    
    # 구글 비전 API를 사용하기 위한 토큰 인증진행
    client = vision.ImageAnnotatorClient.from_service_account_json(jsonToken_dir)
    
    # 유해성을 검사할 이미지 파일 처리진행
    with open(imageDir, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    # API 요청 진행
    response = client.safe_search_detection(image=image)
    
    if response.error.message:
        logger.warning("[!] detect_safe_search - ERROR : " + response.error.message)
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

    # 응답 결과를 리스트로 변환
    safe = response.safe_search_annotation
    
    safe_search_result = [
        safe.adult,
        safe.medical,
        safe.spoof,
        safe.violence,
        safe.racy
    ]
    
    # 유해성 검사결과, 하나라도 의심항목이 있으면 유해성 점수 측정
    for score in safe_search_result:
        if score >= 3:
            logger.info("[*] detect_safe_search - FINISH")
            return safe
    
    else:
        logger.info("[*] detect_safe_search - FINISH")
        return False