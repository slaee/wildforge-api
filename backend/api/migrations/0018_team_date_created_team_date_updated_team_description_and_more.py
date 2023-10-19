# Generated by Django 4.2.5 on 2023-10-11 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wildforge_api', '0017_remove_classmember_is_teacher_classmember_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='date_created',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='team',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='team',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='max_members',
            field=models.IntegerField(default=4),
        ),
        migrations.AddField(
            model_name='team',
            name='name',
            field=models.CharField(default='Team', max_length=50),
        ),
        migrations.AddField(
            model_name='team',
            name='status',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='teammember',
            name='class_member_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wildforge_api.classmember'),
        ),
        migrations.AddField(
            model_name='teammember',
            name='date_created',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='teammember',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='teammember',
            name='role',
            field=models.CharField(default='tl', max_length=2),
        ),
        migrations.AddField(
            model_name='teammember',
            name='status',
            field=models.CharField(default='pending', max_length=50),
        ),
        migrations.AddField(
            model_name='teammember',
            name='team_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wildforge_api.team'),
        ),
    ]
