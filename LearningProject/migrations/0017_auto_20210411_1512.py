# Generated by Django 3.1.6 on 2021-04-11 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LearningProject', '0016_auto_20210411_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usage',
            name='county',
            field=models.CharField(choices=[('cork', 'Cork'), ('dublin', 'Dublin'), ('kerry', 'Kerry')], max_length=25),
        ),
    ]
