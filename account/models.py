from django.db import models
from django.contrib.auth.models import User


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
        
        
    

    