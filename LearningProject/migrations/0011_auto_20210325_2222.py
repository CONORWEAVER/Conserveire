# Generated by Django 3.1.6 on 2021-03-25 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LearningProject', '0010_auto_20210325_2221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usage',
            name='aug',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='usage',
            name='jul',
            field=models.IntegerField(default=0),
        ),
    ]
