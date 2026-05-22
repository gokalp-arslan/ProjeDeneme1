from django.db import models


class GeneralSetting(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ad Soyad")
    title = models.CharField(max_length=100, verbose_name="Unvan (Title)")
    sub_title = models.CharField(max_length=255, verbose_name="Alt Başlık (Sub Title)")
    description = models.TextField(verbose_name="Hakkımda Kısa Açıklama")

    # ImageField yerine CharField kalarak Pillow hatasını kalıcı olarak engelledik knk
    profile_image = models.CharField(max_length=255, verbose_name="Profil Fotoğrafı")

    twitter = models.URLField(blank=True, null=True, verbose_name="Twitter / X Linki")
    facebook = models.URLField(blank=True, null=True, verbose_name="Facebook Linki")
    instagram = models.URLField(blank=True, null=True, verbose_name="Instagram Linki")
    linkedin = models.URLField(blank=True, null=True, verbose_name="LinkedIn Linki")

    class Meta:
        verbose_name = "Genel Ayar"
        verbose_name_plural = "Genel Ayarlar"

    def __str__(self):
        return self.name