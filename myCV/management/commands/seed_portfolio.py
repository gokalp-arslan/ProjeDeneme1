from django.core.management.base import BaseCommand

from myCV.models import Yetenek

VARSAYILAN_YETENEKLER = [
    ('HTML', 90),
    ('CSS', 85),
    ('Angular', 70),
    ('Python', 88),
    ('SQL', 82),
    ('Java', 75),
    ('JavaScript', 86),
    ('C', 70),
    ('C++', 72),
    ('C#', 74),
    ('AutoCAD', 65),
]


class Command(BaseCommand):
    help = 'Varsayılan yetenek kayıtlarını oluşturur (yoksa).'

    def handle(self, *args, **options):
        olusturulan = 0
        for sira, (ad, yuzde) in enumerate(VARSAYILAN_YETENEKLER, start=1):
            _, created = Yetenek.objects.get_or_create(
                ad=ad,
                defaults={'yuzde': yuzde, 'sira': sira, 'aktif': True},
            )
            if created:
                olusturulan += 1
        self.stdout.write(
            self.style.SUCCESS(f'Tamamlandı. {olusturulan} yeni yetenek eklendi.')
        )
