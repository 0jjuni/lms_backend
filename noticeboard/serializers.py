from rest_framework import serializers
from .models import base_board

class NoticeBoardSerializer(serializers.ModelSerializer):

    author = serializers.HiddenField(default=serializers.CurrentUserDefault()) #로그인된 사용자 정보 받아옴
    subject_code = serializers.CharField() #프론트에서 data보내주어 자동으로 작성
    title = serializers.CharField()
    text = serializers.CharField()
    date_posted = serializers.DateTimeField(read_only = True)


    class Meta:
        model = base_board
        fields = ('author', 'subject_code', 'title', 'text', 'date_posted')

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

#게시판 정보 직렬화
class NoticeBoardInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = base_board
        fields = [
            'author',
            'title',
            'date_posted',
        ]