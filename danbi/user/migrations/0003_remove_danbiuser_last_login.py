# Generated by Django 4.2.3 on 2023-07-08 13:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_rename_name_danbiuser_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='danbiuser',
            name='last_login',
        ),
    ]
