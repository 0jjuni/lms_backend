from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from .models import User, Student, Professor
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['enrollment_number', 'username']

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

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
        fields = ['enrollment_number', 'username', 'user_type']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data, user_type=User.STUDENT)
        Student.objects.create(user=user)
        return user

class UserProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['enrollment_number', 'username', 'user_type']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data, user_type=User.PROFESSOR)
        Professor.objects.create(user=user)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_new_password = serializers.CharField(write_only=True, required=True)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not check_password(value, user.password):
            raise serializers.ValidationError('기존의 비밀번호가 올바르지 않습니다.')
        return value

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('새로운 비밀번호는 최소한 8자리 이상이어야 합니다.')
        return value

    def validate(self, data):
        new_password = data.get('new_password')
        confirm_new_password = data.get('confirm_new_password')

        self.validate_new_password(new_password)

        if new_password != confirm_new_password:
            raise serializers.ValidationError('새로운 비밀번호와 비밀번호 확인이 일치하지 않습니다.')
        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['enrollment_number', 'username', 'password', 'confirm_password', 'user_type']

    def validate_enrollment_number(self, value):
        if len(value) != 8:
            raise serializers.ValidationError("학번은 8자리여야 합니다.")
        return value

    def validate_username(self, value):
        if not value:
            raise serializers.ValidationError("사용자 이름을 반드시 입력해야 합니다.")
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("비밀번호와 비밀번호 확인이 일치하지 않습니다.")
        return data

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        user_type = validated_data.get('user_type')

        user, created = User.objects.update_or_create(
            enrollment_number=validated_data['enrollment_number'],
            defaults={
                'username': validated_data['username'],
                'user_type': validated_data['user_type'],
            }
        )
        user.set_password(password)
        user.save()

        if user_type == User.STUDENT:
            Student.objects.update_or_create(user=user)
        elif user_type == User.PROFESSOR:
            Professor.objects.update_or_create(user=user)

        return user