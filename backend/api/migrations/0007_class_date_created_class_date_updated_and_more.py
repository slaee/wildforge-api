# Generated by Django 4.2.5 on 2023-09-23 13:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wildforge_api', '0006_add_classCode_and_teacherId_to_existing_classes'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='date_created',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='class',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='class',
            name='class_code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='class',
            name='teacherId',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
