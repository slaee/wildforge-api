# Generated by Django 4.2.1 on 2023-10-19 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wildforge_api', '0019_team_recuitment_status_alter_team_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='recuitment_status',
        ),
        migrations.AlterField(
            model_name='team',
            name='status',
            field=models.IntegerField(default=1),
        ),
    ]
