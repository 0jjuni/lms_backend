from django.db import models
from django.utils import timezone
from base.models import NoticeBoard
from secure_entry.models import User
# Create your models here.

class lecture(NoticeBoard):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lecture_note')
    upload = models.FileField(upload_to="C:/Users/kilho/Documents/asyouwrite", null=True, blank=True) # 업로드 파일 경로 지정필요

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.date_posted = timezone.now()
        super().save(*args, **kwargs)

