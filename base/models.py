from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
# Create your models here.




class Announcement(models.Model):
    title = models.CharField(max_length=100, blank=False)
    text = models.TextField(max_length=300)
    date_posted = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title



class NoticeBoard(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notices',
        verbose_name=_('author')
    )
    subject_code = models.CharField(
        max_length=10,
        blank=False,
        verbose_name=_('subject code')
    )
    title = models.CharField(
        max_length=100,
        blank=False,
        verbose_name=_('title')
    )
    text = models.TextField(
        verbose_name=_('text')
    )
    date_posted = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('date posted')
    )

    class Meta:
        # abstract = True
        verbose_name = _('notice board')
        verbose_name_plural = _('notice boards')

    def __str__(self) -> str:
        return self.title



# class TimeTable(models.Model):
#     course = models.ForeignKey('courses.course', on_delete=models.CASCADE)
#
#     SUNDAY = 0
#     MONDAY = 1
#     TUESDAY = 2
#     WEDNESDAY = 3
#     THURSDAY = 4
#     FRIDAY = 5
#     SATURDAY = 6
#
#     day_choices = [
#         (SUNDAY, 'Sunday'),
#         (MONDAY, 'Monday'),
#         (TUESDAY, 'Tuesday'),
#         (WEDNESDAY, 'Wednesday'),
#         (THURSDAY, 'Thursday'),
#         (FRIDAY, 'Friday'),
#         (SATURDAY, 'Saturday'),
#     ]
#
#     day = models.PositiveSmallIntegerField(
#         choices=day_choices,
#         blank=False
#     )
#
#     start_time = models.TimeField()
#     end_time = models.TimeField()
#
#     class Meta:
#         verbose_name_plural = "time table"