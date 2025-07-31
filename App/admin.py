from django.contrib import admin
from .models import BirthdayInfo, AdminProfile

# Register your models here.
admin.site.register(BirthdayInfo)
admin.site.register(AdminProfile)
