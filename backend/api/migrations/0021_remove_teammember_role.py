# Generated by Django 4.2.1 on 2023-10-19 22:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wildforge_api', '0020_remove_team_recuitment_status_alter_team_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teammember',
            name='role',
        ),
    ]