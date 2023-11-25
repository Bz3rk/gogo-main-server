from django.contrib import admin
from .models import CustomUser

# Register your models here.
admin.site.site_title = 'GoGo Admin'
admin.site.site_header = 'GoGo Administration'
admin.site.index_title = 'GoGo site admin'
admin.site.register(CustomUser)