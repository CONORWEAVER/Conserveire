# Generated by Django 3.1.6 on 2021-04-12 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LearningProject', '0022_usage_standing_charge'),
    ]

    operations = [
        migrations.AddField(
            model_name='usage',
            name='rate',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
