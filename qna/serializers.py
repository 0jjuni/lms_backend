from rest_framework import serializers
from noticeboard.serializers import NoticeBoardSerializer
from .models import Question

#질문 등록 header subject_code이용
class QuestionSerializer(NoticeBoardSerializer):
    subject_code = serializers.CharField(required=False)

    class Meta(NoticeBoardSerializer.Meta):
        model = Question
        fields = tuple(NoticeBoardSerializer.Meta.fields)

    #질문 게시글 작성

    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        subject_code = request.headers.get('Subject-Code')
        if not subject_code:
            raise serializers.ValidationError("헤더에 Subject-Code(과목코드)가 없습니다.")

        validated_data['author'] = user
        validated_data['subject_code'] = subject_code
        return super().create(validated_data)

class QuestionInfoSerializer(NoticeBoardSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Question
        fields = [
            'author',
            'title',
            'status'
        ]
