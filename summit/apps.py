from django.apps import AppConfig


class SummitConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'summit'

    # было summit.signals
    def ready(self):
        import summit.signals  # noqa


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'summit'

    # было summit.signals
    def ready(self):
        import summit.signals  # noqa