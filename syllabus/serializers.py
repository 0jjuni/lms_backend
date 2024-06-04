from rest_framework import serializers
from .models import Syllabus
from subject.models import Subject
from subject.serializers import SubjectSerializer
#강의자료 생성
class SyllabusSerializer(serializers.ModelSerializer):
    subject_code = serializers.SlugRelatedField(
        slug_field='subject_code',  # Subject 모델에서 subject_code 필드를 찾기 위한 키
        queryset=Subject.objects.all(),
        error_messages={
            'does_not_exist': '입력한 subject_code(과목코드) {value}는 유효하지 않습니다.'
        }
    )

    class Meta:
        model = Syllabus
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SyllabusSerializer, self).__init__(*args, **kwargs)
        # 수정 요청인 경우 subject_code 필드를 읽기 전용으로 설정
        if self.context['request'].method in ['PUT', 'PATCH']:
            self.fields['subject_code'].read_only = True

    def validate(self, data):
        request_method = self.context['request'].method
        subject_code = data.get('subject_code')

        if request_method in ['POST'] and not subject_code:
            raise serializers.ValidationError({"subject_code": "Body에 subject_code(과목코드)가 없습니다."})

        # 생성 요청인 경우에만 중복 확인
        if request_method == 'POST' and Syllabus.objects.filter(subject_code=subject_code).exists():
            raise serializers.ValidationError({"subject_code": "해당 subject_code(과목코드)로 이미 Syllabus가 존재합니다."})

        return data
class SyllabusInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Syllabus
        fields = '__all__'

class TotalSyllabusSerializer(serializers.Serializer):
    subject = SubjectSerializer()
    syllabus = SyllabusInfoSerializer()