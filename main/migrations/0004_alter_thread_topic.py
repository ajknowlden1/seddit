# Generated by Django 4.1.5 on 2023-01-14 13:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_thread_topic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='topic',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='main.topic'),
        ),
    ]
