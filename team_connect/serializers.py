from rest_framework import serializers
from noticeboard.serializers import NoticeBoardSerializer
from .models import *
from subject.models import Subject

class ConnectSerializer(NoticeBoardSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    subject_code = serializers.CharField(required=False)
    status = serializers.ChoiceField(choices=Connect.public_private, required=False)
    class Meta(NoticeBoardSerializer.Meta):
        model = Connect
        fields = ('id', 'subject_code', 'status', 'author') + NoticeBoardSerializer.Meta.fields

    #수정 요청시, subject_code수정 불가능
    def __init__(self, *args, **kwargs):
        super(ConnectSerializer, self).__init__(*args, **kwargs)
        if self.context['request'].method in ['PUT', 'PATCH']:
            self.fields['subject_code'].read_only = True

    #질문 게시글 작성
    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        subject_code = validated_data.get('subject_code')
        if not subject_code:
            raise serializers.ValidationError("바디에 subject_code(과목코드)가 없습니다.")

        if not Subject.objects.filter(subject_code=subject_code).exists():
            raise serializers.ValidationError("해당 subject_code(과목코드)가 Subject 테이블에 존재하지 않습니다.")


        validated_data['author'] = user
        validated_data['subject_code'] = subject_code

        if 'status' not in validated_data:
            validated_data['status'] = Connect.recruit
        return super().create(validated_data)

class ConnectAnswerSerializer(serializers.ModelSerializer):
    connect = serializers.PrimaryKeyRelatedField(queryset=Connect.objects.all())
    subject_code = serializers.CharField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    text = serializers.CharField()
    date_posted = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Connect_answer
        fields = [
            "id", "author", "connect", "subject_code", "text", "date_posted"
        ]
        read_only_fields = ['subject_code', 'date_posted']

    def create(self, validated_data):
        request = self.context['request']
        connect = validated_data.get("connect")
        if not connect:
            raise serializers.ValidationError("Body does not contain connect.")

        validated_data['subject_code'] = connect.subject_code
        validated_data['author'] = request.user
        return Connect_answer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance