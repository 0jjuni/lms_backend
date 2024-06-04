from rest_framework import serializers
from .models import Syllabus
from subject.models import Subject
class SyllabusSerialziers(serializers.Serializer):
    class Meta:
        model = Syllabus
        fields = '__all__'
        read_only_fields = ['subject_code', ]

    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        subject_code = validated_data.get('subject_code')
        if not subject_code:
            raise serializers.ValidationError("Body에 subject_code(과목코드)가 없습니다.")

        # Subject 테이블에서 subject_code 확인
        if not Subject.objects.filter(subject_code=subject_code).exists():
            raise serializers.ValidationError("해당 subject_code(과목코드)가 Subject 테이블에 존재하지 않습니다.")
