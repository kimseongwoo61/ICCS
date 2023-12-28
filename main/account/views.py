# 페이지 접속 제한을 위한 모듈
from django.shortcuts import render, redirect

# 토큰 암복호화를 위한 공개키 관련 모듈
from .src import data_encrypt

# 사용자 계정 정보 및 접근 통제를 위한 모듈
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

# DB 정보 접근을 위한 모델 클래스
from .models import Token_info

# 업로드 파일 json 검증 및 ID, Pass 형식 검사
import re
import os
import json

# 동작 로깅용도
import logging
logger = logging.getLogger('django')



# 로그인 계정의 세션종료를 위한 로그아웃 기능
@login_required(login_url='/')
def logout(request):
    logger.info("[*] logout - START")
    auth_logout(request)
    return redirect('/')


# 최초 로그인 화면 렌더링
def login_first(request):
    logger.info("[*] login_first - START")
    
    # 이미 로그인 되어있는 유저는 dashboard로 리다이렉션 진행
    if request.user.is_authenticated:
        return redirect('/dashboard')
    
    return render(request, 'account/account.html')
    

# 회원가입 페이지 렌더링
def join(request):
    logger.info("[*] join - START")
    return render(request, 'account/join.html', {"result" : None})


# 내 정보 조회 페이지
@login_required(login_url='/')
def myinfo(request):
    logger.info("[*] myinfo - START")
    
    user_name = request.user 
    user = User.objects.get(username=user_name)
    
    information = []
    
    try:
        token_info = user.token_info  # 역참조를 통해 Token_info 객체에 접근
        
        # 회원가입 시 생성한 AES키 경로를 설정
        user_name = request.user.username
        aes_key_dir = os.path.join(os.path.abspath('.'), "user_key", user_name, "aes.key")
        
        
        # AES키로 데이터를 복호화 한다.
        information.append(data_encrypt.decrypt_aes(token_info.naver_searchID, aes_key_dir))
        information.append(data_encrypt.decrypt_aes(token_info.naver_searchAPI, aes_key_dir))
        information.append(data_encrypt.decrypt_aes(token_info.google_searchID, aes_key_dir))
        information.append(data_encrypt.decrypt_aes(token_info.google_searchAPI, aes_key_dir))
        information.append(data_encrypt.decrypt_aes(token_info.google_visionID, aes_key_dir))
        information.append(data_encrypt.decrypt_aes(token_info.google_visionAPI, aes_key_dir))
        
        if information[1] != None:
            information[1] = "****"
        if information[3] != None:
            information[3] = "****"
        if information[5] != None:
            information[5] = "****"
        
    # 토큰 정보가 없을 경우 아무 정보가 없다고 표시한다.
    except Token_info.DoesNotExist:
        logger.warning("[?] myinfo - Token_info_DoesNotExist")
        information = None
    
    return render(request, 'supervision/myinfo.html', {'data' : information})


# 최초 로그인 화면 렌더링
def check(request):
    logger.info("[*] check - START")
    
    # 만약, get 방식의 요청이면 다시 로그인하도록 한다.
    if request.method == "GET":
        return redirect("/")
    
    # 정상적인 요청인 경우에는 평문 Id, 해시값 password를 받는다.
    # 이는 DB 유출시 데이터 추측을 불가능 하도록 하기 위함임.
    # 우선 인자들을 모두 받고, 로그인인지 회원가입 행동인지 분별한다.
    elif request.method == "POST":
        login_or_join = request.POST.get('check')
        username = request.POST.get('loginId')
        password = request.POST.get('password')
        email = request.POST.get('user_mail')
        
        # 로그인이라면 인증을 진행하고 대시보드 화면으로 이동할 것
        if login_or_join  == "login":
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect("/dashboard")
            
            else:
                return redirect('/')
        
        
        # 회원가입이면 중복여부를 확인하고 결과를 출력해준다.
        elif login_or_join == "join":
            
            # 우선 수신된 정보들의 형식 유효성을 우선 검사한다.
            if not is_valid_username(username):
                logger.warning("[?] check - 아이디 입력 형식 문제발견")
                return render(request, 'account/join.html', 
                              {'result': False, 'error': '올바른 형식의 ID를 입력해 주세요.'})
            
            if not validate_sha256_hash(password):
                logger.warning("[*] check - 중간 데이터 손실 발견")
                return render(request, 'account/join.html', 
                              {'result': False, 'error': '비밀번호를 다시 입력해 주세요.'})
            
            if not validate_email(email):
                logger.warning("[*] check - 올바르지 않은 이메일 형식")
                return render(request, 'account/join.html', 
                              {'result': False, 'error': '이메일을 다시 입력해 주세요.'})
            
            
            # DB 정보에서 중복되는 정보를 검증한다.
            if User.objects.filter(username=username).exists():
                logger.warning("[*] check - 이미 사용 중인 아이디입니다.")
                return render(request, 'account/join.html', 
                              {'result': False, 'error': '이미 사용 중인 아이디입니다.'})
            
            elif User.objects.filter(email=email).exists():
                logger.warning("[*] check - 이미 사용 중인 이메일입니다.")
                return render(request, 'account/join.html', 
                              {'result': False, 'error': '이미 사용 중인 이메일입니다.'})
            
            else:
                
                # 유저 정보를 DB에 저장한다.
                user = User(username=username, email=email)
                user.set_password(password)
                user.save()
                
                # 토큰 암복호화를 위한 AES 키를 생성한다.
                data_encrypt.generate_aes_key(os.path.join(os.path.abspath('.'), "user_key", username))
                
                logger.info("[*] check - 회원가입 성공하였습니다.")
                return render(request, 'account/join.html', {'result': True})
                
        # 이 경우는 유저가 프록시로 조작하고 있을 가능성이 높음.
        else:
            return redirect('/')
            
            
@login_required(login_url='/')
def change_myinfo(request):
    logger.info("[*] change_myinfo - START")
    
    # 올바른 접근인지 우선 판별한다.
    if request.method == 'POST':
        
        # 유저 정보수정을 위한 입력값 처리
        user_name = request.user 
        user = User.objects.get(username=user_name)
        token_info = Token_info()
        
        
        # 토큰 암호 파일을 업로드 받는다.
        uploaded_file = request.FILES['file']
        upload_file_save_dir = os.path.join(os.path.abspath('.'), "Google_token", request.user.username)
        fs = FileSystemStorage(location= upload_file_save_dir)
        fs.save(os.path.join(upload_file_save_dir, "vision_token.json"), uploaded_file)
        
        # 업로드된 파일 내용이 json인지 검증한다.
        if is_json(os.path.join(upload_file_save_dir, "vision_token.json")):
            with open(os.path.join(upload_file_save_dir, "vision_token.json")) as f:
                google_vision_token = f.read()
                f.close()
            os.remove(os.path.join(upload_file_save_dir, "vision_token.json"))
            
            # 토큰 정보를 입력 받는다.
            naver_search_clientID = request.POST["naver_search_clientID"].strip()
            naver_search_token = request.POST["naver_search_token"].strip()
            google_search_clientID = request.POST["google_search_clientID"].strip()
            google_search_token = request.POST["google_search_token"].strip()
            google_vision_clientID = request.POST["google_vision_clientID"].strip()
            
            
            #  토큰 정보 형식 검사를 진행한다.
            check_items = [naver_search_clientID, 
                           naver_search_token,
                           google_search_clientID,
                           google_search_token,
                           google_vision_clientID]
            
            for item in check_items:
                if not is_valid_token_info(item):
                    logger.warning("[*] change_myinfo - 올바르지 않은 토큰정보 감지")
                    return render(request, 'account/myinfo.html', {'result': "토큰관련 정보를 정확히 입력해 주세요."})
            
            
            # 토큰 정보를 token_info 모델에 저장한다.
            token_info.user_id = user
            
            # 유저이름을 기반으로 AES 암호키 경로를 설정한다.
            user_name = request.user.username
            aes_key_dir = os.path.join(os.path.abspath('.'), "user_key", user_name, "aes.key")
            
            # 회원가입 시 생성한 공개키로 토큰 정보를 모두 암호화하여 저장한다.
            token_info.naver_searchID = data_encrypt.encrypt_aes(naver_search_clientID, aes_key_dir)
            token_info.naver_searchAPI = data_encrypt.encrypt_aes(naver_search_token, aes_key_dir)
            token_info.google_searchID = data_encrypt.encrypt_aes(google_search_clientID, aes_key_dir)
            token_info.google_searchAPI = data_encrypt.encrypt_aes(google_search_token, aes_key_dir)
            token_info.google_visionID = data_encrypt.encrypt_aes(google_vision_clientID, aes_key_dir)
            token_info.google_visionAPI = data_encrypt.encrypt_aes(google_vision_token, aes_key_dir)
            token_info.save()
        
            return render(request, 'account/myinfo.html', {'result': "처리가 완료되었습니다."})
        
        else:
            logger.warning("[*] change_myinfo - 지원하지 않는 파일 업로드 확인.")
            return render(request, 'account/myinfo.html', {'result': "올바른 토큰 파일을 업로드하세요."})
    
    else:
        logger.warning("[*] change_myinfo - 올바르지 않은 접근 감지")
        return render(request, 'account/myinfo.html', {'result': "허용되지 않은 접근입니다."})
    

# view 코드에서 유저의 입력 정보를 검사하기 위한 필터
def is_json(file_path):
    try:
        with open(file_path, 'r') as file:
            json.load(file)
            file.close()
        return True
    
    except json.JSONDecodeError:
        os.remove(file_path)
        return False
    
    
def is_valid_username(username):
    pattern = re.compile(r"^[a-zA-Z0-9_]{4,20}$")
    return bool(pattern.match(username))


def validate_sha256_hash(hash_string):
    # sha256 해시값을 나타내는 정규표현식 패턴
    sha256_pattern = re.compile(r"^[a-fA-F0-9]{64}$")
    
    return bool(sha256_pattern.match(hash_string))


def validate_email(email):
    # 이메일 형식을 나타내는 정규표현식 패턴
    email_pattern = re.compile(r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$")
    
    return bool(email_pattern.match(email))

def is_valid_token_info(token):
    pattern = re.compile(r'^[a-zA-Z0-9_]{1,50}$')
    return pattern.match(token) is not None