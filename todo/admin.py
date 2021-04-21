from django.contrib import admin
from .models import UserInfo, Todo


class UserInfoAdmin(admin.ModelAdmin):

    list_display = ('user_no','user_id', 'name', 'mail', 'birthday', 'regist_date', 'withdrawal_date')

# Register your models here.
admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(Todo)
