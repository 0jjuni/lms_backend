# Generated by Django 5.0.3 on 2024-06-04 14:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team_connect', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Connect_answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_code', models.CharField(max_length=10)),
                ('text', models.TextField(verbose_name='text')),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('Connect', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='connect', to='team_connect.connect')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
