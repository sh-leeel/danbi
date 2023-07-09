from django.db import models


class DanbiUser(models.Model):
    user_key = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    team = models.CharField(max_length=255)
    create_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'