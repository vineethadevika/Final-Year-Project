# Generated by Django 5.0.3 on 2024-03-31 23:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0021_alter_addtimetable_iv_cse_a_faculty_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Invigilation',
        ),
        migrations.DeleteModel(
            name='InvigilationAssignment',
        ),
    ]
