# Generated by Django 5.0.2 on 2024-02-23 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listapp', '0002_alter_resumemanager_resume'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resumemanager',
            name='emp_email',
        ),
        migrations.RemoveField(
            model_name='resumemanager',
            name='emp_name',
        ),
        migrations.AddField(
            model_name='resumemanager',
            name='candidate_contactNumber',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='resumemanager',
            name='candidate_education',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='resumemanager',
            name='candidate_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='resumemanager',
            name='candidate_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='resumemanager',
            name='resume',
            field=models.FileField(blank=True, null=True, upload_to='resumes/'),
        ),
    ]