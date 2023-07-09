from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from .views import Signup, SignIn
from task.models import Team
from user.models import DanbiUser

class SignupTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        task1 = Team.objects.create(name="땅이") 
        task2 = Team.objects.create(name="블라블라") 
        user = DanbiUser.objects.create(username="danbi", team="땅이", password="1q2w3e4r") 

    #signup
    def test_signup_success(self):
        request_data = {
            'name': 'user1',
            'team': '땅이',
            'password': '1q2w3e4r'
        }
        request = self.factory.post('/signup/', data=request_data)
        response = Signup.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_duplicate_name(self):
        request_data = {
            'name': 'danbi',
            'team': '땅이',
            'password': '1ㅂ2ㅈ3ㄷ4ㄱ'
        }
        request = self.factory.post('/signup/', data=request_data)
        response = Signup.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_not_exist_team(self):
        request_data = {
            'name': 'user1',
            'team': 'team123',
            'password': '1q2w3e4r'
        }
        request = self.factory.post('/signup/', data=request_data)
        response = Signup.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    #signin
    def test_signin_success(self):
        request_data = {
            'name': 'danbi',
            'password': '1q2w3e4r',
            'team' : '땅이'
        }
        request = self.factory.post('/signin/', data=request_data)
        response = SignIn.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Token', response.data)

    def test_signin_invalid_user(self):
        request_data = {
            'name': 'test',
            'password': '1q2w3e4r',
            'team' : '땅이'
        }
        request = self.factory.post('/signin/', data=request_data)
        response = SignIn.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_signin_invalid_password(self):
        request_data = {
            'name': 'danbi',
            'password': '123123123123',
            'team' : '땅이'
        }
        request = self.factory.post('/signin/', data=request_data)
        response = SignIn.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)