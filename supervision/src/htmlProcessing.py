# -*- coding: utf-8 -*-

from gensim.summarization.summarizer import summarize
from bs4 import BeautifulSoup
import pandas as pd
import re

# 동작 로깅용도
import logging
logger = logging.getLogger('django')



# 크롬 드라이버를 기반으로 html 파일을 추출한다.
# input : html 파일 저장경로, 크롬 프로세스, 크롬 드라이버
# return : 추출된 html 파일
def download_html(output_dir, chrome, driver):  
    logger.info("[*] download_html - START")
    
    try:
        # 웹 페이지 HTML 가져오기
        html = driver.page_source
        
        # HTML 파일로 저장
        with open(output_dir, "w", encoding="utf-8") as file:
            file.write(html)
        
    
    except Exception as e:
        chrome.kill()
        logger.warning("[!] download_html - ERROR : " + str(e))
    
    logger.info("[*] download_html - FINISH")



# html 파일에서 한글 텍스트를 모두 추출한다.
# input : html 파일 경로
# return : 추출된 한글 텍스트
def extract_hangul(html_dir):
    logger.info("[*] extract_hangul - START")
    
    with open(html_dir, "r", encoding="utf-8") as file:
        html = file.read()
    
    #한글 및 공백 추출을 위한 정규표현식 패턴
    pattern = re.compile('[ㄱ-ㅎㅏ-ㅣ가-힣]+')
    
    # HTML에서 한글 추출
    korean_text_list = pattern.findall(html)
    korean_text = '. '.join(korean_text_list)
    
    logger.info("[*] extract_hangul - FINISH")
    return korean_text



# 한글 텍스트에서 블랙리스트 키워드 포함 여부를 검증한다.
# input : 검증 필요 한글 텍스트, 블랙리스트 키워드 경로
# return : 블랙리스트 키워드 포함 여부(bool)
def check_text(text, keyword_dir):
    logger.info("[*] check_text - START")
    
    check = False
    # 자살관련 유해 키워드 엑셀파일에서 리스트로 불러온다.
    df = pd.read_excel(keyword_dir, engine = "openpyxl")
    
    keywords = df["Keyword"].tolist()
    
    
    # textrank의 정보에서 의심 키워드가 있으면
    # 검출 여부와 textrank 정보를 리턴한다.
    try:
        summary = summarize(text, ratio=0.2)
        
    except Exception as e:
        summary = text
        logger.warning("[!] check_text - ERROR : " + str(e))
    
    
    for i in keywords:
        if text.find(i) != -1:
            check = True
            break
        
    logger.info("[*] check_text - FINISH")
    return check, summary
    


# html 파일에서 제목 정보를 추출한다.
# input : html 파일 경로
# return : title 정보
def get_page_title(html_dir):
    logger.info("[*] get_page_title - START")
    
    # 응답의 HTML 내용을 파싱
    with open(html_dir, 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()
        soup = BeautifulSoup(html_content, 'html.parser')
    
    # 페이지 제목 추출
    page_title = soup.title.text if soup.title else None
    
    logger.info("[*] get_page_title - START")
    return page_title



# URL 정보에서 도메인 주소 정보를 추출한다.
# input : URL 전체 주소
# return : 도메인 주소
def extract_domain(url):
    logger.info("[*] extract_domain - START")
    pattern = r"(https?://)?([A-Za-z_0-9.-]+).*"

    # 도메인 이름 추출
    match = re.match(pattern, url)
    domain = match.group(2)
    
    logger.info("[*] extract_domain - FINISH")
    return domain
    
    

    
    