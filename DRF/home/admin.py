from django.contrib import admin
from . models import MyUser,UserProfile,Shammas

# Register your models here.

admin.site.register(MyUser)
admin.site.register(UserProfile)
admin.site.register(Shammas)

class myuserAdmin(admin.ModelAdmin):
    list_display = ['id','user','age']