from rest_framework import serializers
from base.models import NoticeBoard

class NoticeBoardSerializer(serializers.ModelSerializer):

    # author = serializers.CharField() # userModel, 혹은 로그인된 사용자 ID 받아오기
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # subject_code = serializers.CharField() #글을 작성한 위치에 따라 자동으로 채우도록
    subject_code = serializers.CharField() #수정 필요함
    title = serializers.CharField()
    text = serializers.CharField()
    date_posted = serializers.DateTimeField(read_only = True)


    class Meta:
        model = NoticeBoard
        fields = '__all__'

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        validated_data['subject_code'] = 1 #차후 수정진행
        return super().create(validated_data)

#게시판 정보 직렬화
class NoticeBoardInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeBoard
        fields = [
            'author',
            'title',
            'date_posted',
        ]