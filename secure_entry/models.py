from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, enrollment_number, username, password, **extra_fields):
        if not enrollment_number:
            raise ValueError(_("학번을 반드시 입력해야 합니다."))
        if not username:
            raise ValueError(_("사용자 이름을 반드시 입력해야 합니다."))
        if not password:
            raise ValueError(_("비밀번호를 반드시 입력해야 합니다."))

        user = self.model(enrollment_number=enrollment_number, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, enrollment_number, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('user_type', 'A')

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('슈퍼유저는 is_staff=True 이어야 합니다.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('슈퍼유저는 is_superuser=True 이어야 합니다.'))

        return self.create_user(enrollment_number, username, password, **extra_fields)


class User(AbstractUser):
    enrollment_number = models.CharField(max_length=9, unique=True, primary_key=True)
    username = models.CharField(max_length=100, blank=False)

    STUDENT = 'S'
    PROFESSOR = 'P'
    ADMIN = 'A'
    USER_TYPE_CHOICES = (
        (STUDENT, 'Student'),
        (PROFESSOR, 'Professor'),
        (ADMIN, 'Admin'),
    )
    user_type = models.CharField(
        max_length=1,
        choices=USER_TYPE_CHOICES,
        default=STUDENT
    )
    groups = models.ManyToManyField(
        Group,
        related_name='secure_entry_user_groups',
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        verbose_name=_('groups')
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='secure_entry_user_permissions',
        blank=True,
        help_text=_('Specific permissions for this user.'),
        verbose_name=_('user permissions')
    )

    USERNAME_FIELD = 'enrollment_number'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def save(self, *args, **kwargs):
        creating = self._state.adding
        super().save(*args, **kwargs)
        if creating:
            if self.user_type == self.STUDENT:
                Student.objects.get_or_create(user=self)
            elif self.user_type == self.PROFESSOR:
                Professor.objects.get_or_create(user=self)

    def __str__(self):
        return self.username

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self) -> str:
        return f'{self.user.username}'

class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self) -> str:
        return f'{self.user.username}'
