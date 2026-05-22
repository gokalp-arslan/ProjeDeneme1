from django.contrib import admin
from django.urls import path, include

# Hocanın 2. maddede eklenmesini istediği importlar
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('contact.urls')),
]

# Geliştirme ortamında medya dosyaları; CSS/JS için runserver + staticfiles yeterli
# (STATIC_ROOT boşken static() eklemek ana sayfada CSS/JS 404 verir, sayfa "bozuk" görünür)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)