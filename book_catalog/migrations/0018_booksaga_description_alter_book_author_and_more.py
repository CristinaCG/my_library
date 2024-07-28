# Generated by Django 4.2.9 on 2024-07-28 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("book_catalog", "0017_author_biography_author_social_media"),
    ]

    operations = [
        migrations.AddField(
            model_name="booksaga",
            name="description",
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name="book",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="book_catalog.author"
            ),
        ),
        migrations.AlterField(
            model_name="book",
            name="saga",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="book_catalog.booksaga",
            ),
        ),
    ]
