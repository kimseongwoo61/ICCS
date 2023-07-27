from . import google_vision
from . import illegalContents
from . import imageProcessing
from . import htmlProcessing
from account.models import Token_info
from django.contrib.auth.models import User
import os
import re
import shutil

black_keywords = os.path.abspath('.').replace('\\','/') + "/supervision/src/keywords.xlsx"
base_dir = os.path.abspath('.').replace('\\','/') + "/supervision/src/user/"




# 웹 페이지의 텍스트, 이미지 정보를 분석하여 유해성 검사 결과를 반환한다.
# return 항목 : title, url, domain, 블랙리스트 키워드 검출여부, 유해 이미지, 이미지 평가정보, 콘텐츠 요약
def checker(request, url, crawler):
    image_dirInfo = []
    score_illegal = []
    summary = None
    
    if not request.user.is_authenticated:
        return 
    
    
    print("illegalContents checker --------- start")

    
    # 먼저 로그인된 유저 ID 이름의 폴더를 만들어 작업 공간을 분리한다.
    # check : 검증 데이터가 임시로 저장되는 공간
    # result : 최종 탐색 보고서가 저장되는 공간
    # result -> image : 엑셀 보고서에 참조될 유해 이미지 파일 저장공간
    
    
    # 우선 작업하기 전에, 유저 공간의 모든 데이터를 삭제한다.
    if crawler == 0:
        if(os.path.exists(base_dir + request.user.username)):
            try:
                shutil.rmtree(base_dir + request.user.username)
                os.mkdir(base_dir + request.user.username)
                os.mkdir(base_dir + request.user.username + "/check")
                os.mkdir(base_dir + request.user.username + "/result")
                os.mkdir(base_dir + request.user.username + "/result/image")
            
            except Exception as e:
                print("illegalContents checker --------- Error " + str(e))
        
        else:
            os.mkdir(base_dir + request.user.username)
    
    
    # 유해 콘텐츠 유무를 판별한다.
    
    
    
    # 1. 이미지와 같은 시각 자료의 유해성을 확인한다.
    
    # User 모델과 One-to-One 관계인 Token_info 모델
    user = User.objects.get(username=request.user.username)
    
    # 역참조를 통해 Token_info 객체에 접근
    # 구글 비전 api 토큰 파일 이름을 불러옴
    token_info = user.token_info 
    
    # 웹 페이지에서 추출한 이미지 저장 경로
    image_save_dir = base_dir + request.user.username + "/check"
    
    # 구글 비전 토큰 경로
    vision_token_dir = base_dir + request.user.username + "/temp_token"
    with open(vision_token_dir, "w") as f:
        f.write(token_info.google_visionAPI)
        f.close()
    
    
    # url에 접속하여 웹 이미지를 추출한다.
    imageProcessing.extract_images_with_selenium(url, image_save_dir)

    # 추출된 이미지들의 유해성을 검사한다.
    for imageDir in os.listdir(image_save_dir):
        print("이미지 검증 - " + str(imageDir))
        try:
            safe = google_vision.detect_safe_search(image_save_dir + "/" + imageDir, vision_token_dir)
            
            # 의심항목이 없으면 해당 파일을 삭제한다.
            if safe == False:
                os.remove(image_save_dir + "/" + imageDir)
            
            
            # 의심항목이 존재한다면 유해 결과 및 이미지 경로를 저장한다.
            else:
                score_illegal.append(safe)
                image_dirInfo.append(image_save_dir + "/" + imageDir)
        
        
        # 만약 구글 비전에서 지원하지 않는 확장자거나 오류가 발생한다면 파일을 삭제.
        except Exception as e:
            print("illegalContents checker --------- Error1 " + str(e))
            try:
                os.remove(image_save_dir + "/" + imageDir)
            except Exception as e:
                print("illegalContents checker --------- Error2 " + str(e))
    os.remove(vision_token_dir)
    
    
    # 2. 텍스트를 추출하여 자살유해 키워드 유무를 분석한다.
    html_save_dir = base_dir + request.user.username + "/check/need_check.html"
    
    # url에서 도메인을 추출한다.
    domain = htmlProcessing.extract_domain(url)
    
    # html 파일을 추출한다.
    htmlProcessing.download_html(url, html_save_dir)
    
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
    
    
    return title, url, domain, check_blackList, image_dirInfo, score_illegal, summary



def validate_url(url):
    # URL 유효성을 검증하기 위한 정규 표현식 패턴
    pattern = re.compile(r"^(http|https)://")

    # 정규 표현식을 사용하여 URL을 검증
    match = pattern.match(url)

    # URL이 유효한지 여부를 반환
    return bool(match)

        