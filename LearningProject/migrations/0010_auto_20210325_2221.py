# Generated by Django 3.1.6 on 2021-03-25 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LearningProject', '0009_remove_usage_test'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usage',
            name='aug',
            field=models.IntegerField(default=0, unique=True),
        ),
        migrations.AlterField(
            model_name='usage',
            name='jul',
            field=models.IntegerField(default=0, unique=True),
        ),
    ]
