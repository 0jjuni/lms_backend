from django.db import models
from rest_framework.fields import DateTimeField

from base.models import NoticeBoard
from secure_entry.models import User


# Create your models here.
#과제등록
class Register(NoticeBoard):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='homework_registers')
    due_date = models.DateTimeField(null=True, blank=True) #마감시간
    upload = models.FileField(upload_to="C:/Users/kilho/Documents/asyouwrite", null=True, blank=True) # 업로드 파일 경로 지정필요

    def __str__(self):
        return self.title

#과제제출
class Submission(NoticeBoard):
    assignment = models.ForeignKey(Register, on_delete=models.CASCADE, related_name="submission") #register(과제등록 연결)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submission") #user(사용자 연결)
    upload = models.FileField(upload_to="C:/Users/kilho/Documents/asyouwrite", null=True, blank=True)  # 업로드 파일 경로 지정필요

    def save(self, *args, **kwargs):
        if not self.subject_code:
            self.subject_code = self.assignment.subject_code
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title