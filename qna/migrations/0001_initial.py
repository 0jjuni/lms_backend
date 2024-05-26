# Generated by Django 5.0.3 on 2024-05-26 09:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_code', models.CharField(max_length=10, verbose_name='subject code')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('text', models.TextField(verbose_name='text')),
                ('date_posted', models.DateTimeField(auto_now_add=True, verbose_name='date posted')),
                ('status', models.IntegerField(choices=[(0, 'public'), (1, 'private')], default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'notice board',
                'verbose_name_plural': 'notice boards',
                'abstract': False,
            },
        ),
    ]
