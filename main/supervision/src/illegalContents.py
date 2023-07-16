from . import google_vision
from . import illegalContents
from . import imageProcessing
from . import htmlProcessing


import os
import re

image_output = os.path.abspath('.').replace('\\','/') + "/supervision/src/image"
token_dir = os.path.abspath('.').replace('\\','/') + "/supervision/src/icm-system-392403-eb6386028156.json"
black_keywords = os.path.abspath('.').replace('\\','/') + "/supervision/src/keywords.xlsx"
html_output = os.path.abspath('.').replace('\\','/') + "/supervision/src/check.html"



def checker(request, url):

    score = []
    imageInfo = []
    
    # 1. 이미지와 같은 시각 자료의 유해성을 확인한다.
    
    # 현재 로그인 되어있는 유저 정보를 확인한다.
    #if request.user.is_authenticated:
    #    token = Token_info.objects.get(user_id = request.user.username)
        
    # url에 접속하여 웹 이미지를 추출한다.
    imageProcessing.extract_images_with_selenium(url, image_output)

    # 구글 토큰 경로와 url 정보를 기반으로 유해성 검사를 진행한다.
    for imageDir in os.listdir(image_output):
        safe = google_vision.detect_safe_search(image_output + "/" + imageDir, token_dir)
        
        
        # 의심항목이 없으면 해당 파일을 삭제한다.
        if safe == False:
            os.remove(image_output + "/" + imageDir)
        
        # 의심항목이 존재한다면 아래 코드를 실행
        else:
            # 이미지의 유해성 검사 점수와 원본 이미지 경로를 저장한다.
            score.append(safe)
            imageInfo.append(image_output + "/" + imageDir)
    
    
    # 유해 시각자료가 존재하면 preview를 위한 블러처리
    if score is not []:
        imageProcessing.image_blur(image_output)
            
    
    
    
    
    # 2. 텍스트를 추출하여 자살유해 키워드 유무를 분석한다.
    
    # 2-1. html 파일을 추출한다.
    htmlProcessing.download_html(url, html_output)
    
    # 2-2. 한글 텍스트를 모두 추출한다.
    extract_text = htmlProcessing.extract_hangul(html_output)
    
    # 2-3. textrank로 요약한 내용에서 블랙리스트 키워드 검출 여부와 요약 정보를 받는다.
    check, summary = htmlProcessing.check_text(extract_text, black_keywords)
    os.remove(html_output)
    
    
    return score, imageInfo, check, summary






def validate_url(url):
    # URL 유효성을 검증하기 위한 정규 표현식 패턴
    pattern = re.compile(r"^(http|https)://")

    # 정규 표현식을 사용하여 URL을 검증
    match = pattern.match(url)

    # URL이 유효한지 여부를 반환
    return bool(match)

        