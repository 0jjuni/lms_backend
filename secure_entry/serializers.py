from .models import User, Student, Professor
from base.serializers import BatchSerializer
from rest_framework import serializers
from django.contrib.auth.hashers import check_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'enrollment_number', 'username']

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    #batch = BatchSerializer()

    class Meta:
        model = Student
        fields = '__all__'

class ProfessorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Professor
        fields = '__all__'


class UserStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'enrollment_number', 'username', 'user_type']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data, user_type=User.STUDENT)
        Student.objects.create(user=user)
        return user

class UserProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'enrollment_number', 'username', 'user_type']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data, user_type=User.PROFESSOR)
        Professor.objects.create(user=user)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, min_length=8)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not check_password(value, user.password):
            raise serializers.ValidationError('기존의 비밀번호가 올바르지 않습니다.')
        return value

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('새로운 비밀번호는 최소한 8자리 이상이어야 합니다.')
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
