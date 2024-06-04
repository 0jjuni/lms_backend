from django.db import models
from subject.models import Subject
# Create your models here.

class Syllabus(models.Model):
    subject_code = models.OneToOneField(Subject, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.title