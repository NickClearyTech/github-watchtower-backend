# Generated by Django 4.1 on 2022-09-05 02:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("watchtower_service", "0003_rename_app_id_installation_app"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="installation",
            name="id",
        ),
        migrations.AlterField(
            model_name="installation",
            name="installation_id",
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name="Repository",
            fields=[
                (
                    "repository_id",
                    models.IntegerField(primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=512)),
                ("archived", models.BooleanField(default=False)),
                ("description", models.CharField(max_length=1024, null=True)),
                ("is_fork", models.BooleanField(default=False)),
                ("has_downloads", models.BooleanField(default=False)),
                ("has_issues", models.BooleanField(default=False)),
                ("has_pages", models.BooleanField(default=False)),
                ("has_projects", models.BooleanField(default=False)),
                ("has_wiki", models.BooleanField(default=False)),
                ("language", models.CharField(max_length=128, null=True)),
                (
                    "master_branch",
                    models.CharField(default="main", max_length=512, null=True),
                ),
                ("is_private", models.BooleanField(default=False)),
                ("last_pushed_at", models.DateTimeField(null=True)),
                ("size", models.IntegerField(null=True)),
                ("subscribers_count", models.IntegerField(default=0, null=True)),
                ("last_updated", models.DateTimeField(null=True)),
                ("owner_id", models.IntegerField()),
                (
                    "owner_type",
                    models.CharField(
                        choices=[("org", "Organization"), ("user", "User")],
                        default="org",
                        max_length=4,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateField(auto_now=True)),
                (
                    "installation",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="repositories",
                        to="watchtower_service.installation",
                    ),
                ),
            ],
            options={
                "unique_together": {("owner_id", "owner_type")},
            },
        ),
    ]