from django.contrib import admin
from .models import Connect, Connect_answer

class ConnectAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'date_posted')
    list_filter = ('status', 'date_posted')
    search_fields = ('title', 'author__username')

class ConnectAnswerAdmin(admin.ModelAdmin):
    list_display = ('author', 'connect', 'subject_code', 'date_posted')
    list_filter = ('date_posted', 'subject_code')
    search_fields = ('author__username', 'subject_code', 'connect__title')

admin.site.register(Connect, ConnectAdmin)
admin.site.register(Connect_answer, ConnectAnswerAdmin)
