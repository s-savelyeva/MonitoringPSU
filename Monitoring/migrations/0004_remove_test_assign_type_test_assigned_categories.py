# Generated by Django 5.1.7 on 2025-06-13 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Monitoring', '0003_remove_test_direction_remove_test_education_level_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='assign_type',
        ),
        migrations.AddField(
            model_name='test',
            name='assigned_categories',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
