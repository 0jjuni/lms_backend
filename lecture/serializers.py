from rest_framework import serializers
from noticeboard.serializers import NoticeBoardSerializer
from .models import lecture
from subject.models import Subject
class LectureSerializer(NoticeBoardSerializer):
    upload = serializers.FileField(required=False, allow_empty_file=True, allow_null=True)
    subject_code = serializers.CharField(required=True)

    class Meta(NoticeBoardSerializer.Meta):
        model = lecture
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(LectureSerializer, self).__init__(*args, **kwargs)
        # 수정 요청인 경우 subject_code 필드를 읽기 전용으로 설정
        if self.context['request'].method in ['PUT', 'PATCH']:
            self.fields['subject_code'].read_only = True

    def create(self, validated_data):
        request = self.context['request']
        user = request.user


        subject_code = validated_data.get('subject_code')
        if not subject_code:
            raise serializers.ValidationError("Body에 subject_code(과목코드)가 없습니다.")

        # Subject 테이블에서 subject_code 확인
        if not Subject.objects.filter(subject_code=subject_code).exists():
            raise serializers.ValidationError("해당 subject_code(과목코드)가 Subject 테이블에 존재하지 않습니다.")


        validated_data['author'] = user
        validated_data['subject_code'] = subject_code

        return super().create(validated_data)

class LectureInfo(NoticeBoardSerializer):
    class Meta:
        model = lecture
        fields = "__all__"
