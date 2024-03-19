# Generated by Django 5.0.3 on 2024-03-06 08:17

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TotalLecture",
            fields=[
                (
                    "grade",
                    models.IntegerField(blank=True, db_column="Grade", null=True),
                ),
                (
                    "course_classification",
                    models.CharField(
                        blank=True,
                        db_column="Course_Classification",
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "course_number",
                    models.AutoField(
                        db_column="Course_Number", primary_key=True, serialize=False
                    ),
                ),
                (
                    "course_name",
                    models.CharField(
                        blank=True, db_column="Course_Name", max_length=50, null=True
                    ),
                ),
                (
                    "course_type",
                    models.CharField(
                        blank=True, db_column="Course_Type", max_length=50, null=True
                    ),
                ),
                (
                    "class_type",
                    models.CharField(
                        blank=True, db_column="Class_Type", max_length=50, null=True
                    ),
                ),
                (
                    "instructor",
                    models.CharField(
                        blank=True, db_column="Instructor", max_length=50, null=True
                    ),
                ),
                (
                    "lecture_time",
                    models.CharField(
                        blank=True, db_column="Lecture_Time", max_length=50, null=True
                    ),
                ),
                (
                    "classroom",
                    models.CharField(
                        blank=True, db_column="Classroom", max_length=50, null=True
                    ),
                ),
                (
                    "credit",
                    models.IntegerField(blank=True, db_column="Credit", null=True),
                ),
                (
                    "department_quota",
                    models.IntegerField(
                        blank=True, db_column="Department_Quota", null=True
                    ),
                ),
                (
                    "outside_department_quota",
                    models.IntegerField(
                        blank=True, db_column="Outside_Department_Quota", null=True
                    ),
                ),
                (
                    "minor_dual_major_quota",
                    models.IntegerField(
                        blank=True, db_column="Minor/Dual_Major_Quota", null=True
                    ),
                ),
                (
                    "general_category",
                    models.CharField(
                        blank=True,
                        db_column="General_Category",
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "core_competency",
                    models.CharField(
                        blank=True,
                        db_column="Core_Competency",
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "recognized_credits",
                    models.CharField(
                        blank=True,
                        db_column="Recognized_Credits",
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "class_section",
                    models.CharField(
                        blank=True, db_column="Class_Section", max_length=50, null=True
                    ),
                ),
                (
                    "remarks",
                    models.CharField(
                        blank=True, db_column="Remarks", max_length=100, null=True
                    ),
                ),
                (
                    "department_name",
                    models.CharField(db_column="Department_Name", max_length=50),
                ),
            ],
            options={
                "db_table": "total_lecture",
                "managed": True,
                "unique_together": {("course_number", "department_name")},
            },
        ),
    ]
