# Generated by Django 3.0.7 on 2021-03-29 20:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('learning_material', '0027_auto_20210329_2022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learning_material.Course'),
        ),
    ]
