from django.contrib import admin
from .models import userLogin,MasterTable,Session
# Register your models here.
admin.site.register(userLogin)
admin.site.register(MasterTable)
admin.site.register(Session)