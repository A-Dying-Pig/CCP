from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CCPUser

admin.site.register(CCPUser, UserAdmin)
# Register your models here.
