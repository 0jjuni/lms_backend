from rest_framework import serializers
from .models import User, Student, Professor
from base.serializers import BatchSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'enrollment_number', 'username']

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    batch = BatchSerializer()

    class Meta:
        model = Student
        fields = '__all__'

class ProfessorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Professor
        fields = '__all__'
