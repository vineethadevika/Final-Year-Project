# Generated by Django 5.0.3 on 2024-03-30 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0016_remove_addtimetable_batch_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='addtimetable',
            name='batch',
            field=models.CharField(default='Batch CSE A', max_length=100),
        ),
        migrations.AddField(
            model_name='addtimetable',
            name='teacher',
            field=models.CharField(default='Durga', max_length=100),
        ),
    ]
