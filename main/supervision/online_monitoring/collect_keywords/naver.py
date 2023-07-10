# -*- coding: utf-8 -*-

import os
import sys
import urllib.request
import json
import pandas as pd
import matplotlib.pyplot as plt
import time
import random
import requests
import hashlib
import hmac
import base64




# 기능 : 연관검색어 수집을 위한 검색 시그니처 생성
# 인자 : timestamp, method, uri, secret_key
# 리턴 값 :
#        - base64.b64encode(hash.digest())
class Signature:

    @staticmethod
    def generate(timestamp, method, uri, secret_key):
        message = "{}.{}.{}".format(timestamp, method, uri)
        hash = hmac.new(bytes(secret_key, "utf-8"), bytes(message, "utf-8"), hashlib.sha256)
        hash.hexdigest()
        return base64.b64encode(hash.digest())
    

def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = Signature.generate(timestamp, method, uri, secret_key)
    
    return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 
            'X-API-KEY': api_key, 'X-Customer': str(customer_id), 'X-Signature': signature}


def getresults(hintKeywords):

    BASE_URL = 'https://api.naver.com'
    API_KEY = '010000000023b1daea2c725b0527626e9e42a01b2ce3360f69c673029cef8822a4df7984cc'
    SECRET_KEY = 'AQAAAAAjsdrqLHJbBSdibp5CoBssEum+XXFfgrIWsretdQnlZQ=='
    CUSTOMER_ID = '2656966'

    uri = '/keywordstool'
    method = 'GET'

    params={}

    params['hintKeywords']=hintKeywords
    params['showDetail']='1'

    r=requests.get(BASE_URL + uri, params=params, 
                 headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

    return pd.DataFrame(r.json()['keywordList']).iloc[0:,[0]]


def collect(fileDir, saveDir):
    excel = pd.read_excel(fileDir)  # base.xlsx
    base_keywords = excel["Keyword"]
    
    total = pd.DataFrame()
    
    for keyword in base_keywords:
        try:
            temp = getresults(keyword)
            total = pd.concat([total, temp], ignore_index=True)
        
        except Exception as e:
            continue
    
    with pd.ExcelWriter(saveDir, mode='w', engine='openpyxl') as writer:
        total.to_excel(writer, sheet_name="Keyword", index=False, header=["Keyword"])
        
        
    return total



if __name__ == '__main__':
    # 연관 검색어를 추출할 기본(base) 키워드 리스트 파일경로
    base_list  = os.getcwd() + "\\..\\input_data\\base.xlsx"

    # 수집한 연관 검색어를 저장할 파일경로
    new_list   = os.getcwd() + "\\..\\daily_reports\\naver.xlsx"
    
    print(base_list)
    print(collect(base_list, new_list))