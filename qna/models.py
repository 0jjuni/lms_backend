from django.db import models
from django.utils import timezone

from base.models import NoticeBoard
from secure_entry.models import User
# Create your models here.

class Question(NoticeBoard):
    author = models.ForeignKey(User, on_delete=models.CASCADE,)

    public = 0
    private = 1

    #공개 여부 선택지 리스트
    public_private =[
        (public, 'public'),
        (private, 'private')
    ]
    #공개 여부 필드 정의
    status = models.IntegerField(choices=public_private, default=public)

    def __str__(self):
        return self.title

    #수정시 자동 시간 갱신
    def save(self, *args, **kwargs):
        self.date_posted = timezone.now()  # date_posted 필드를 현재 시간으로 갱신
        super().save(*args, **kwargs)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="qna")
    subject_code = models.CharField(max_length=10, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "qna")
    answer = models.TextField(verbose_name=('text')) #답변
    date_posted = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)  # 수정 날짜 자동 업데이트

    def __str__(self):
        return self.answer
