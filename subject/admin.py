from django.contrib import admin
from .models import Subject, Enrollment

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_code', 'subject_name', 'subject_div', 'professor', 'classroom')
    search_fields = ('subject_code', 'subject_name', 'professor__name')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'student', 'semester', 'grade')
    search_fields = ('subject__subject_name', 'student__user__username', 'semester')
    list_filter = ('semester', 'subject__subject_div')