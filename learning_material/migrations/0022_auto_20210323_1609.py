# Generated by Django 3.0.7 on 2021-03-23 16:09

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('learning_material', '0021_auto_20210323_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datetime',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 23, 16, 9, 50, 435178, tzinfo=utc)),
        ),
    ]