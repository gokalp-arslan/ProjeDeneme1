from django.contrib import admin

from .models import (
    EgitimKaydi,
    GelenMesaj,
    GirisBolumu,
    Hakkimda,
    Hizmet,
    IletisimBilgisi,
    IsDeneyimi,
    OzgecmisProfili,
    PortfolyoProjesi,
    SayisalIstatistik,
    SertifikaKaydi,
    SiteAyari,
    SosyalMedyaLinki,
    Yetenek,
    Yorum,
)


@admin.register(SiteAyari)
class SiteAyariAdmin(admin.ModelAdmin):
    list_display = ['anahtar', 'deger', 'aciklama', 'guncellenme_tarihi']
    search_fields = ['anahtar', 'deger']
    list_editable = ['deger']


@admin.register(GirisBolumu)
class GirisBolumuAdmin(admin.ModelAdmin):
    list_display = ['ad', 'soyad', 'universite', 'bolum', 'aktif']
    list_editable = ['aktif']


@admin.register(Hakkimda)
class HakkimdaAdmin(admin.ModelAdmin):
    list_display = ['unvan', 'eposta', 'deneyim_seviyesi', 'aktif']
    search_fields = ['unvan', 'onyazi', 'ilerledigi_alanlar']


@admin.register(SayisalIstatistik)
class SayisalIstatistikAdmin(admin.ModelAdmin):
    list_display = [
        'proje_sayisi',
        'is_yeri_sayisi',
        'arastirma_raporu_sayisi',
        'sertifika_sayisi',
        'aktif',
    ]


@admin.register(Yetenek)
class YetenekAdmin(admin.ModelAdmin):
    list_display = ['ad', 'yuzde', 'sira', 'aktif']
    list_editable = ['yuzde', 'sira', 'aktif']
    ordering = ['sira']


class IsDeneyimiInline(admin.TabularInline):
    model = IsDeneyimi
    extra = 0
    fields = [
        'baslangic_tarihi', 'bitis_tarihi', 'kurum_adi',
        'pozisyon', 'aciklama', 'sira',
    ]


class EgitimKaydiInline(admin.TabularInline):
    model = EgitimKaydi
    extra = 0
    fields = [
        'baslangic_tarihi', 'bitis_tarihi', 'okul_adi',
        'bolum', 'aciklama', 'sira',
    ]


class SertifikaKaydiInline(admin.TabularInline):
    model = SertifikaKaydi
    extra = 0
    fields = ['sertifika_adi', 'veren_kurum', 'tarih', 'sira']


@admin.register(OzgecmisProfili)
class OzgecmisProfiliAdmin(admin.ModelAdmin):
    list_display = ['id', 'aktif', 'guncellenme_tarihi']
    inlines = [IsDeneyimiInline, EgitimKaydiInline, SertifikaKaydiInline]
    fieldsets = (
        ('Özgeçmiş Metinleri', {
            'fields': ('profesyonel_ozet', 'iletisim_ozeti', 'teknik_beceriler'),
            'description': (
                'Sadece <strong>Profesyonel Özet</strong> doldurarak kaydedebilirsiniz. '
                'Deneyim, eğitim ve sertifikaları aşağıdan ayrı satırlarla ekleyin.'
            ),
        }),
        ('Görsel ve Durum', {
            'fields': ('profil_fotografi', 'aktif'),
        }),
    )


@admin.register(PortfolyoProjesi)
class PortfolyoProjesiAdmin(admin.ModelAdmin):
    list_display = ['proje_adi', 'kategori', 'sira', 'aktif']
    list_editable = ['sira', 'aktif']
    list_filter = ['kategori']


@admin.register(Hizmet)
class HizmetAdmin(admin.ModelAdmin):
    list_display = ['baslik', 'ikon', 'sira', 'aktif']
    list_editable = ['sira', 'aktif']


@admin.register(Yorum)
class YorumAdmin(admin.ModelAdmin):
    list_display = ['yorumcu_adi', 'yorum_tarihi', 'onaylandi', 'olusturulma_tarihi']
    list_filter = ['onaylandi', 'yorum_tarihi']
    list_editable = ['onaylandi']
    search_fields = ['yorumcu_adi', 'yorum_metni']


@admin.register(SosyalMedyaLinki)
class SosyalMedyaLinkiAdmin(admin.ModelAdmin):
    list_display = ['platform_adi', 'url', 'ikon_sinifi', 'sira', 'aktif']
    list_editable = ['sira', 'aktif']


@admin.register(IletisimBilgisi)
class IletisimBilgisiAdmin(admin.ModelAdmin):
    list_display = ['eposta', 'telefon', 'adres', 'aktif']


@admin.register(GelenMesaj)
class GelenMesajAdmin(admin.ModelAdmin):
    list_display = ['ad_soyad', 'eposta', 'konu', 'okundu', 'olusturulma_tarihi']
    list_filter = ['okundu']
    list_editable = ['okundu']
    readonly_fields = ['olusturulma_tarihi', 'guncellenme_tarihi']
