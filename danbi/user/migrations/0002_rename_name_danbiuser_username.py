# Generated by Django 4.2.3 on 2023-07-08 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='danbiuser',
            old_name='name',
            new_name='username',
        ),
    ]
