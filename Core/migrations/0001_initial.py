# Generated by Django 4.2.4 on 2025-02-12 14:23

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("create_at", models.DateTimeField(auto_now_add=True)),
                ("update_at", models.DateTimeField(auto_now=True)),
                (
                    "alt_text",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        verbose_name="Alternative Text",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True, max_length=200, null=True, verbose_name="Name"
                    ),
                ),
                ("Image", models.ImageField(upload_to="images/", verbose_name="Image")),
            ],
            options={
                "verbose_name": "Image",
                "verbose_name_plural": "Images",
            },
        ),
    ]
