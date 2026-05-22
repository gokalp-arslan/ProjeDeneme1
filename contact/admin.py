from django.contrib import admin
from .models import GeneralSetting

@admin.register(GeneralSetting)
class GeneralSettingAdmin(admin.ModelAdmin):
    # Admin panelinde listenirken görünecek başlıklar
    list_display = ('id', 'name', 'title', 'sub_title')