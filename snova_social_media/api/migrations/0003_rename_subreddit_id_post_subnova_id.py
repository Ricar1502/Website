# Generated by Django 4.0.5 on 2022-10-22 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_vote_v_flag'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='subreddit_id',
            new_name='subNova_id',
        ),
    ]
