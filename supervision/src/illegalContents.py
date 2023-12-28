# -*- coding: utf-8 -*-

from . import google_vision
from . import imageProcessing
from . import htmlProcessing
from . import whois_info
from . import data_encrypt
from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import os
import shutil

# 동작 로깅용도
import logging
logger = logging.getLogger('django')

black_keywords = os.path.join(os.path.abspath('.'), "supervision", "src", "keywords.xlsx")
base_dir = os.path.join(os.path.abspath('.'), "supervision", "src", "user")


# 웹 페이지의 텍스트, 이미지 정보를 분석하여 유해성 검사 결과를 반환한다.
# return 항목 : title, url, domain, 블랙리스트 키워드 검출여부, 유해 이미지, 이미지 평가정보, 콘텐츠 요약
def checker(request, url, crawler, index):
    logger.info("[*] checker - START")
    
    image_dirInfo = []
    score_illegal = []
    summary = None
    
    if not request.user.is_authenticated:
        return 
    
    # 먼저 로그인된 유저 ID 이름의 폴더를 만들어 작업 공간을 분리한다.
    # - check : 검증 데이터가 임시로 저장되는 공간
    # - result : 최종 탐색 보고서가 저장되는 공간
    #   - image : 엑셀 보고서에 참조될 유해 이미지 파일 저장공간
    
    # 유저 공간의 모든 데이터를 삭제한다.
    user_directory = os.path.join(base_dir, request.user.username)
    
    if crawler == 0:
        if(os.path.exists(user_directory)):
            try:
                shutil.rmtree(user_directory)
                os.mkdir(user_directory)
                os.mkdir(os.path.join(user_directory, "check"))
                os.mkdir(os.path.join(user_directory, "result"))
                os.mkdir(os.path.join(user_directory, "result", "image"))
            
            except Exception as e:
                logger.warning("[!] checker - ERROR : " + str(e))
        
        else:
            os.mkdir(user_directory)
    
    
    # 유해 콘텐츠 유무를 판별한다.
    
    # User 모델과 One-to-One 관계인 Token_info 모델
    user = User.objects.get(username=request.user.username)
    
    # 역참조를 통해 Token_info 객체에 접근
    # 구글 비전 api 토큰 파일 이름을 불러옴
    token_info = user.token_info 
    
    # 웹 페이지에서 추출한 이미지 저장 경로
    image_save_dir = os.path.join(user_directory, "check")
    
    # 회원가입 시 생성한 개인키 생성 경로를 설정
    user_name = request.user.username
    aes_key_dir = os.path.join(os.path.abspath('.'), "user_key", user_name, "aes.key")
    
    # 구글 비전 토큰 경로
    vision_token_dir = os.path.join(user_directory, "temp_token")
    with open(vision_token_dir, "w") as f:
        plain_data  = data_encrypt.decrypt_aes(token_info.google_visionAPI, aes_key_dir)
        f.write(plain_data)
        f.close()
    
    
    # 1. 이미지, html 파일추출을 진행한다.
    # url에 접속하여 웹 이미지와 html를 추출한다.
    html_save_dir = os.path.join(image_save_dir, "need_check.html")
    
    try:
        imageProcessing.extract_images_and_html(url, image_save_dir, html_save_dir, index)
    
    except imageProcessing.ChromeNotInstalledException as e:
        logger.critical("[!] checker - CRITICAL ERROR : " + str(e))
        raise Exception("크롬이 설치되어있지 않습니다!!!")

    # 추출된 이미지들의 유해성을 검사한다.
    for imageDir in os.listdir(image_save_dir):
        logger.info("이미지 검증 - " + str(imageDir))

        try:
            if imageDir == "need_check.html":
                continue
            
            safe = google_vision.detect_safe_search(os.path.join(image_save_dir, imageDir), vision_token_dir)
            
            # 의심항목이 없으면 해당 파일을 삭제한다.
            if safe == False:
                os.remove(os.path.join(image_save_dir, imageDir))
            
            
            # 의심항목이 존재한다면 유해 결과 및 이미지 경로를 저장한다.
            else:
                score_illegal.append(safe)
                image_dirInfo.append(os.path.join(image_save_dir, imageDir))
        
        
        # 만약 구글 비전에서 지원하지 않는 확장자거나 오류가 발생한다면 파일을 삭제.
        except Exception as e:
            logger.warning("[!] checker - ERROR : " + str(e))
            
            try:
                os.remove(os.path.join(image_save_dir, imageDir))
                
            except Exception as e:
                logger.warning("[!] checker - ERROR : " + str(e))

    os.remove(vision_token_dir)
    
    
    # 2. 텍스트에서 자살유해 키워드 유무를 분석한다.
    
    # url에서 도메인을 추출한다.
    domain = htmlProcessing.extract_domain(url)
    
    # html 파일에서 페이지 제목을 추출한다.
    title = htmlProcessing.get_page_title(html_save_dir)
    if title == None:
        title = "None"
    
    # 한글 텍스트를 모두 추출한다.
    extract_text = htmlProcessing.extract_hangul(html_save_dir)
    
    # textrank로 요약한 내용에서 블랙리스트 키워드 검출 여부와 요약 정보를 받는다.
    check_blackList, summary = htmlProcessing.check_text(extract_text, black_keywords)
    
    # 검사가 끝난 html 파일은 삭제한다.
    os.remove(html_save_dir)
    
    whois_reports = whois_info.get(url)
    
    return title, url, domain, check_blackList, image_dirInfo, score_illegal, summary, whois_reports



# URL 주소가 정확한 형식인지 판별하는 기능
# input : 유저 입력값
# return : URL 형식 판별(bool)
def validate_url(url):
    logger.info("[*] validate_url - START")
    
    # URL 유효성을 검증하기 위한 정규 표현식 패턴
    url_validator = URLValidator()

    # 정규 표현식을 사용하여 URL을 검증
    try:
        url_validator(url)
        logger.info("[*] validate_url - FINISH")
        return True
    
    # URL이 유효한지 여부를 반환
    except ValidationError as e:
        logger.warning("[!] validate_url - ERROR : " + str(e))
        return False

        