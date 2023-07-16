from django.contrib import admin
from .models import User, Token_info


admin.site.unregister(User)
admin.site.register(Token_info)
admin.site.register(User)
# Register your models here.
