from rest_framework import serializers
from .models import PersonalCalendar

class PersonalCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalCalendar
        fields = '__all__'
