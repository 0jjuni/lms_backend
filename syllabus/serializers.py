from rest_framework import serializers
from .models import Syllabus
from subject.models import Subject
#강의자료 생성
class SyllabusSerialziers(serializers.ModelSerializer):
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
        super(SyllabusSerialziers, self).__init__(*args, **kwargs)
        # 수정 요청인 경우 subject_code 필드를 읽기 전용으로 설정
        if self.context['request'].method in ['PUT', 'PATCH']:
            self.fields['subject_code'].read_only = True

    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        if user and hasattr(Syllabus, 'author'):
            validated_data['author'] = user

        return super().create(validated_data)

    def validate(self, data):
        if 'subject_code' not in data:
            raise serializers.ValidationError({"subject_code": "Body에 subject_code(과목코드)가 없습니다."})
        return data
