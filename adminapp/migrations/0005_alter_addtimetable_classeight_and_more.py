# Generated by Django 5.0.2 on 2024-03-28 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0004_seatallocation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addtimetable',
            name='classeight',
            field=models.CharField(default='free', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='addtimetable',
            name='classfive',
            field=models.CharField(default='free', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='addtimetable',
            name='classfour',
            field=models.CharField(default='free', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='addtimetable',
            name='classone',
            field=models.CharField(default='free', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='addtimetable',
            name='classseven',
            field=models.CharField(default='free', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='addtimetable',
            name='classsix',
            field=models.CharField(default='free', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='addtimetable',
            name='classthree',
            field=models.CharField(default='free', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='addtimetable',
            name='classtwo',
            field=models.CharField(default='free', max_length=20, null=True),
        ),
    ]
