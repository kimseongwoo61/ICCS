<<<<<<< HEAD
from django.contrib import admin
from .models import Token_info
from .models import QnA


admin.site.register(Token_info)
admin.site.register(QnA)
# Register your models here.
=======
from django.contrib import admin
from .models import User, Token_info


admin.site.unregister(User)
admin.site.register(Token_info)
admin.site.register(User)
# Register your models here.
>>>>>>> 719cd225de0c04018c059ed171d0c81cd36fa789
