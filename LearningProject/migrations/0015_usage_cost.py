# Generated by Django 3.1.6 on 2021-04-11 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LearningProject', '0014_usage_county'),
    ]

    operations = [
        migrations.AddField(
            model_name='usage',
            name='cost',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]