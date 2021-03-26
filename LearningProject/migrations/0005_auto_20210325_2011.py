# Generated by Django 3.1.6 on 2021-03-25 20:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('LearningProject', '0004_auto_20210307_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usage',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='county',
            field=models.CharField(choices=[('cork', 'Cork'), ('dublin', 'Dublin'), ('kerry', 'Kerry')], max_length=20),
        ),
    ]
