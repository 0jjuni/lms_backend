from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Student, Professor

class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('enrollment_number', 'password')}),
        ('Personal info', {'fields': ('username',)}),
        ('User type', {'fields': ('user_type',)}),  # user_type 필드 추가
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('enrollment_number', 'username', 'user_type', 'password1', 'password2'),
        }),
    )
    list_display = ('enrollment_number', 'username', 'user_type', 'is_staff')
    search_fields = ('enrollment_number', 'username')
    ordering = ('enrollment_number',)
    filter_horizontal = ('groups', 'user_permissions')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user',)# 'batch')
    search_fields = ('user__username',)# 'batch__name')

class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Professor, ProfessorAdmin)
