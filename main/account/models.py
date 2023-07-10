from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.CharField(max_length=32, unique=True, verbose_name='사용자 아이디')
    user_pw = models.CharField(max_length=128, verbose_name='사용자 패스워드')
    user_name = models.CharField(max_length=16, unique=True, verbose_name='사용자 이름')
    user_email = models.CharField(max_length=128, unique=True, verbose_name='사용자 이메일')
    user_register = models.DateTimeField(auto_now=True, verbose_name='계정 생성시간')

    
    class Meta:
        db_table = 'user'
