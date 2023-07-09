from django.db import models
from user.models import DanbiUser


class Team(models.Model):
    name = models.CharField(max_length=50)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'teams'


class Task(models.Model):
    create_user = models.ForeignKey(DanbiUser, on_delete=models.CASCADE, null=True)
    team = models.CharField(max_length=50)
    title = models.CharField(max_length=500)
    content = models.TextField()
    is_complete = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        
    class Meta:
        db_table = 'task'


class SubTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)
    team = models.CharField(max_length=50)
    is_complete = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sub_task'
