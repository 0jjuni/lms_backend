from django.contrib import admin
from .models import Announcement

class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posted')
    list_filter = ('date_posted',)
    search_fields = ('title', 'author__username')

admin.site.register(Announcement, AnnouncementAdmin)
