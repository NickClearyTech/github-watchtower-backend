from django.apps import AppConfig

# from django.db import models
# from django.contrib.auth.models import User


class WatchtowerServiceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "watchtower_service"

    def ready(self):
        from watchtower_service.signals import create_user_token
        from django.db import models
        from django.contrib.auth.models import User

        models.signals.post_save.connect(create_user_token, sender=User)
