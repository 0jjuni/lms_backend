# Generated by Django 5.0.3 on 2024-05-25 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homework', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='register',
            name='due_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
