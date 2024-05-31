from django.db.migrations import serializer
from rest_framework import serializers
from noticeboard.serializers import NoticeBoardSerializer
from .models import Register, Submission
from subject.models import Subject


# NoticeBoard직렬화 상속
class registerSerializer(NoticeBoardSerializer):
    due_date = serializers.DateTimeField()
    upload = serializers.FileField(required=False, allow_empty_file=True, allow_null=True)
    subject_code = serializers.CharField(required=False)
    class Meta(NoticeBoardSerializer.Meta):
        model = Register
        fields = tuple(NoticeBoardSerializer.Meta.fields) + ('due_date', 'upload','subject_code',)

    def __init__(self, *args, **kwargs):
        super(registerSerializer, self).__init__(*args, **kwargs)
        # 수정 요청인 경우 subject_code 필드를 읽기 전용으로 설정
        if self.context['request'].method in ['PUT', 'PATCH']:
            self.fields['subject_code'].read_only = True

    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        #과제등록 권한설정
        if user.user_type != 'P':
            raise serializers.ValidationError("과제등록은 교수님만 가능합니다.")

        subject_code = validated_data.get('subject_code')
        if not subject_code:
            raise serializers.ValidationError("Body에 subject_code(과목코드)가 없습니다.")

        # Enrollment 테이블에서 subject_code 확인
        if not Subject.objects.filter(subject_code=subject_code).exists():
            raise serializers.ValidationError("해당 subject_code(과목코드)가 Subject 테이블에 존재하지 않습니다.")


        validated_data['author'] = user
        validated_data['subject_code'] = subject_code
        return super().create(validated_data)

    # 마감날짜 확인
    def validate_due_date(self, value):
        from django.utils import timezone
        if value < timezone.now():
            raise serializers.ValidationError("날짜를 다시 설정해주세요")
        return value

class registeInfoSerializer(NoticeBoardSerializer):
    author = serializers.StringRelatedField()
    class Meta:
        model = Register
        fields = '__all__'

#과제제출
class submissiontSerializer(NoticeBoardSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    assignment = serializers.PrimaryKeyRelatedField(queryset=Register.objects.all())

    subject_code = serializers.CharField(read_only=True)
    class Meta:
        model = Submission
        fields = ['id', 'assignment', 'author', 'subject_code', 'title', 'text', 'date_posted', 'upload']
        read_only_fields = ['subject_code', 'date_posted']

    def create(self, validated_data):
        request = self.context['request']

        assignment_id = validated_data.get('assignment')

        if not assignment_id:
            raise serializers.ValidationError("Body에 assignment_id(과제ID)가 없습니다.")

        try:
            assignment = Register.objects.get(pk=assignment_id.id)
        except Register.DoesNotExist:
            raise serializers.ValidationError("해당 과제를 찾을 수 없습니다.")

        validated_data['assignment'] = assignment
        validated_data['subject_code'] = assignment.subject_code
        validated_data['author'] = request.user

        return super().create(validated_data)

class submissionInfoSerializer(NoticeBoardSerializer):
    class Meta:
        model = Register
        fields = '__all__'

class submissionUpdateSerializer(NoticeBoardSerializer):
    class Meta:
        model = Submission
        fields = ['title', 'text', 'upload', 'date_posted']
        read_only_fields = ['date_posted']