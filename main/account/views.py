from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth import logout as auth_logout
from account.models import Token_info
from django.contrib.auth.models import User


# 최초 로그인 화면 렌더링
def login_first(request):
    # 이미 로그인 되어있는 유저는 dashboard로 리다이렉션 진행
    if request.user.is_authenticated:
        return redirect('/dashboard')
    
    return render(request, 'account/account.html')
    
# 회원가입 페이지 렌더링
def join(request):
    return render(request, 'account/join.html')

# 내 정보 조회 페이지
def myinfo(request):
    if not request.user.is_authenticated:
        return redirect('/')
    
    
    user_name = request.user 
    user = User.objects.get(username=user_name)
    information = []
    
    
    try:
        token_info = user.token_info  # 역참조를 통해 Token_info 객체에 접근
        information.append(token_info.naver_searchID)
        information.append(token_info.naver_searchAPI)
        information.append(token_info.naver_keywordID)
        information.append(token_info.naver_keywordAPI)
        information.append(token_info.google_visionID)
        information.append(token_info.google_visionAPI)
    
    except Token_info.DoesNotExist:
        information = None
    
    
    
    return render(request, 'supervision/myinfo.html', {'data' : information})


# 최초 로그인 화면 렌더링
def check(request):
    
    # 만약, get 방식의 요청이면 다시 로그인하도록 한다.
    if request.method == "GET":
        return render(request, 'account/account.html')
    
    
    # 정상적인 요청인 경우에는 평문 Id, 해시값 password를 받는다.
    # 이는 DB 유출시 데이터 추측을 불가능 하도록 하기 위함임.
    elif request.method == "POST":
        
        username = request.POST.get('loginId')
        password = request.POST.get('password')

        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("/dashboard")
        
        else:
            return redirect('/')
        

def logout(request):
    auth_logout(request)
    return redirect('/')
    
        