from django.shortcuts import render
from django.contrib.auth import authenticate, login


# 최초 로그인 화면 렌더링
def login(request):
    return render(request, 'account/account.html')
    
# 회원가입 페이지 렌더링
def join(request):
    return render(request, 'account/join.html')

# 최초 로그인 화면 렌더링
def check(request):
    
    # 만약, get 방식의 요청이면 다시 로그인하도록 한다.
    if request.method == "GET":
        return render(request, 'account/account.html')
    
    elif request.method == "POST":
        username = request.POST["loginId"]
        password = request.POST["loginPw"]
        
        user = authenticate(request, username=username, password=password)
        
        if user is None:
            auth.login(requests, user)
            return redirect('dashboard')
        
        