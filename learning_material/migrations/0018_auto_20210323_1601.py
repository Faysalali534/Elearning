# Generated by Django 3.0.7 on 2021-03-23 16:01

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('learning_material', '0017_auto_20210323_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datetime',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 23, 16, 1, 3, 920864, tzinfo=utc)),
        ),
    ]