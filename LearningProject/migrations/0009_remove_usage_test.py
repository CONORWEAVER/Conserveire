# Generated by Django 3.1.6 on 2021-03-25 20:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LearningProject', '0008_usage_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usage',
            name='test',
        ),
    ]