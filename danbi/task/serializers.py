from rest_framework import serializers
from django.core.exceptions import ValidationError 

from task.models import Team, Task, SubTask


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('name',)


class SubTaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    team = serializers.CharField(max_length=50)
    is_complete = serializers.BooleanField()
    is_delete = serializers.BooleanField()
    completed_date = serializers.DateTimeField()

    class Meta:
        model = SubTask
        fields = '__all__'


class SubEditTaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    subtasks = SubTaskSerializer(many=True, required=True)


class TaskSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, required=True)

    class Meta:
        model = Task
        fields = '__all__'

    def create(user, validated_data):
        subtasks_data = validated_data.pop('subtasks')
        task = Task.objects.create(**validated_data)
        task.create_user = user
        task.save()

        team = Team.objects.all().values_list('name', flat=True)
        for subtask_data in subtasks_data:
            if subtask_data.get('team') not in team:
                raise ValidationError({'error': 'Not Exist Team'})
        
            SubTask.objects.create(task=task, **subtask_data)

        return task


class MainTaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    team = serializers.CharField(max_length=50)
    title = serializers.CharField(max_length=500)
    content = serializers.CharField()
    is_complete = serializers.BooleanField()
    is_delete = serializers.BooleanField()