from django import forms

from .models import GelenMesaj, Yorum


class YorumForm(forms.ModelForm):
    class Meta:
        model = Yorum
        fields = ['yorum_metni', 'yorumcu_adi', 'yorumcu_unvan']
        widgets = {
            'yorum_metni': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Yorumunuzu yazın...',
                'required': True,
            }),
            'yorumcu_adi': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Adınız Soyadınız',
                'required': True,
            }),
            'yorumcu_unvan': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Unvanınız (isteğe bağlı)',
            }),
        }
        labels = {
            'yorum_metni': 'Yorumunuz',
            'yorumcu_adi': 'Adınız Soyadınız',
            'yorumcu_unvan': 'Unvanınız',
        }


class IletisimMesajForm(forms.ModelForm):
    class Meta:
        model = GelenMesaj
        fields = ['ad_soyad', 'eposta', 'konu', 'mesaj']
        widgets = {
            'ad_soyad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Adınız Soyadınız',
            }),
            'eposta': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ornek@mail.com',
            }),
            'konu': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mesaj konusu',
            }),
            'mesaj': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Mesajınızı yazın...',
            }),
        }
        labels = {
            'ad_soyad': 'Ad Soyad',
            'eposta': 'E-posta',
            'konu': 'Konu',
            'mesaj': 'Mesaj',
        }
