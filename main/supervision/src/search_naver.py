# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 14:00:48 2023

@author: kimse
"""

# 네이버 검색 API 예제 - 블로그 검색
import os
import sys
import urllib.request
import json
import re
import pandas as pd
import time


    
def search_naver(query, client_id, client_secret, count):
    title = []
    link = []
    displayLink = []
    
    url = "https://openapi.naver.com/v1/search/webkr?query=" + urllib.parse.quote(query) + "&display=100" # JSON 결과
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    
    for num in range(0, count, 100):
        for start in range(num, num + 100):
            url += '&start=' + str(start)
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
                print('API 요청에 실패했습니다.')
                
    
    return title, link, displayLink
    
    
def extract_domain(url):
    pattern = r"(https?://)?([A-Za-z_0-9.-]+).*"

    # 도메인 이름 추출
    match = re.match(pattern, url)
    domain = match.group(2)
    
    return domain


def gen_xlsx(title, displayLink, link, output):
    search_data = pd.DataFrame({'제목': title, '도메인':displayLink, 'url':link})
    
    if os.path.exists(output):
        df = pd.read_excel(output)
        combined_df = pd.concat([df, search_data], ignore_index=True)
        combined_df.to_excel(output, index=False)
    
    else:
        search_data.to_excel(output, index=False)
    
    
    
