# Generated by Django 4.2.9 on 2024-01-14 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="film",
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
                ("title", models.CharField(max_length=255)),
                ("director", models.CharField(max_length=255)),
                ("year", models.IntegerField()),
                ("synopsis", models.TextField()),
                ("category", models.CharField(max_length=100)),
            ],
        ),
    ]
