# Generated by Django 3.1.6 on 2021-04-10 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LearningProject', '0013_auto_20210326_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='usage',
            name='county',
            field=models.CharField(choices=[('cork', 'Cork'), ('dublin', 'Dublin'), ('kerry', 'Kerry')], default='', max_length=25),
        ),
    ]
