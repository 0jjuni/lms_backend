from rest_framework import serializers
from noticeboard.serializers import NoticeBoardSerializer
from .models import Question, Answer

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



# 질문 답변 header question요청
class AnswerSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(read_only=True)
    subject_code = serializers.CharField(read_only=True)
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    answer = serializers.CharField()
    date_posted = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Answer
        fields = [
            "id", "question", "subject_code", "author", "answer", "date_posted"
        ]
        read_only_fields = ['subject_code', 'date_posted']

    def create(self, validated_data):
        request = self.context['request']

        #교수님 답변
        if request.user.user_type != 'P':
            raise serializers.ValidationError("답변은 교수님만 가능합니다.")

        question_id = request.headers.get("question")
        # 프론트 요청시 헤더 question ID입력하기
        if not question_id:
            raise serializers.ValidationError("헤더에 question이 없습니다.")

        try:
            question = Question.objects.get(pk=question_id)
        except Answer.DoesNotExist:
            raise serializers.ValidationError("해당 질문을 찾을 수 없습니다.")

        validated_data['question'] = question
        validated_data['subject_code'] = question.subject_code
        validated_data['author'] = request.user

        return super().create(validated_data)


