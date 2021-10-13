# Generated by Django 3.2.7 on 2021-10-13 02:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('imageRepo', '0003_auto_20211012_2254'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='directory',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='media',
            name='parent',
        ),
        migrations.AddField(
            model_name='node',
            name='parent',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='imageRepo.directory'),
        ),
    ]
