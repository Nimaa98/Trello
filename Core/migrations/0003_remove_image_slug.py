# Generated by Django 4.2.4 on 2025-02-12 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Core", "0002_image_slug"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="image",
            name="slug",
        ),
    ]
