from django.db import models
from django.conf import settings

class TeamRecruitment(models.Model):
    # 사용자 모델에 대한 외래 키 추가, null 허용
    userid = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,  # null 허용
        blank=True,  # 폼에서 빈값 허용
        default=None,  # 기본값으로 None 설정
    )

    # Course_name에 대한 외래 키 추가, null 허용
    course_name = models.ForeignKey(
        'sugang_register.TotalLecture',
        on_delete=models.CASCADE,
        null=True,  # null 허용
        blank=True,  # 폼에서 빈값 허용
        default=None,  # 기본값으로 None 설정
        db_column='Course_Name',  # 실제 DB에서 사용하는 컬럼 이름을 명시합니다. 이 부분은 필드 정의에 필요하지 않을 수 있습니다.
    )

    title = models.CharField(max_length=100)
    content = models.TextField()
    team_size = models.PositiveIntegerField()
    kakao_openlink = models.CharField(max_length=255)
    publication_date = models.DateField(auto_now_add=True)
    deadline = models.DateField(null=True, blank=True, auto_now_add=False)
    recruitment_status = [
        ('모집중', '모집중'),
        ('모집완료', '모집완료'),
    ]

    class Meta:
         # user 필드와 course_name 필드의 조합이 유니크해야 함을 지정합니다.
         unique_together = [['userid', 'course_name']]