# Generated by Django 4.0.5 on 2022-11-06 13:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_comment_depth_comment_path'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='depth',
        ),
    ]
