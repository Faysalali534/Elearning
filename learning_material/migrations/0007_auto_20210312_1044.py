# Generated by Django 3.0.7 on 2021-03-12 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning_material', '0006_auto_20210312_1015'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testtime',
            name='time',
        ),
        migrations.AddField(
            model_name='testtime',
            name='name',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
