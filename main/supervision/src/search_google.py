<<<<<<< HEAD
# -*- coding: utf-8 -*-

import requests
import json
import pandas as pd
import os

# 동작 로깅용도
import logging
logger = logging.getLogger('django')


def search_google(query, search_engine_id, api_key, count):
    logger.info("[*] search_google - START")
    
    url = 'https://www.googleapis.com/customsearch/v1?key=' + api_key + '&cx=' + search_engine_id + '&q=' + query + "&num=5"
    title = []
    displayLink = []
    link = []
    
    q = count // 10
    r = count % 10
    
    if count < 10:
        url += '&start=0'
        response = requests.get(url)
        
        if response.status_code == 200:
            json_data = json.loads(response.text)

            for index in json_data['items']:
                link.append(index['link'])
                displayLink.append(index['displayLink'])
                title.append(index['title'])
                
        else:
            logger.warning("[*] search_google - ERROR : API 요청에 실패했습니다.")
            logger.warning(response.text)
    
    else:
        if r != 0:
            q += 1
            
        for num in range(0, q):
            url += '&start=' + str(num * 10)
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                json_data = json.loads(response.text)

                for index in json_data['items']:
                    link.append(index['link'])
                    displayLink.append(index['displayLink'])
                    title.append(index['title'])
                    
            else:
                logger.warning("[*] search_google - ERROR : API 요청에 실패했습니다.")
                logger.warning(response.text)
    
    logger.info("[*] search_google - FINISH")
    return title, displayLink, link 


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
    


=======
import requests
import json
import pandas as pd
import os


def search_google(query, search_engine_id, api_key, count):
    url = 'https://www.googleapis.com/customsearch/v1?key=' + api_key + '&cx=' + search_engine_id + '&q=' + query + "&num=10"
    
    
    title = []
    displayLink = []
    link = []
    
    
    for num in range(0, count, 10):
        for start in range(num, num + 10):
            url += '&start=' + str(start)
            response = requests.get(url)
            
            if response.status_code == 200:
                json_data = json.loads(response.text)

                for index in json_data['items']:
                    link.append(index['link'])
                    displayLink.append(index['displayLink'])
                    title.append(index['title'])
                    
            else:
                print('API 요청에 실패했습니다.')
                print(response.text)
    
    return title, displayLink, link 


def gen_xlsx(title, displayLink, link, output):
    search_data = pd.DataFrame({'제목': title, '도메인':displayLink, 'url':link})
    
    if os.path.exists(output):
        df = pd.read_excel(output)
        combined_df = pd.concat([df, search_data], ignore_index=True)
        combined_df.to_excel(output, index=False)
    
    else:
        search_data.to_excel(output, index=False)
    


>>>>>>> 719cd225de0c04018c059ed171d0c81cd36fa789
