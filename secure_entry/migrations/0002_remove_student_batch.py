# Generated by Django 5.0.3 on 2024-05-19 08:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('secure_entry', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='batch',
        ),
    ]
