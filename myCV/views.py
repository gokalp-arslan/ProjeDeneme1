from django.contrib import messages
from django.db.models import Prefetch
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import IletisimMesajForm, YorumForm
from .models import (
    EgitimKaydi,
    GirisBolumu,
    Hakkimda,
    Hizmet,
    IletisimBilgisi,
    IsDeneyimi,
    OzgecmisProfili,
    PortfolyoProjesi,
    SayisalIstatistik,
    SiteAyari,
    SertifikaKaydi,
    SosyalMedyaLinki,
    Yetenek,
    Yorum,
)


def site_ayari_getir(anahtar, varsayilan=''):
    try:
        return SiteAyari.objects.get(anahtar=anahtar).deger
    except SiteAyari.DoesNotExist:
        return varsayilan


def ortak_site_context():
    return {
        'site_title': site_ayari_getir('site_title', 'CV Portföy'),
        'site_keywords': site_ayari_getir('site_keywords'),
        'site_description': site_ayari_getir('site_description'),
        'about_myself_footer': site_ayari_getir(
            'about_myself_footer',
            '&copy; Tüm hakları saklıdır.',
        ),
    }


def portfoy_verilerini_getir():
    """Admin panelindeki tüm aktif içerikleri tek seferde yükler."""
    hero = GirisBolumu.objects.filter(aktif=True).order_by('-guncellenme_tarihi').first()
    hakkimda = Hakkimda.objects.filter(aktif=True).order_by('-guncellenme_tarihi').first()
    istatistik = SayisalIstatistik.objects.filter(aktif=True).order_by('-guncellenme_tarihi').first()
    yetenekler = Yetenek.objects.filter(aktif=True).order_by('sira', 'ad')
    ozgecmis = (
        OzgecmisProfili.objects.filter(aktif=True)
        .order_by('-guncellenme_tarihi')
        .prefetch_related(
            Prefetch('deneyimler', queryset=IsDeneyimi.objects.order_by('sira', '-id')),
            Prefetch('egitimler', queryset=EgitimKaydi.objects.order_by('sira', '-id')),
            Prefetch('sertifikalar', queryset=SertifikaKaydi.objects.order_by('sira', '-id')),
        )
        .first()
    )
    projeler = PortfolyoProjesi.objects.filter(aktif=True).order_by('sira', '-id')
    hizmetler = Hizmet.objects.filter(aktif=True).order_by('sira', 'baslik')
    yorumlar = Yorum.objects.filter(onaylandi=True).order_by('-yorum_tarihi')
    sosyal_medya = SosyalMedyaLinki.objects.filter(aktif=True).order_by('sira')
    iletisim = IletisimBilgisi.objects.filter(aktif=True).order_by('-guncellenme_tarihi').first()

    portfolyo_kategorileri = projeler.values_list('kategori', flat=True).distinct().order_by('kategori')

    return {
        'hero': hero,
        'hakkimda': hakkimda,
        'istatistik': istatistik,
        'yetenekler': yetenekler,
        'ozgecmis': ozgecmis,
        'projeler': projeler,
        'portfolyo_kategorileri': portfolyo_kategorileri,
        'hizmetler': hizmetler,
        'yorumlar': yorumlar,
        'sosyal_medya': sosyal_medya,
        'iletisim': iletisim,
    }


def index(request):
    yorum_form = YorumForm()
    mesaj_form = IletisimMesajForm()

    if request.method == 'POST':
        form_tipi = request.POST.get('form_tipi')

        if form_tipi == 'yorum':
            yorum_form = YorumForm(request.POST)
            if yorum_form.is_valid():
                yorum = yorum_form.save(commit=False)
                yorum.onaylandi = False
                yorum.save()
                messages.success(
                    request,
                    'Yorumunuz alındı. Onaylandıktan sonra sitede yayınlanacaktır.',
                )
                return redirect(reverse('index') + '#testimonials')
            messages.error(request, 'Yorum gönderilemedi. Lütfen alanları kontrol edin.')

        elif form_tipi == 'mesaj':
            mesaj_form = IletisimMesajForm(request.POST)
            if mesaj_form.is_valid():
                mesaj_form.save()
                messages.success(
                    request,
                    'Mesajınız başarıyla gönderildi. En kısa sürede dönüş yapacağım.',
                )
                return redirect(reverse('index') + '#contact')
            messages.error(request, 'Mesaj gönderilemedi. Lütfen alanları kontrol edin.')

    context = {
        **ortak_site_context(),
        **portfoy_verilerini_getir(),
        'yorum_form': yorum_form,
        'mesaj_form': mesaj_form,
    }
    return render(request, 'index.html', context)


def contact(request):
    """Tek sayfa deneyimi: iletişim bölümüne yönlendir."""
    if request.method == 'POST':
        mesaj_form = IletisimMesajForm(request.POST)
        if mesaj_form.is_valid():
            mesaj_form.save()
            messages.success(
                request,
                'Mesajınız başarıyla gönderildi. En kısa sürede dönüş yapacağım.',
            )
        else:
            messages.error(request, 'Mesaj gönderilemedi. Lütfen alanları kontrol edin.')
    return redirect(reverse('index') + '#contact')
