# Generated by Django 2.0.6 on 2018-08-02 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todo',
            name='description',
        ),
        migrations.AddField(
            model_name='todo',
            name='content',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='todo',
            name='is_done',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='todo',
            name='title',
            field=models.CharField(max_length=80),
        ),
    ]
