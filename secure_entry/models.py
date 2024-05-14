from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from base.models import Batch

class UserManager(BaseUserManager):
    def create_user(self, enrollment_number, username, password, **extra_fields):
        if not enrollment_number:
            raise ValueError(_("The Enrollment Number must be set"))
        user = self.model(enrollment_number=enrollment_number, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, enrollment_number, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(enrollment_number, username, password, **extra_fields)

class User(AbstractUser):
    enrollment_number = models.CharField(max_length=9, unique=True)
    username = models.CharField(max_length=100, blank=False)

    STUDENT = 'S'
    PROFESSOR = 'P'

    USER_TYPE_CHOICES = (
        (STUDENT, 'Student'),
        (PROFESSOR, 'Professor'),
    )

    user_type = models.CharField(
        max_length=1,
        choices=USER_TYPE_CHOICES,
        default=STUDENT
    )

    groups = models.ManyToManyField(
        Group,
        related_name='secure_entry_user_groups',  # related_name 추가
        blank=True,
        help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        verbose_name=_('groups')
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='secure_entry_user_permissions',  # related_name 추가
        blank=True,
        help_text=_('Specific permissions for this user.'),
        verbose_name=_('user permissions')
    )

    USERNAME_FIELD = 'enrollment_number'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f'{self.user.username}'

class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self) -> str:
        return f'{self.user.username}'
