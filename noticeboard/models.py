from django.db import models
from base.models import NoticeBoard
from secure_entry.models import User


# Create your models here.
class base_board(NoticeBoard):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='baseboard_posts')
    pass