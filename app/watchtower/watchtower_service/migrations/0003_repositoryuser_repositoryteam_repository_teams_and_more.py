# Generated by Django 4.1.1 on 2022-10-04 03:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("watchtower_service", "0002_alter_githubuser_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="RepositoryUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "permission",
                    models.CharField(
                        choices=[
                            ("read", "Read"),
                            ("write", "Write"),
                            ("admin", "Admin"),
                        ],
                        default="read",
                        max_length=8,
                    ),
                ),
                (
                    "repo",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="watchtower_service.repository",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="watchtower_service.githubuser",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RepositoryTeam",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "permission",
                    models.CharField(
                        choices=[
                            ("read", "Read"),
                            ("write", "Write"),
                            ("admin", "Admin"),
                        ],
                        default="read",
                        max_length=8,
                    ),
                ),
                (
                    "repo",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="watchtower_service.repository",
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="watchtower_service.team",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="repository",
            name="teams",
            field=models.ManyToManyField(
                related_name="repos",
                through="watchtower_service.RepositoryTeam",
                to="watchtower_service.team",
            ),
        ),
        migrations.AddField(
            model_name="repository",
            name="users",
            field=models.ManyToManyField(
                related_name="repos",
                through="watchtower_service.RepositoryUser",
                to="watchtower_service.githubuser",
            ),
        ),
    ]
