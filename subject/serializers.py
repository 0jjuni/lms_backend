from rest_framework import serializers
from .models import Enrollment, Subject

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['subject_code', 'subject_name', 'subject_div', 'professor', 'classroom']



class EnrollmentSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()
    class Meta:
        model = Enrollment
        fields = '__all__'