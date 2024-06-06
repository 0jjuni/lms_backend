from django.contrib import admin
from .models import Question, Answer

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'date_posted')
    list_filter = ('status', 'date_posted')
    search_fields = ('title', 'author__username')

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'subject_code', 'author', 'date_posted', 'date_modified')
    list_filter = ('date_posted', 'subject_code', 'date_modified')
    search_fields = ('author__username', 'subject_code', 'question__title', 'answer')

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
