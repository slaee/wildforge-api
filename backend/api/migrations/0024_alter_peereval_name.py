# Generated by Django 4.2.1 on 2023-10-20 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wildforge_api', '0023_teammember_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='peereval',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
