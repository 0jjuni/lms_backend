# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class TotalLecture(models.Model):
    grade = models.IntegerField(db_column='Grade', blank=True, null=True)  # Field name made lowercase.
    course_classification = models.CharField(db_column='Course_Classification', max_length=50, blank=True, null=True)  # Field name made lowercase.
    course_number = models.AutoField(db_column='Course_Number', primary_key=True)  # Field name made lowercase. The composite primary key (Course_Number, Department_Name) found, that is not supported. The first column is selected.
    course_name = models.CharField(db_column='Course_Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    course_type = models.CharField(db_column='Course_Type', max_length=50, blank=True, null=True)  # Field name made lowercase.
    class_type = models.CharField(db_column='Class_Type', max_length=50, blank=True, null=True)  # Field name made lowercase.
    instructor = models.CharField(db_column='Instructor', max_length=50, blank=True, null=True)  # Field name made lowercase.
    lecture_time = models.CharField(db_column='Lecture_Time', max_length=50, blank=True, null=True)  # Field name made lowercase.
    classroom = models.CharField(db_column='Classroom', max_length=50, blank=True, null=True)  # Field name made lowercase.
    credit = models.IntegerField(db_column='Credit', blank=True, null=True)  # Field name made lowercase.
    department_quota = models.IntegerField(db_column='Department_Quota', blank=True, null=True)  # Field name made lowercase.
    outside_department_quota = models.IntegerField(db_column='Outside_Department_Quota', blank=True, null=True)  # Field name made lowercase.
    minor_dual_major_quota = models.IntegerField(db_column='Minor/Dual_Major_Quota', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    general_category = models.CharField(db_column='General_Category', max_length=50, blank=True, null=True)  # Field name made lowercase.
    core_competency = models.CharField(db_column='Core_Competency', max_length=50, blank=True, null=True)  # Field name made lowercase.
    recognized_credits = models.CharField(db_column='Recognized_Credits', max_length=50, blank=True, null=True)  # Field name made lowercase.
    class_section = models.CharField(db_column='Class_Section', max_length=50, blank=True, null=True)  # Field name made lowercase.
    remarks = models.CharField(db_column='Remarks', max_length=100, blank=True, null=True)  # Field name made lowercase.
    department_name = models.CharField(db_column='Department_Name', max_length=50)  # Field name made lowercase.


    def publish(self):
        self.save()

    def __str__(self):
        return self.course_number

    class Meta:
        managed = False
        db_table = 'total_lecture'
        unique_together = (('course_number', 'department_name'),)
