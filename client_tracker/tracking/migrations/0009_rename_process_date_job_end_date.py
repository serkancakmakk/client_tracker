# Generated by Django 5.1.6 on 2025-03-05 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0008_job_created_by_alter_job_employee'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='process_date',
            new_name='end_date',
        ),
    ]
