# Generated by Django 3.1.6 on 2021-04-13 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LearningProject', '0027_usage_electricity'),
    ]

    operations = [
        migrations.AddField(
            model_name='usage',
            name='greenmonth',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
