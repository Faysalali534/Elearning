# Generated by Django 3.0.7 on 2021-03-02 01:48

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210224_0934'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='userinfo',
            managers=[
                ('liberty', django.db.models.manager.Manager()),
            ],
        ),
    ]