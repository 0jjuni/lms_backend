from rest_framework import serializers
from .models import TeamRecruitment


class TeamRecruitmentSerializer(serializers.ModelSerializer):
    # 기본값으로 "모집중" 설정
    recruitment_status = serializers.CharField(default="모집중")

    class Meta:
        model = TeamRecruitment
        fields = ['id', 'title', 'content', 'team_size', 'kakao_openlink', 'publication_date', 'deadline', 'recruitment_status']
        read_only_fields = ['id']

    def create(self, validated_data):
        # 여기서 recruitment_status에 대한 처리를 제거
        return TeamRecruitment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.team_size = validated_data.get('team_size', instance.team_size)
        instance.kakao_openlink = validated_data.get('kakao_openlink', instance.kakao_openlink)
        instance.deadline = validated_data.get('deadline', instance.deadline)

        # recruitment_status 업데이트
        if 'recruitment_status' in validated_data:
            instance.recruitment_status = validated_data['recruitment_status']

        instance.save()
        return instance
