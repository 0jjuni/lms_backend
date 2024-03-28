from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

class ChangePasswordTestCase(TestCase):
    def setUp(self):
        # 테스트용 사용자 생성
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='old_password')
        self.client = APIClient()
        # 인증된 사용자로 테스트 클라이언트 설정
        self.client.force_authenticate(user=self.user)

    def test_change_password(self):
        # 비밀번호 변경 요청 URL. 여기서는 사용자 ID를 URL 경로에 포함시키고 있습니다.
        url = reverse('auth_change_password', kwargs={'pk': self.user.pk})
        # 비밀번호 변경 요청 데이터
        data = {
            'old_password': 'old_password',
            'password': 'new_password',
            'password2': 'new_password',
        }
        # 비밀번호 변경 요청 실행
        response = self.client.put(url, data)
        # 응답 상태 코드 검증
        self.assertEqual(response.status_code, status.HTTP_200_OK)