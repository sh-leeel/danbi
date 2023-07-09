from django.urls import path
from .views import Signup, SignIn

urlpatterns = [
    path('/signup', Signup.as_view()),
    path('/signin', SignIn.as_view()),
]
