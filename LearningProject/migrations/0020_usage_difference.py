# Generated by Django 3.1.6 on 2021-04-12 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LearningProject', '0019_auto_20210411_2032'),
    ]

    operations = [
        migrations.AddField(
            model_name='usage',
            name='difference',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
