from homework.models import Register
from rest_framework import serializers

class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = ['id', 'title', 'text', 'date_posted', 'due_date', 'upload', 'subject_code']