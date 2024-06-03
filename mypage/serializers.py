from homework.models import Register
from rest_framework import serializers
from announcement.models import Announcement

class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = ['id', 'title', 'text', 'date_posted', 'due_date', 'upload', 'subject_code']


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id', 'title', 'text', 'date_posted', 'subject_code']