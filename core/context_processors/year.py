import datetime


def year(request):
    """Актуальный год в шаблонах"""

    return {
        'year': datetime.date.today().year,
    }
