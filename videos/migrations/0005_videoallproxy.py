# Generated by Django 4.1.1 on 2022-09-17 04:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0004_video_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoAllProxy',
            fields=[
            ],
            options={
                'verbose_name': 'All video',
                'verbose_name_plural': 'All videos',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('videos.video',),
        ),
    ]