# Generated by Django 3.2.16 on 2022-11-11 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_post_total_of_upvote'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='total_of_upvote',
            new_name='best_score',
        ),
    ]
