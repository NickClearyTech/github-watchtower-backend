from django.db import models


# Create your models here.


class WebhookEvent(models.Model):
    event_json = models.JSONField()


class Organization(models.Model):
    organization_id = models.IntegerField(null=False, primary_key=True)
    organization_login = models.CharField(null=False, max_length=256, db_index=True)
    organization_name = models.CharField(null=True, max_length=256)
    organization_type = models.CharField(null=True, max_length=32)
    description = models.CharField(null=True, max_length=2048)
    email = models.EmailField(null=True)

    created_at = models.DateTimeField(null=False, auto_now_add=True)
    updated_at = models.DateTimeField(null=False, auto_now=True)

    company = models.CharField(null=True, max_length=128)
    # plan = models.Charfield() Add this later

    avatar_url = models.URLField(null=True)

    default_repository_permission = models.CharField(null=True, max_length=32)

    disk_usage = models.IntegerField(null=True)


class App(models.Model):
    class OwnerTypeChoices(models.TextChoices):
        USER = "user"
        ORGANIZATION = "org"

    ### TODO: Implement on .save() check for valid owner

    app_id = models.IntegerField(null=False, primary_key=True)
    name = models.CharField(null=True, max_length=256)
    slug = models.CharField(null=True, max_length=256, db_index=True)
    installation_count = models.IntegerField(null=True)

    owner_id = models.IntegerField(null=False)
    owner_type = models.CharField(
        null=False, max_length=4, choices=OwnerTypeChoices.choices, default="org"
    )

    created_at = models.DateTimeField(null=False, auto_now_add=True)
    updated_at = models.DateTimeField(null=False, auto_now=True)


class Installation(models.Model):
    class TargetTypeChoice(models.TextChoices):
        ORGANIZATION = "org"
        REPOSITORY = "repo"

    ### TODO: Implement on .save() check for valid target

    installation_id = models.IntegerField(null=False, primary_key=True)
    app = models.ForeignKey(App, on_delete=models.CASCADE)

    target_id = models.IntegerField(null=False)
    target_type = models.CharField(
        null=False, max_length=4, choices=TargetTypeChoice.choices, default="org"
    )

    created_at = models.DateTimeField(null=False, auto_now_add=True)
    updated_at = models.DateTimeField(null=False, auto_now=True)


class Repository(models.Model):
    class OwnerTypeChoice(models.TextChoices):
        ORGANIZATION = "org"
        USER = "user"

    repository_id = models.IntegerField(null=False, primary_key=True)
    name = models.CharField(null=False, max_length=512)

    archived = models.BooleanField(null=False, default=False)
    description = models.CharField(null=True, max_length=1024)
    is_fork = models.BooleanField(null=False, default=False)
    has_downloads = models.BooleanField(null=False, default=False)
    has_issues = models.BooleanField(null=False, default=False)
    has_pages = models.BooleanField(null=False, default=False)
    has_projects = models.BooleanField(null=False, default=False)
    has_wiki = models.BooleanField(null=False, default=False)
    language = models.CharField(null=True, max_length=128)
    master_branch = models.CharField(null=True, default="main", max_length=512)
    is_private = models.BooleanField(default=False, null=False)
    last_pushed_at = models.DateTimeField(null=True)
    size = models.IntegerField(null=True)
    subscribers_count = models.IntegerField(null=True, default=0)
    # Represents when repository was last updated on github
    last_updated = models.DateTimeField(null=True)

    owner_id = models.IntegerField(null=True)
    owner_type = models.CharField(
        null=False, max_length=4, choices=OwnerTypeChoice.choices, default="org"
    )

    # TODO: Implement parent repository functionality here
    # parent

    # A little helper bit to easily grab the installation necessary to access the repo through the github API
    installation = models.ForeignKey(
        Installation, on_delete=models.CASCADE, null=True, related_name="repositories"
    )

    created_at = models.DateTimeField(null=False, auto_now_add=True)
    # Represents when object in database was last updated, not when item on github was updated
    updated_at = models.DateTimeField(null=False, auto_now=True)
