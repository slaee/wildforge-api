# Generated by Django 4.2.1 on 2023-09-28 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wildforge_api', '0015_alter_user_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='classmember',
            name='status',
            field=models.CharField(default='pending', max_length=50),
        ),
    ]
