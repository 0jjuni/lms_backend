from django.db import models
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

