# Generated by Django 4.2.1 on 2023-10-22 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wildforge_api', '0024_alter_peereval_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='max_members',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='team',
            name='status',
            field=models.CharField(default='open', max_length=10),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='status',
            field=models.CharField(default='pending', max_length=10),
        ),
    ]
