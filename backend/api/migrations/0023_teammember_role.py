# Generated by Django 4.2.1 on 2023-10-19 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wildforge_api', '0022_peereval_date_created_peereval_date_updated_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='teammember',
            name='role',
            field=models.CharField(default='m', max_length=1),
        ),
    ]