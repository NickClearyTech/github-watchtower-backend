from django.apps import AppConfig
from django.db import models
from django.contrib.auth.models import User


class SignalApp(AppConfig):
    # Literally to just register the User created signal
    name = "watchtower_signals"
    verbose_name = "Watchtower Signals"

    def ready(self):
        from watchtower_service.signals import create_user_token

        models.signals.post_save.connect(create_user_token, sender=User)
