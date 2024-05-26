from django.db.migrations import serializer
from rest_framework import serializers
from noticeboard.serializers import NoticeBoardSerializer
from .models import Register, Submission


# NoticeBoard직렬화 상속
class registerSerializer(NoticeBoardSerializer):
    due_date = serializers.DateTimeField()
    upload = serializers.FileField(required=False, allow_empty_file=True, allow_null=True)
    subject_code = serializers.CharField(required=False)
    class Meta(NoticeBoardSerializer.Meta):
        model = Register
        fields = tuple(NoticeBoardSerializer.Meta.fields) + ('due_date', 'upload',)

    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        #과제등록 권한설정
        if user.user_type != 'P':
            raise serializers.ValidationError("과제등록은 교수님만 가능합니다.")
        #헤더에서 subject_code가져옴
        subject_code = request.headers.get('Subject-Code')
        if not subject_code:
            raise serializers.ValidationError("헤더에 Subject-Code(과목코드)가 없습니다.")

        # try:
        #     assignment = Register.objects.get(pk=subject_code) #학생 수강 과목 DB생성 후 제작하기
        # except Register.DoesNotExist:
        #     raise serializers.ValidationError("해당 과목를 찾을 수 없습니다.")


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
        fields = [
            'author',
            'title',
            'due_date'
                  ]

class submissiontSerializer(NoticeBoardSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    assignment = serializers.PrimaryKeyRelatedField(read_only=True)
    subject_code = serializers.CharField(read_only=True)
    class Meta:
        model = Submission
        fields = ['id', 'assignment', 'author', 'subject_code', 'title', 'text', 'date_posted', 'upload']
        read_only_fields = ['subject_code', 'date_posted']

    def create(self, validated_data):
        request = self.context['request']
        #http헤더 assignment정보 받아오기
        assignment_id = request.headers.get('Assignment')
        if not assignment_id:
            raise serializers.ValidationError("헤더에 assignment가 없습니다.")

        try:
            assignment = Register.objects.get(pk=assignment_id)
        except Register.DoesNotExist:
            raise serializers.ValidationError("해당 과제를 찾을 수 없습니다.")

        validated_data['assignment'] = assignment
        validated_data['subject_code'] = assignment.subject_code
        validated_data['author'] = request.user

        return super().create(validated_data)

class submissionUpdateSerializer(NoticeBoardSerializer):
    class Meta:
        model = Submission
        fields = ['title', 'text', 'upload', 'date_posted']
        read_only_fields = ['date_posted']