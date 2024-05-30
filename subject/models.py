from django.db import models
from secure_entry.models import Professor
from secure_entry.models import Student



class Subject(models.Model):
    COURSE_DIV_CHOICES = [
        ('GE', '교양'),
        ('GE_REQ', '교양필수'),
        ('MAJ_ELECT', '전공선택'),
        ('MAJ_REQ', '전공필수'),
        ('CORE', '전공핵심'),
        ('GEN_ELECT', '일반선택'),
        ('EDU', '교직'),
    ]

    subject_code = models.CharField(max_length=10, primary_key=True)
    subject_div = models.CharField(max_length=10, choices=COURSE_DIV_CHOICES)
    subject_name = models.CharField(max_length=100)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    classroom = models.CharField(max_length=50)

    def __str__(self):
        return self.subject_name

class Enrollment(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.CharField(max_length=20)
    grade = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'{self.student.user.username} - {self.subject.subject_name} ({self.semester})'