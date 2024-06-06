from django.contrib import admin
from .models import Register, Submission

class RegisterAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'due_date', 'file_type', 'date_posted')
    list_filter = ('file_type', 'due_date', 'date_posted')
    search_fields = ('title', 'author__username')

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'assignment', 'author', 'date_posted')
    list_filter = ('assignment', 'date_posted')
    search_fields = ('title', 'author__username', 'assignment__title')

admin.site.register(Register, RegisterAdmin)
admin.site.register(Submission, SubmissionAdmin)
