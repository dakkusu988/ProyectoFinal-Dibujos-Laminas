# Generated by Django 4.2.7 on 2024-06-11 21:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dibujo', '0002_like'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='timestamp',
        ),
    ]
