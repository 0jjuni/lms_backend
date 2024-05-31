from rest_framework import serializers
from noticeboard.serializers import NoticeBoardSerializer
from .models import Question, Answer
from subject.models import Subject

#질문 등록
class QuestionSerializer(NoticeBoardSerializer):
    subject_code = serializers.CharField(required=False)
    status = serializers.ChoiceField(choices=Question.public_private, required=False)
    class Meta(NoticeBoardSerializer.Meta):
        model = Question
        fields = tuple(NoticeBoardSerializer.Meta.fields) + ('subject_code', 'status')

    #수정 요청시, subject_code수정 불가능
    def __init__(self, *args, **kwargs):
        super(QuestionSerializer, self).__init__(*args, **kwargs)
        if self.context['request'].method in ['PUT', 'PATCH']:
            self.fields['subject_code'].read_only = True

    #질문 게시글 작성
    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        subject_code = validated_data.get('subject_code')
        if not subject_code:
            raise serializers.ValidationError("바디에 subject_code(과목코드)가 없습니다.")

        # Subject 테이블에서 subject_code 확인
        # + Enrollment 테이블에서 subject_code 확인 기능 추가 하기
        if not Subject.objects.filter(subject_code=subject_code).exists():
            raise serializers.ValidationError("해당 subject_code(과목코드)가 Subject 테이블에 존재하지 않습니다.")


        validated_data['author'] = user
        validated_data['subject_code'] = subject_code

        if 'status' not in validated_data:
            validated_data['status'] = Question.public
        return super().create(validated_data)

class QuestionInfoSerializer(NoticeBoardSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Question
        fields = '__all__'



# 질문 답변 Body question요청
class AnswerSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
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

        #body question 요청
        question  = validated_data.get("question")
        if not question :
            raise serializers.ValidationError("Body에 question_id이 없습니다.")

        try:
            question = Question.objects.get(pk=question.id)
        except Question.DoesNotExist:
            raise serializers.ValidationError("해당 질문을 찾을 수 없습니다.")

        validated_data['question'] = question
        validated_data['subject_code'] = question.subject_code
        validated_data['author'] = request.user

        return super().create(validated_data)

class AnswerInfoSerializer(serializers.ModelSerializer):
    question = serializers.StringRelatedField()

    class Meta:
        model = Answer
        fields = '__all__'
