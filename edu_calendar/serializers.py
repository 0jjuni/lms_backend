from rest_framework import serializers
from .models import PersonalCalendar

class PersonalCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalCalendar
        fields = '__all__'
        extra_kwargs = {'enrollment_number': {'required': False}}

    def create(self, validated_data):
        # Create without enrollment_number, it will be added in the viewset
        return PersonalCalendar.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Update without enrollment_number, it will be added in the viewset
        validated_data.pop('enrollment_number', None)
        return super().update(instance, validated_data)
