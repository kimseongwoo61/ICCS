# -*- coding: utf-8 -*-

# 네이버 검색 API 예제 - 블로그 검색
import os
import urllib.request
import json
import re
import pandas as pd
import time

# 동작 로깅용도
import logging
logger = logging.getLogger('django')


    
def search_naver(query, client_id, client_secret, count):
    logger.info("[*] search_naver - START")
    
    title = []
    link = []
    displayLink = []
    
    url = "https://openapi.naver.com/v1/search/webkr?query=" + urllib.parse.quote(query) + "&display=10" # JSON 결과
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    
    q = count // 10
    r = count % 10
    
    if count < 10:
        url += '&start=0'
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        
        if rescode == 200:
            response_body = response.read()
            json_data = json.loads(response_body.decode('utf-8'))
            time.sleep(1)
            for index in json_data['items']:
                link.append(index['link'])
                displayLink.append(extract_domain(index['link']))
                title.append(index['title'])
                
        else:
            logger.info("[*] search_naver - ERROR : API 요청에 실패했습니다.")
    
    else:
        if r != 0:
            q += 1
        
        for num in range(0, q):
            url += '&start=' + str(num * 10)
            response = urllib.request.urlopen(request)
            rescode = response.getcode()

            if rescode == 200:
                response_body = response.read()
                json_data = json.loads(response_body.decode('utf-8'))
                time.sleep(1)
                for index in json_data['items']:
                    link.append(index['link'])
                    displayLink.append(extract_domain(index['link']))
                    title.append(index['title'])
                    
            else:
                logger.info("[*] search_naver - ERROR : API 요청에 실패했습니다.")
    
    logger.info("[*] search_naver - FINISH")
    return title, link, displayLink
    
    
def extract_domain(url):
    logger.info("[*] extract_domain - START")
    
    pattern = r"(https?://)?([A-Za-z_0-9.-]+).*"

    # 도메인 이름 추출
    match = re.match(pattern, url)
    domain = match.group(2)
    
    logger.info("[*] extract_domain - FINISH")
    return domain


def gen_xlsx(title, displayLink, link, output):
    logger.info("[*] gen_xlsx - START")
    search_data = pd.DataFrame({'제목': title, '도메인':displayLink, 'url':link})
    
    if os.path.exists(output):
        df = pd.read_excel(output)
        combined_df = pd.concat([df, search_data], ignore_index=True)
        combined_df.to_excel(output, index=False)
        logger.info("[*] gen_xlsx - FINISH")
    
    else:
        search_data.to_excel(output, index=False)
        logger.info("[*] gen_xlsx - FINISH")
    
    
    
