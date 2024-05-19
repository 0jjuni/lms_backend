# Generated by Django 5.0.3 on 2024-05-19 08:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("secure_entry", "0002_remove_student_batch"),
    ]

    operations = [
        migrations.CreateModel(
            name="Courses",
            fields=[
                (
                    "courses_code",
                    models.CharField(max_length=10, primary_key=True, serialize=False),
                ),
                (
                    "courses_div",
                    models.CharField(
                        choices=[
                            ("GE", "교양"),
                            ("GE_REQ", "교양필수"),
                            ("MAJ_ELECT", "전공선택"),
                            ("MAJ_REQ", "전공필수"),
                            ("CORE", "전공핵심"),
                            ("GEN_ELECT", "일반선택"),
                            ("EDU", "교직"),
                        ],
                        max_length=10,
                    ),
                ),
                ("courses_name", models.CharField(max_length=100)),
                ("classroom", models.CharField(max_length=50)),
                (
                    "professor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="secure_entry.professor",
                    ),
                ),
            ],
        ),
    ]
