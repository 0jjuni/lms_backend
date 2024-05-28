from rest_framework import serializers
from noticeboard.serializers import NoticeBoardSerializer
from .models import Announcement
class announcementSerializer(NoticeBoardSerializer):
    subject_code = serializers.CharField(required=False)

    class Meta(NoticeBoardSerializer.Meta):
        model = Announcement
        fields = tuple(NoticeBoardSerializer.Meta.fields)

    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        subject_code = request.headers.get('Subject-Code')
        if not subject_code:
            raise serializers.ValidationError("헤더에 Subject-Code(과목코드)가 없습니다.")


        validated_data['author'] = user
        validated_data['subject_code'] = subject_code
        return super().create(validated_data)