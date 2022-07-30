from django.db import models

# Create your models here.


class WebhookEvent(models.Model):
    event_json = models.JSONField()


class Installation(models.Model):
    installation_id = models.IntegerField(null=False)
    installation_name = models.CharField(null=False, max_length=128)
