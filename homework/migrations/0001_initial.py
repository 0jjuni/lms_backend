# Generated by Django 5.0.3 on 2024-05-27 09:14

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Register",
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
                (
                    "subject_code",
                    models.CharField(max_length=10, verbose_name="subject code"),
                ),
                ("title", models.CharField(max_length=100, verbose_name="title")),
                ("text", models.TextField(verbose_name="text")),
                (
                    "date_posted",
                    models.DateTimeField(auto_now_add=True, verbose_name="date posted"),
                ),
                ("due_date", models.DateTimeField(blank=True, null=True)),
                (
                    "upload",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="C:/Users/kilho/Documents/asyouwrite",
                    ),
                ),
            ],
            options={
                "verbose_name": "notice board",
                "verbose_name_plural": "notice boards",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Submission",
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
                (
                    "subject_code",
                    models.CharField(max_length=10, verbose_name="subject code"),
                ),
                ("title", models.CharField(max_length=100, verbose_name="title")),
                ("text", models.TextField(verbose_name="text")),
                (
                    "upload",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="C:/Users/kilho/Documents/asyouwrite",
                    ),
                ),
                ("date_posted", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "notice board",
                "verbose_name_plural": "notice boards",
                "abstract": False,
            },
        ),
    ]
