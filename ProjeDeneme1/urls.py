from django.contrib import admin
from django.urls import path, include # include buraya eklendi, çok önemli!

urlpatterns = [
    path('admin/', admin.site.urls),
    # Burası 'contact' isimli app'indeki urls.py dosyasına kapı açıyor:
    path('', include('contact.urls')),
]