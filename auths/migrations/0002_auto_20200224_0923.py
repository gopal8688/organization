# Generated by Django 3.0.3 on 2020-02-24 09:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='webplatform',
            old_name='verification',
            new_name='verify_code',
        ),
    ]
