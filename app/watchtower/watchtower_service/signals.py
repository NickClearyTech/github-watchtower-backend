from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

import logging
logger = logging.getLogger(__name__)


@receiver(models.signals.post_save, sender=User)
def create_user_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.get_or_create(user=instance)
        logger.info(f"Created token object for user {instance.id}")
