# Generated by Django 5.0.3 on 2024-05-23 13:54

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0002_announcement"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Batch",
        ),
    ]
