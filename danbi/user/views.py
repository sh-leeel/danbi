import bcrypt

from rest_framework.views import APIView
from rest_framework import status
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404

from task.models import Team
from user.models import DanbiUser
from common.utils.token import create_user_key, create_access_token


class Signup(APIView):
    def post(self, request):
        try:
            data = request.data
            name = data.get('name')
            team = data.get('team')
            password = data.get('password')

            team_list = Team.objects.all().values_list('name', flat=True)
            if team not in team_list:
                return JsonResponse({'message': "Not Exist Team"}, status=status.HTTP_400_BAD_REQUEST)

            if DanbiUser.objects.filter(username=name):
                return JsonResponse({'message': "Duplicate Name"}, status=status.HTTP_400_BAD_REQUEST)

            user_key = create_user_key()
            password = password.encode("utf-8")
            hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt()).decode()

            user = DanbiUser.objects.create(username=name, password=hashed_pw, user_key=user_key, team=team)
            token = create_access_token(user=user)

            return JsonResponse({'Token': token}, status=status.HTTP_201_CREATED)
        
        except KeyError as key_e:
            return JsonResponse({'KeyError': f'{key_e}'}, status=status.HTTP_400_BAD_REQUEST)

        except ValueError as value_e:
            return JsonResponse({'ValueError': f'{value_e}'}, status=status.HTTP_400_BAD_REQUEST)


class SignIn(APIView):
    def post(self, request):
        try:
            user = get_object_or_404(DanbiUser, username=request.data['name'])
            if not user:
                return JsonResponse({'message': "Invalid User"}, status=status.HTTP_400_BAD_REQUEST)
            
            if not bcrypt.checkpw(request.data['password'].encode("utf-8"), user.password.encode()):
                return JsonResponse({'message': "Invalid User"}, status=status.HTTP_400_BAD_REQUEST)     
            
            token = create_access_token(user=user)
            return JsonResponse({'Token': token}, status=status.HTTP_200_OK)

        except KeyError as key_e:
            return JsonResponse({'KeyError': f'{key_e}'}, status=status.HTTP_400_BAD_REQUEST)

        except ValueError as value_e:
            return JsonResponse({'ValueError': f'{value_e}'}, status=status.HTTP_400_BAD_REQUEST)
