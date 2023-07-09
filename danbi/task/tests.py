from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import DanbiUser
from common.utils.token import create_access_token, create_user_key
from .models import Team, Task, SubTask
from .views import TeamInfo, ListMyTeamTask, CreateTask, EditMainTask, EditSubTask


class CreateTaskTestCase(APITestCase):
    def setUp(self):
        self.team1 = Team.objects.create(name='땅이')
        self.team2 = Team.objects.create(name='블라블라')
        
        self.user_key = create_user_key()
        self.user = DanbiUser.objects.create(username='danbi', password='password', team=self.team1, user_key=self.user_key)
        self.token = create_access_token(user=self.user)
        
        self.task1 = Task.objects.create(team=self.team1, create_user=self.user, title='Task 1', content='Task 1 Content', is_complete=False)
        self.task2 = Task.objects.create(team=self.team2, create_user=self.user, title='Task 2', content='Task 2 Content', is_complete=False)
        self.subtask1 = SubTask.objects.create(task=self.task1, team=self.team1, is_complete=False, is_delete=False)
        self.subtask2 = SubTask.objects.create(task=self.task1, team=self.team2, is_complete=False, is_delete=False)

    def test_get_team_info(self):
        # url = reverse('team-info')
        response = self.client.get('/team')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_my_team_task(self):
        url = reverse('list-my-team-task')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get('/list')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_task_success(self):
        url = reverse('create-task')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        request_data = {
            "team": str(self.team1.id),
            "title": "New Task",
            "content": "New Task Content",
            "subtasks": [
                {
                    "team": str(self.team1.id),
                    "is_complete": False,
                    "is_delete": False
                },
                {
                    "team": str(self.team2.id),
                    "is_complete": False,
                    "is_delete": False
                }
            ]
        }
        response = self.client.post(url, data=request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_edit_main_task_success(self):
        url = reverse('edit-main-task')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        request_data = {
            'id': self.task1.id,
            'team': str(self.team1.id),
            'title': 'Edited Task',
            'content': 'Edited Task Content',
            'is_complete': False
        }
        response = self.client.put(url, data=request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_sub_task_success(self):
        url = reverse('edit-sub-task')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        request_data = {
            'id': self.task1.id,
            'subtasks': [
                {
                    'id': self.subtask1.id,
                    'team': str(self.team1.id),
                    'is_complete': True,
                    'is_delete': False
                },
                {
                    'id': self.subtask2.id,
                    'team': str(self.team2.id),
                    'is_complete': False,
                    'is_delete': True
                }
            ]
        }
        response = self.client.put(url, data=request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
