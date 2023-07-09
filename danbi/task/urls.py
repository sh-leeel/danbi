from django.urls import path
from .views import (
    TeamInfo, CreateTask, ListMyTeamTask, EditMainTask, EditSubTask
)

urlpatterns = [
    path('/team', TeamInfo.as_view()),
    path('/create', CreateTask.as_view()),
    path('/list', ListMyTeamTask.as_view()),
    path('/edit/main', EditMainTask.as_view()),
    path('/edit/sub', EditSubTask.as_view()),
]
