# Generated by Django 4.1.1 on 2022-09-17 06:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0008_video_publish_timestamp_alter_video_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='timestamp',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='video',
            name='updated',
            field=models.DateField(auto_now=True),
        ),
    ]
