from rest_framework import serializers
from .models import Enrollment, Subject

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'



class EnrollmentSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()
    class Meta:
        model = Enrollment
        fields = '__all__'