from django.db import models

# Create your models here.


class WebhookEvent(models.Model):
    event_json = models.JSONField()


class Organization(models.Model):
    organization_id = models.IntegerField(null=False, primary_key=True)
    organization_login = models.CharField(null=False, max_length=256, db_index=True)
    organization_name = models.CharField(null=False, max_length=256)
    organization_type = models.CharField(null=False, max_length=32)
    description = models.CharField(null=True, max_length=2048)
    email = models.EmailField(null=True)

    created_at = models.DateTimeField(null=False)
    update_at = models.DateField(null=False)

    company = models.CharField(null=True, max_length=128)
    # plan = models.Charfield() Add this later

    avatar_url = models.URLField(null=True)

    default_repository_permission = models.CharField(null=False, max_length=32)

    disk_usage = models.IntegerField(null=True)


class App(models.Model):
    class Meta:
        unique_together = ("owner_id", "owner_type")

    class OwnerTypeChoices(models.TextChoices):
        USER = "user"
        ORGANIZATION = "org"

    ### TODO: Implement on .save() check for valid owner

    app_id = models.IntegerField(null=False, primary_key=True)
    name = models.CharField(null=False, max_length=256)
    slug = models.CharField(null=False, max_length=256, db_index=True)
    installation_count = models.IntegerField(null=False)

    owner_id = models.IntegerField(null=False)
    owner_type = models.CharField(
        null=False, max_length=4, choices=OwnerTypeChoices.choices, default="org"
    )

    created_at = models.DateTimeField(null=False)
    update_at = models.DateField(null=False)


class Installation(models.Model):
    class Meta:
        unique_together = ("target_id", "target_type")

    class TargetTypeChoice(models.TextChoices):
        ORGANIZATION = "org"
        REPOSITORY = "repo"

    ### TODO: Implement on .save() check for valid target

    installation_id = models.IntegerField(null=False)
    app_id = models.ForeignKey(App, on_delete=models.CASCADE)

    target_id = models.IntegerField(null=False)
    target_type = models.CharField(
        null=False, max_length=4, choices=TargetTypeChoice.choices, default="org"
    )
