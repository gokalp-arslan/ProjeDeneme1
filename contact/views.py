from django.shortcuts import render


def index(request):
    try:
        from myCV.views import index as cv_index
        return cv_index(request)
    except Exception as e:
        return render(
            request,
            'index_error.html',
            {'hata': str(e)},
            status=500,
        )


def contact_view(request):
    try:
        from myCV.views import contact as cv_contact
        return cv_contact(request)
    except Exception as e:
        return render(
            request,
            'index_error.html',
            {'hata': str(e)},
            status=500,
        )
