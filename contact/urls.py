from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # Ana sayfa adresi (127.0.0.1:8000)
    path('contact/', views.contact_view, name='contact'), # Şikayet sayfası adresi (127.0.0.1:8000/contact/)
]