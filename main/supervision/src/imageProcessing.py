from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image, ImageFilter
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import subprocess
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import os
import urllib
import time
import signal
import psutil

def kill_processes_by_name(process_name):
    for process in psutil.process_iter(['name']):
        if process.info['name'] == process_name:
            process.kill()


# 웹 페이지로 부터 이미지 파일을 모두 추출한다.
# input : 추출할 웹 주소(+http), 데이터 저장경로
# output : 저장 경로에 이미지 파일이 저장됨 
def extract_images_with_selenium(url, output_directory):

    
    # 웹드라이버 설정
    chrome = subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9223 --user-data-dir="C:\Users\kimse\AppData\Local\Google\Chrome\User Data\Default"')
    try:
        option = Options()
        option.add_experimental_option("debuggerAddress", "127.0.0.1:9223")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
        driver.minimize_window()
        
        
        # 웹페이지 로드
        driver.get(url)
        
        
        # 일반적으로 대다수 SNS는 동적 웹페이지가 많기 때문에 로딩을 위해서 인위적으로 지연코드 삽입
        time.sleep(5)
        
        
        # 이미지 태그 추출
        img_elements = driver.find_elements(By.TAG_NAME, 'img')
    
        # 이미지 파일 추출 및 저장
        for img_element in img_elements:
            
            # 이미지 URL 가져오기
            img_url = img_element.get_attribute('src')
    
            try:
                # 이미지 다운로드
                img_filename = os.path.basename(urllib.parse.urlsplit(img_url).path)
                img_path = output_directory + "/" + img_filename + ".jpg"
                print(img_path)
                urllib.request.urlretrieve(img_url, img_path)
    
                print(f'Saved image: {img_filename}')
                
    
            except Exception as e:
                print(f'Error occurred while downloading image from {img_url}: {str(e)}')
                
    
        # 웹드라이버 종료
        driver.quit()
        chrome.kill()
    
    
    except Exception as e:
        chrome.kill()
        print("imageProcessing extract_images_with_selenium --------- Error : " + str(e))



# 이미지 파일들의 해상도를 낮춘 흐린 사진을 생성한다.
# input : 흐림 처리할 파일들의 경로
# output : 흐림 처리된 이미지 파일(blur_....jpg)
def image_blur(image_directory):
    
    for image in os.listdir(image_directory):
        
        try:
            #이미지 불러오기
            image1 = Image.open(image_directory + "/" + image)
             
            #BoxBlur를 통한 이미지 흐림 처리
            blurI = image1.filter(ImageFilter.BoxBlur(12))
            blurI.save(image_directory + "/blur_" + image)
        
        except Exception as e:
            print("error : " + str(e))



if __name__ == "__main__":
    # 테스트를 위해 사용할 URL과 이미지를 저장할 디렉토리 설정
    url = 'https://twitter.com/Kitty_gidi/status/1678280695347806209'  # 웹페이지 URL
    output_directory = 'C:/Users/kimse/OneDrive/바탕 화면/소개딩/테스트/main/supervision/src/image'  # 이미지 저장 디렉토리
    
    
    # 이미지 추출 실행
    extract_images_with_selenium(url, output_directory)
    image_blur(output_directory)
