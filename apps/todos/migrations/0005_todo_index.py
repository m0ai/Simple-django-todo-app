# Generated by Django 2.0.5 on 2018-08-06 18:50

from django.db import migrations
import positions.fields


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0004_auto_20180803_0010'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='index',
            field=positions.fields.PositionField(default=-1),
        ),
    ]
