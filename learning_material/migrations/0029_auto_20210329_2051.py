# Generated by Django 3.0.7 on 2021-03-29 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning_material', '0028_auto_20210329_2028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='lesson_id',
            field=models.CharField(max_length=100),
        ),
    ]
