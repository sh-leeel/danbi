from django.urls import (
    path,
    include
)
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


urlpatterns = [
    path('task', include('task.urls')),
    path('user', include('user.urls'))
]