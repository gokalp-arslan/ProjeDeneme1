from django.db import models
from django.utils import timezone


class ZamanDamgasi(models.Model):
    guncellenme_tarihi = models.DateTimeField(
        auto_now=True,
        verbose_name='Güncellenme Tarihi',
    )
    olusturulma_tarihi = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Oluşturulma Tarihi',
    )

    class Meta:
        abstract = True


# ---------------------------------------------------------------------------
# Site genel ayarları (eski GeneralSetting yapısı — geriye dönük uyumluluk)
# ---------------------------------------------------------------------------
class SiteAyari(ZamanDamgasi):
    anahtar = models.CharField(
        max_length=254,
        unique=True,
        verbose_name='Ayar Anahtarı',
        help_text='Örn: site_title, about_myself_footer',
    )
    aciklama = models.CharField(
        max_length=254,
        blank=True,
        verbose_name='Açıklama',
    )
    deger = models.CharField(
        max_length=500,
        blank=True,
        verbose_name='Değer',
    )

    class Meta:
        verbose_name = 'Site Ayarı'
        verbose_name_plural = 'Site Ayarları'
        ordering = ('anahtar',)

    def __str__(self):
        return self.anahtar


# 1 — Giriş (Hero)
# ---------------------------------------------------------------------------
class GirisBolumu(ZamanDamgasi):
    ad = models.CharField(max_length=100, verbose_name='Ad')
    soyad = models.CharField(max_length=100, verbose_name='Soyad')
    universite = models.CharField(max_length=254, verbose_name='Okunan Üniversite')
    bolum = models.CharField(max_length=254, verbose_name='Bölüm')
    kisa_aciklama = models.TextField(
        blank=True,
        verbose_name='Kısa Tanıtım',
        help_text='Hero altında görünen kısa metin.',
    )
    profil_fotografi = models.ImageField(
        upload_to='profil/',
        blank=True,
        null=True,
        verbose_name='Profil Fotoğrafı',
    )
    aktif = models.BooleanField(default=True, verbose_name='Aktif')

    class Meta:
        verbose_name = 'Giriş (Hero) Bilgisi'
        verbose_name_plural = 'Giriş (Hero) Bilgileri'

    def __str__(self):
        return f'{self.ad} {self.soyad}'

    @property
    def tam_ad(self):
        return f'{self.ad} {self.soyad}'.strip()


# 2 — Hakkımda (About)
# ---------------------------------------------------------------------------
class Hakkimda(ZamanDamgasi):
    unvan = models.CharField(
        max_length=254,
        verbose_name='Unvan',
        help_text='Örn: Yazılım Geliştirici',
    )
    eposta = models.EmailField(verbose_name='E-posta')
    telefon = models.CharField(max_length=30, verbose_name='Telefon')
    adres = models.CharField(max_length=500, blank=True, verbose_name='Adres')
    onyazi = models.TextField(verbose_name='Hakkımda Önyazısı')
    ilerledigi_alanlar = models.CharField(
        max_length=500,
        verbose_name='İlerlediğim Alanlar',
    )
    deneyim_seviyesi = models.CharField(
        max_length=100,
        verbose_name='Deneyim Seviyesi',
        help_text='Örn: Junior, Mid-Level',
    )
    egitim_bilgileri = models.TextField(verbose_name='Eğitim Bilgileri')
    diller = models.CharField(
        max_length=500,
        verbose_name='Diller',
        help_text='Virgülle ayırarak yazın.',
    )
    profil_fotografi = models.ImageField(
        upload_to='hakkimda/',
        blank=True,
        null=True,
        verbose_name='Profil Fotoğrafı',
    )
    cv_dosyasi = models.FileField(
        upload_to='cv/',
        blank=True,
        null=True,
        verbose_name='CV Dosyası (PDF)',
    )
    aktif = models.BooleanField(default=True, verbose_name='Aktif')

    class Meta:
        verbose_name = 'Hakkımda Bilgisi'
        verbose_name_plural = 'Hakkımda Bilgileri'

    def __str__(self):
        return self.unvan


# 3 — Sayısal İstatistikler (Counters)
# ---------------------------------------------------------------------------
class SayisalIstatistik(ZamanDamgasi):
    proje_sayisi = models.PositiveIntegerField(default=0, verbose_name='Proje Sayısı')
    is_yeri_sayisi = models.PositiveIntegerField(default=0, verbose_name='Çalışılan İş Yeri Sayısı')
    arastirma_raporu_sayisi = models.PositiveIntegerField(
        default=0,
        verbose_name='Araştırma Raporu Sayısı',
    )
    sertifika_sayisi = models.PositiveIntegerField(default=0, verbose_name='Sertifika Sayısı')
    aktif = models.BooleanField(default=True, verbose_name='Aktif')

    class Meta:
        verbose_name = 'Sayısal İstatistik'
        verbose_name_plural = 'Sayısal İstatistikler'

    def __str__(self):
        return f'İstatistikler ({self.proje_sayisi} proje)'


# 4 — Yetenekler (Skills)
# ---------------------------------------------------------------------------
class Yetenek(ZamanDamgasi):
    ad = models.CharField(max_length=100, verbose_name='Yetenek Adı')
    yuzde = models.PositiveIntegerField(
        default=0,
        verbose_name='Yüzde (%)',
        help_text='0 ile 100 arasında bir değer girin.',
    )
    sira = models.PositiveIntegerField(default=0, verbose_name='Sıra')
    aktif = models.BooleanField(default=True, verbose_name='Aktif')

    class Meta:
        verbose_name = 'Yetenek'
        verbose_name_plural = 'Yetenekler'
        ordering = ('sira', 'ad')

    def __str__(self):
        return f'{self.ad} (%{self.yuzde})'


# 5 — CV / Özgeçmiş (Resume) — ana profil + ilişkili kayıtlar
# ---------------------------------------------------------------------------
class OzgecmisProfili(ZamanDamgasi):
    profesyonel_ozet = models.TextField(
        verbose_name='Profesyonel Özet',
        help_text='Özgeçmiş sayfasında görünen ana tanıtım metni.',
    )
    iletisim_ozeti = models.TextField(
        blank=True,
        verbose_name='İletişim Bilgileri Özeti',
        help_text='Özgeçmiş yan panelinde görünecek iletişim metni.',
    )
    teknik_beceriler = models.TextField(
        blank=True,
        default='',
        verbose_name='Teknik Beceriler',
        help_text='Her satıra bir beceri yazabilirsiniz. (İsteğe bağlı)',
    )
    profil_fotografi = models.ImageField(
        upload_to='ozgecmis/',
        blank=True,
        null=True,
        verbose_name='Özgeçmiş Profil Fotoğrafı',
    )
    aktif = models.BooleanField(default=True, verbose_name='Aktif')

    class Meta:
        verbose_name = 'Özgeçmiş Profili'
        verbose_name_plural = 'Özgeçmiş Profilleri'

    def __str__(self):
        return 'Özgeçmiş Profili'


class IsDeneyimi(ZamanDamgasi):
    profil = models.ForeignKey(
        OzgecmisProfili,
        on_delete=models.CASCADE,
        related_name='deneyimler',
        verbose_name='Özgeçmiş Profili',
    )
    baslangic_tarihi = models.CharField(
        max_length=50,
        verbose_name='Başlangıç Tarihi',
        help_text='Örn: 2022 veya Ocak 2022',
    )
    bitis_tarihi = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Bitiş Tarihi',
        help_text='Devam ediyorsa boş bırakın veya "Günümüz"',
    )
    kurum_adi = models.CharField(max_length=254, verbose_name='Kurum / Şirket')
    pozisyon = models.CharField(max_length=254, verbose_name='Pozisyon')
    aciklama = models.TextField(blank=True, verbose_name='Açıklama')
    sira = models.PositiveIntegerField(default=0, verbose_name='Sıra')

    class Meta:
        verbose_name = 'İş Deneyimi'
        verbose_name_plural = 'İş Deneyimleri'
        ordering = ('sira', '-baslangic_tarihi')

    def __str__(self):
        return f'{self.pozisyon} — {self.kurum_adi}'


class EgitimKaydi(ZamanDamgasi):
    profil = models.ForeignKey(
        OzgecmisProfili,
        on_delete=models.CASCADE,
        related_name='egitimler',
        verbose_name='Özgeçmiş Profili',
    )
    baslangic_tarihi = models.CharField(max_length=50, verbose_name='Başlangıç Tarihi')
    bitis_tarihi = models.CharField(max_length=50, blank=True, verbose_name='Bitiş Tarihi')
    okul_adi = models.CharField(max_length=254, verbose_name='Okul / Üniversite')
    bolum = models.CharField(max_length=254, verbose_name='Bölüm')
    aciklama = models.TextField(blank=True, verbose_name='Açıklama')
    sira = models.PositiveIntegerField(default=0, verbose_name='Sıra')

    class Meta:
        verbose_name = 'Eğitim Kaydı'
        verbose_name_plural = 'Eğitim Kayıtları'
        ordering = ('sira',)

    def __str__(self):
        return f'{self.okul_adi} — {self.bolum}'


class SertifikaKaydi(ZamanDamgasi):
    profil = models.ForeignKey(
        OzgecmisProfili,
        on_delete=models.CASCADE,
        related_name='sertifikalar',
        verbose_name='Özgeçmiş Profili',
    )
    sertifika_adi = models.CharField(max_length=254, verbose_name='Sertifika Adı')
    veren_kurum = models.CharField(max_length=254, blank=True, verbose_name='Veren Kurum')
    tarih = models.CharField(max_length=50, blank=True, verbose_name='Tarih')
    sira = models.PositiveIntegerField(default=0, verbose_name='Sıra')

    class Meta:
        verbose_name = 'Sertifika Kaydı'
        verbose_name_plural = 'Sertifika Kayıtları'
        ordering = ('sira',)

    def __str__(self):
        return self.sertifika_adi


# 6 — Portföy
# ---------------------------------------------------------------------------
class PortfolyoProjesi(ZamanDamgasi):
    proje_adi = models.CharField(max_length=254, verbose_name='Proje Adı')
    gorsel = models.ImageField(
        upload_to='portfolyo/',
        blank=True,
        null=True,
        verbose_name='Proje Görseli',
    )
    kategori = models.CharField(
        max_length=100,
        verbose_name='Kategori',
        help_text='Filtre için kullanılır. Örn: web, mobil, tasarım',
    )
    proje_linki = models.URLField(blank=True, verbose_name='Proje Linki')
    aciklama = models.TextField(blank=True, verbose_name='Açıklama')
    sira = models.PositiveIntegerField(default=0, verbose_name='Sıra')
    aktif = models.BooleanField(default=True, verbose_name='Aktif')

    class Meta:
        verbose_name = 'Portföy Projesi'
        verbose_name_plural = 'Portföy Projeleri'
        ordering = ('sira',)

    def __str__(self):
        return self.proje_adi


# 7 — Hizmetler
# ---------------------------------------------------------------------------
class Hizmet(ZamanDamgasi):
    baslik = models.CharField(max_length=254, verbose_name='Hizmet Başlığı')
    ikon = models.CharField(
        max_length=100,
        verbose_name='İkon Sınıfı',
        help_text='Bootstrap Icons sınıfı. Örn: bi bi-camera',
        default='bi bi-star',
    )
    aciklama = models.TextField(verbose_name='Açıklama')
    sira = models.PositiveIntegerField(default=0, verbose_name='Sıra')
    aktif = models.BooleanField(default=True, verbose_name='Aktif')

    class Meta:
        verbose_name = 'Hizmet'
        verbose_name_plural = 'Hizmetler'
        ordering = ('sira',)

    def __str__(self):
        return self.baslik


# 8 — Yorumlar (Testimonials)
# ---------------------------------------------------------------------------
class Yorum(ZamanDamgasi):
    yorum_metni = models.TextField(verbose_name='Yorum')
    yorumcu_adi = models.CharField(max_length=150, verbose_name='Yorumu Yapan')
    yorumcu_unvan = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Yorumu Yapanın Unvanı',
    )
    yorum_tarihi = models.DateField(
        default=timezone.now,
        verbose_name='Yorum Tarihi',
    )
    onaylandi = models.BooleanField(
        default=False,
        verbose_name='Onaylandı',
        help_text='Sitede yalnızca onaylanan yorumlar gösterilir.',
    )

    class Meta:
        verbose_name = 'Yorum'
        verbose_name_plural = 'Yorumlar'
        ordering = ('-yorum_tarihi',)

    def __str__(self):
        return f'{self.yorumcu_adi} — {self.yorum_tarihi}'


# 9 — Sosyal Medya
# ---------------------------------------------------------------------------
class SosyalMedyaLinki(ZamanDamgasi):
    platform_adi = models.CharField(max_length=100, verbose_name='Platform Adı')
    url = models.URLField(verbose_name='URL')
    ikon_sinifi = models.CharField(
        max_length=100,
        verbose_name='İkon Sınıfı',
        help_text='Örn: bi bi-linkedin, bi bi-github',
        default='bi bi-link-45deg',
    )
    sira = models.PositiveIntegerField(default=0, verbose_name='Sıra')
    aktif = models.BooleanField(default=True, verbose_name='Aktif')

    class Meta:
        verbose_name = 'Sosyal Medya Linki'
        verbose_name_plural = 'Sosyal Medya Linkleri'
        ordering = ('sira',)

    def __str__(self):
        return self.platform_adi


# 10 — İletişim
# ---------------------------------------------------------------------------
class IletisimBilgisi(ZamanDamgasi):
    adres = models.CharField(max_length=500, verbose_name='Adres')
    eposta = models.EmailField(verbose_name='E-posta')
    telefon = models.CharField(max_length=30, verbose_name='Telefon')
    harita_linki = models.URLField(blank=True, verbose_name='Harita Linki')
    aktif = models.BooleanField(default=True, verbose_name='Aktif')

    class Meta:
        verbose_name = 'İletişim Bilgisi'
        verbose_name_plural = 'İletişim Bilgileri'

    def __str__(self):
        return self.eposta


class GelenMesaj(ZamanDamgasi):
    ad_soyad = models.CharField(max_length=200, verbose_name='Ad Soyad')
    eposta = models.EmailField(verbose_name='E-posta')
    konu = models.CharField(max_length=300, verbose_name='Konu')
    mesaj = models.TextField(verbose_name='Mesaj')
    okundu = models.BooleanField(default=False, verbose_name='Okundu')

    class Meta:
        verbose_name = 'Gelen Mesaj'
        verbose_name_plural = 'Gelen Mesajlar'
        ordering = ('-olusturulma_tarihi',)

    def __str__(self):
        return f'{self.ad_soyad} — {self.konu}'
