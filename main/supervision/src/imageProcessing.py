# -*- coding: utf-8 -*-

from . import htmlProcessing
from screeninfo import get_monitors 
from PIL import Image, ImageFilter

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

import os
import time
import urllib
import subprocess

# 동작 로깅용도
import logging
logger = logging.getLogger('django')


# 웹 콘텐츠 검증 시, 페이지 경고문 팝업을 위해 사용
message = "유해 콘텐츠 검사 진행중 입니다."
message += "\\n화면을 닫지 마세요."
message += "\\n- ICMS running -"

dark_layer_script = f"""
var darkLayer = document.createElement('div');
darkLayer.style.position = 'fixed';
darkLayer.style.top = '0';
darkLayer.style.left = '0';
darkLayer.style.width = '100%';
darkLayer.style.height = '100%';
darkLayer.style.backgroundColor = 'rgba(0, 0, 0, 1)';
document.body.appendChild(darkLayer);

var textElement = document.createElement('div');
textElement.style.position = 'fixed';
textElement.style.top = '50%';
textElement.style.left = '50%';
textElement.style.transform = 'translate(-50%, -50%)';
textElement.style.fontSize = '15px';
textElement.style.color = 'white';
textElement.style.textAlign = 'center';
textElement.innerText = "{message}";
document.body.appendChild(textElement);
"""

# 크롬이 설치되지 않았을 경우 발생되는 예외 정의
class ChromeNotInstalledException(Exception):
    pass


# 웹 페이지로 부터 이미지 파일을 모두 추출한다.
# input : 추출할 웹 주소(+http), 데이터 저장경로
# output : 저장 경로에 이미지 파일이 저장됨 
def extract_images_and_html(url, output_directory, html_save_dir, index):
    logger.info("[*] extract_images_and_html - START")
    
    try:
        # 크롬 실행파일, 프로필 경로를 탐색한다.
        chrome_dir = find_chrome_executable_windows()
        profile_dir = find_chrome_profile()
        
        # 크롬이 설치되어 있지 않으면         
        if chrome_dir != None:
            # 크롬 제어를 위한 설정진행
            chrome = subprocess.Popen(f'{chrome_dir} --remote-debugging-port=9223 --user-data-dir="{profile_dir}"')
            service = Service(executable_path=r'./supervision/src')
            option = Options()
            option.add_experimental_option("debuggerAddress", "127.0.0.1:9223")
            driver = webdriver.Chrome(service=service, options=option)
            
            # 크롬창 위치를 설정한다.
            monitors = get_monitors()
            if monitors:
                first_monitor = monitors[0]
            
            driver.set_window_position(first_monitor.width - 1000, first_monitor.height - 600)
            driver.set_window_size(600, 400)
            
            # 웹페이지 로드 및 화면을 block 처리한다.
            driver.execute_script(dark_layer_script)
            driver.get(url)
            driver.execute_script(dark_layer_script)
            time.sleep(5)
            
            # 이미지 태그 추출
            img_elements = driver.find_elements(By.TAG_NAME, 'img')
            
            # 이미지 파일 추출 및 저장
            counter = 0
            for img_element in img_elements:
                # 이미지 URL 가져오기
                img_url = img_element.get_attribute('src')
        
                try:
                    # 이미지 다운로드
                    img_filename = str(index) + "_check-" + str(counter)
                    img_path = output_directory + "/" + img_filename + ".jpg"
                    urllib.request.urlretrieve(img_url, img_path)
                    logger.info(f'[*] Saved image: {img_filename}')
                    counter += 1
                    
        
                except Exception as e:
                    logger.warning(f'[!] extract_images_and_html - ERROR : {img_url} {str(e)}')
            
            
            
            try:
                htmlProcessing.download_html(html_save_dir, chrome, driver)
                logger.info("[*] extract_images_and_html - FINISH")
                driver.quit()
                chrome.kill()
                
            except Exception as e:
                logger.warning("[!] extract_images_and_html - ERROR : " + str(e))
                driver.quit()
                chrome.kill()
            
            
            
        else:
            # 웹드라이버 종료
            raise ChromeNotInstalledException("크롬이 설치되어 있지 않습니다!!!")
    
    except Exception as e:
        logger.warning("[!] extract_images_and_html - ERROR : " + str(e))
        driver.quit()
        chrome.kill()
        


# 이미지 파일들의 해상도를 낮춘 흐린 사진을 생성한다.
# input : 흐림 처리할 파일들의 경로
# output : 흐림 처리된 이미지 파일(blur_....jpg)
def image_blur(image_directory):
    logger.info("[*] image_blur - START")
    
    for image in os.listdir(image_directory):
        
        try:
            #이미지 불러오기
            image1 = Image.open(os.path.join(image_directory, image))
             
            #BoxBlur를 통한 이미지 흐림 처리
            blurI = image1.filter(ImageFilter.BoxBlur(12))
            blurI.save(os.path.join(image_directory, "blur_" + image))
            logger.info("[*] image_blur - FINISH")
        
        except Exception as e:
            logger.warning("[*] image_blur - ERROR : " + str(e))


# 크롬 브라우저 실행파일 경로를 탐색한다.
# input : None
# return : 크롬 브라우저 실행파일 경로
def find_chrome_executable_windows():
    logger.info("[*] find_chrome_executable_windows - START")
    
    try:
        import winreg
    except ImportError:
        import _winreg as winreg


    reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe"
    
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
            chrome_path = winreg.QueryValue(key, None)
            logger.info("[*] find_chrome_executable_windows - FINISH")
        
        return chrome_path
    
    
    except FileNotFoundError as e:
        logger.warning("[!] find_chrome_executable_windows - ERROR : " + str(e))
        return None


# 크롬 브라우저 제어를 위한 유저데이터 경로를 탐색한다.
# input : None
# return : 크롬 브라우저 실행파일 경로
def find_chrome_profile():
    logger.info("[*] find_chrome_profile - START")
    
    appdata_path = os.getenv("LOCALAPPDATA")  # 사용자의 AppData 디렉토리 경로를 가져옵니다.
    
    # 기본 default 프로파일 경로를 지정합니다.
    default_profile_path = os.path.join(appdata_path, "Google", "Chrome", "User Data", "Default")
    
    # 프로파일 디렉토리가 존재하면 해당 경로를 반환합니다.
    if os.path.exists(default_profile_path):
        logger.info("[*] find_chrome_profile - FINISH")
        return default_profile_path
    
    # 다른 프로파일 파일이 존재하는지 확인하고, 있으면 해당 경로를 반환합니다.
    other_profiles = ["Profile 1", "Profile 2"]  # 원하는 다른 프로파일 이름들을 추가합니다.
    for profile_name in other_profiles:
        profile_path = os.path.join(appdata_path, "Google", "Chrome", "User Data", profile_name)
        if os.path.exists(profile_path):
            logger.info("[*] find_chrome_profile - FINISH")
            return profile_path
    
    # 위의 경우에 해당하지 않으면 새로운 프로파일 디렉토리를 생성하고 경로를 반환합니다.
    new_profile_path = os.path.join(appdata_path, "Google", "Chrome", "User Data", "NewProfile")
    os.makedirs(new_profile_path, exist_ok=True)
    logger.info("[*] find_chrome_profile - FINISH")
    return new_profile_path
