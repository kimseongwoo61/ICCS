# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 22:44:30 2023

@author: kimse
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image, ImageFilter
import os
import urllib
import time
import re
import pandas as pd
from gensim.summarization.summarizer import summarize


def download_html(URL, output_dir):
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(options=options)
    
    # 웹 페이지 로드
    driver.get(URL)  
    time.sleep(5)
    
    
    # 웹 페이지 HTML 가져오기
    html = driver.page_source
    
    # HTML 파일로 저장
    with open(output_dir, "w", encoding="utf-8") as file:
        file.write(html)
    
    # 웹 드라이버 종료
    driver.quit()


def extract_hangul(html_dir):
    with open(html_dir, "r", encoding="utf-8") as file:
        html = file.read()
    
    #한글 추출을 위한 정규표현식 패턴
    pattern = re.compile('[ㄱ-ㅎㅏ-ㅣ가-힣]+')
    
    # HTML에서 한글 추출
    korean_text_list = pattern.findall(html)
    korean_text = '. '.join(korean_text_list)
    
    return korean_text


def check_text(text, keyword_dir):
    check = False
    
    
    # 자살관련 유해 키워드 엑셀파일에서 리스트로 불러온다.
    df = pd.read_excel(keyword_dir, engine = "openpyxl")
    keywords = df["Keyword"].tolist()
    
    
    # textrank의 정보에서 의심 키워드가 있으면
    # 검출 여부와 textrank 정보를 리턴한다.
    summary = summarize(text, ratio=0.5)
    
    for i in keywords:
        if summary.find(i) is not -1:
            check = True
            break
        
    return check, summary
    
    
    

    
    