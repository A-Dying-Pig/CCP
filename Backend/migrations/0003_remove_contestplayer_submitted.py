# Generated by Django 2.1.3 on 2018-12-03 10:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0002_auto_20181203_1811'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contestplayer',
            name='submitted',
        ),
    ]
