# Generated by Django 3.0.7 on 2021-03-14 18:23

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('learning_material', '0009_test'),
    ]

    operations = [
        migrations.CreateModel(
            name='DateTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=datetime.datetime(2021, 3, 14, 18, 23, 48, 917091, tzinfo=utc))),
            ],
        ),
    ]