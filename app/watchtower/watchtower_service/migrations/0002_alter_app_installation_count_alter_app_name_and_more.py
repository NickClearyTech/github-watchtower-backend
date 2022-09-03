# Generated by Django 4.0.6 on 2022-08-31 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("watchtower_service", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="app",
            name="installation_count",
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="app",
            name="name",
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name="app",
            name="slug",
            field=models.CharField(db_index=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name="organization",
            name="default_repository_permission",
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name="organization",
            name="organization_type",
            field=models.CharField(max_length=32, null=True),
        ),
    ]