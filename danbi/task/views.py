from datetime import datetime

from django.http.response import JsonResponse
from django.core.exceptions import ValidationError 
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.serializers import ValidationError

from .models import Team, Task, SubTask
from .serializers import TaskSerializer, TeamSerializer, MainTaskSerializer
from user.models import DanbiUser
from common.utils.token import user_check


class TeamInfo(APIView):
    def get(self, request):
        try:
            teams = Team.objects.all()
            serializer = TeamSerializer(teams, many=True)
            return JsonResponse({'data': serializer.data}, status=status.HTTP_200_OK)

        except KeyError as e:
            return JsonResponse({'KeyError' : f'{e}'}, status=status.HTTP_400_BAD_REQUEST)

        except ValueError as e:
            return JsonResponse({'ValueError' : f'{e}'}, status=status.HTTP_400_BAD_REQUEST)


class ListMyTeamTask(APIView):
    def get(self, request):
        try:
            auth_header = request.headers.get('Authorization')
            request_user = user_check(auth_header)

            subtasks = SubTask.objects.filter(team=request_user.team)
            user_task = Task.objects.filter(subtask__in=subtasks).distinct()

            data = [{
                'id' : task.id,
                'team' : task.team,
                'title' : task.title,
                'content' : task.content,
                'is_complete' : task.is_complete,
                'subtasks' :[{
                    "id" : sub.id,
                    "team": sub.team,
                    "is_complete": sub.is_complete,
                    "is_delete" : sub.is_delete
                } for sub in task.subtask_set.all()]
            } for task in user_task]
        
            return JsonResponse({'message': data}, status=200)            

        except KeyError as e:
            return JsonResponse({'KeyError' : f'{e}'}, status=status.HTTP_400_BAD_REQUEST)

        except ValueError as e:
            return JsonResponse({'ValueError' : f'{e}'}, status=status.HTTP_400_BAD_REQUEST)


class CreateTask(APIView):
    def post(self, request):
        try:
            auth_header = request.headers.get('Authorization')
            request_user = user_check(auth_header)
            team = Team.objects.all().values_list('name', flat=True)

            if not request.data['team'] or request.data['team'] not in team:
                return JsonResponse({'error': 'Not Exist Team'}, status=status.HTTP_400_BAD_REQUEST)

            if not request.data['subtasks'] or len(request.data['subtasks']) == 0:
                return JsonResponse({'error': 'Sub Task Null'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = TaskSerializer.create(user=request_user,validated_data=request.data)

            return JsonResponse({'message': "success"}, status=status.HTTP_201_CREATED)

        except KeyError as e:
            return JsonResponse({'KeyError': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)

        except ValueError as e:
            return JsonResponse({'ValueError': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)


class EditMainTask(APIView):
    def put(self, request):
        try:
            auth_header = request.headers.get('Authorization')
            request_user = user_check(auth_header)
            
            task = get_object_or_404(Task, id=request.data['id'])
            team = Team.objects.all().values_list('name', flat=True)

            if request.data['team'] not in team:
                return JsonResponse({'error': 'Not Exist Team'}, status=status.HTTP_400_BAD_REQUEST)

            if task.create_user != request_user:
                return JsonResponse({'error': 'Not Match Team'}, status=status.HTTP_400_BAD_REQUEST)

            Task.objects.filter(id=request.data['id']).update(
                title = request.data['title'],
                content = request.data['content'],
                is_complete = request.data['is_complete']
            )
            return JsonResponse({'message': "success"}, status=status.HTTP_200_OK)

        except KeyError as e:
            return JsonResponse({'KeyError': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)

        except ValueError as e:
            return JsonResponse({'ValueError': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)


class EditSubTask(APIView):
    def put(self, request):
        try:
            auth_header = request.headers.get('Authorization')
            request_user = user_check(auth_header)
            task = get_object_or_404(Task, id=request.data['id'])
            team = Team.objects.all().values_list('name', flat=True)

            all_subtask = SubTask.objects.filter(task=task)
            for subtask_data in request.data['subtasks']:
                if subtask_data['team'] not in team:
                    raise ValidationError({'error': 'Not Exist Team'})
                
                subtask = all_subtask.filter(id=subtask_data['id'])
                if subtask:
                    if not subtask.first().is_complete and not subtask.first().is_delete:
                        if subtask_data['is_complete']:
                            if request_user.team != subtask_data['team']:
                                raise ValidationError('Not Match Team')
                            else:
                                subtask.update(
                                    is_complete=subtask_data['is_complete'],
                                    completed_date=datetime.now()
                                )
                        else:
                            if task.create_user != request_user:
                               raise ValidationError('Not Match Team') 
                            else:
                                subtask.update(
                                    team=subtask_data['team'],
                                )
                    if subtask_data['is_delete']:
                        if subtask.first().is_complete:
                            pass
                        else:
                            if task.create_user != request_user:
                               raise ValidationError('Not Match Team') 
                            else:
                                subtask.delete()
            subtask_is_complete = all_subtask.values_list('is_complete', flat=True)
            if all(subtask_is_complete):
                task.is_complete = True
                completed_date=datetime.now()

            return JsonResponse({'message': "success"}, status=status.HTTP_200_OK)

        except KeyError as e:
            return JsonResponse({'KeyError': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)

        except ValueError as e:
            return JsonResponse({'ValueError': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)
        
        except ValidationError as e:
            return JsonResponse({'ValueError': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)
