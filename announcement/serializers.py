from rest_framework import serializers
from noticeboard.serializers import NoticeBoardSerializer
from .models import Announcement
from subject.models import Subject
class AnnouncementSerializer(NoticeBoardSerializer):
    subject_code = serializers.CharField(required=False)

    class Meta(NoticeBoardSerializer.Meta):
        model = Announcement
        fields = ('id',) + tuple(NoticeBoardSerializer.Meta.fields)

    def __init__(self, *args, **kwargs):
        super(AnnouncementSerializer, self).__init__(*args, **kwargs)
        # 수정 요청인 경우 subject_code 필드를 읽기 전용으로 설정
        if self.context['request'].method in ['PUT', 'PATCH']:
            self.fields['subject_code'].read_only = True

    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        if user.user_type == 'S':
            raise serializers.ValidationError("학생계정은 공지사항 작성이 불가능 합니다.")

        subject_code = validated_data.get('subject_code')
        if not subject_code:
            raise serializers.ValidationError("Body에 subject_code(과목코드)가 없습니다.")

        # Subject_table subject_code 확인
        if not Subject.objects.filter(subject_code=subject_code).exists():
            raise serializers.ValidationError("해당 subject_code(과목코드)가 Subject 테이블에 존재하지 않습니다.")


        validated_data['author'] = user
        validated_data['subject_code'] = subject_code
        return super().create(validated_data)

class AnnouncementInfo(NoticeBoardSerializer):
    class Meta:
        model = Announcement
        fields = "__all__"