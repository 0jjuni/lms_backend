from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')  # 파일이 업로드될 디렉토리 경로 설정

    def __str__(self):
        return "파일"
