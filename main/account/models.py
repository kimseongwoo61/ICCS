from django.db import models
from django.contrib.auth.models import User


# 검색결과 수집 및 유해성 검증 API를 사용하므로 별도 암호화를 진행한다.
class Token_info(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='token_info')
    
    naver_searchID = models.BinaryField(unique=True, default = b'', verbose_name='네이버 검색 client ID')
    naver_searchAPI = models.BinaryField(unique=True, default = b'',  verbose_name='네이버 검색 API 토큰')
    
    google_searchID = models.BinaryField(unique=True, default = b'', verbose_name='구글 검색 client ID')
    google_searchAPI = models.BinaryField(unique=True, default = b'', verbose_name='구글 검색 API 토큰')
    
    google_visionID = models.BinaryField(unique=True, default = b'', verbose_name='구글 비전 clinet ID')
    google_visionAPI = models.BinaryField(unique=True, default = b'', verbose_name='구글 비전 API 토큰 암호정보')
    
    class Meta:
        db_table = 'token'
        

# 단순 관리자에게 문의글을 남기는 목적이므로 별도 암호화하지 않는다
class QnA(models.Model):
    user_id = models.CharField(unique=False, default = '', max_length=100, verbose_name='아이디')
    title = models.CharField(unique=False, default = '', max_length=100, verbose_name='제목')
    contents = models.CharField(unique=False, default = '', max_length=1000, verbose_name='문의 내용')
    date = models.DateField(auto_now_add=True)
    
    name = models.CharField(unique=False, default = '', max_length=100, verbose_name='이름')
    phone_number = models.CharField(unique=False, default = '', max_length=100, verbose_name='전화번호')

    
    class Meta:
        db_table = 'qna'
        
        
    

    