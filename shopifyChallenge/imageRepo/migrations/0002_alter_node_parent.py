# Generated by Django 3.2.7 on 2021-10-12 22:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('imageRepo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='parent',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='imageRepo.node'),
        ),
    ]