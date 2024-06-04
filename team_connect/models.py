from django.db import models
from base.models import NoticeBoard
from secure_entry.models import User
from django.utils import timezone
# Create your models here.

class Connect(NoticeBoard):
    author = models.ForeignKey(User, on_delete=models.CASCADE, )

    recruit = 0
    fin_recruit = 1

    # 모집 여부
    public_private = [
        (recruit, '모집중'),
        (fin_recruit, '모집완료')
    ]

    # 모집상태 필즈 저의
    status = models.IntegerField(choices=public_private, default=recruit)

    def __str__(self):
        return self.title

        # 수정시 자동 시간 갱신
    def save(self, *args, **kwargs):
        self.date_posted = timezone.now()  # date_posted 필드를 현재 시간으로 갱신
        super().save(*args, **kwargs)


class Connect_answer(models.Model):
    connect = models.ForeignKey(Connect, on_delete=models.CASCADE, related_name="connect")
    subject_code = models.CharField(max_length=10, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE,)
    text = models.TextField(verbose_name=('text')) # 자기 소개
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.answer