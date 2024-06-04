from django.db import models
from subject.models import Subject
# Create your models here.

class Syllabus(models.Model):
    subject_code = models.ForeignKey(Subject, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    context = models.TextField()

    def __str__(self):
        return self.title
