# Generated by Django 5.1.2 on 2024-10-25 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_workoutplan_duration'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workoutplan',
            old_name='sections',
            new_name='workout_data',
        ),
        migrations.AddField(
            model_name='workoutplan',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='workoutplan',
            name='full_equipment_list',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='workoutplan',
            name='full_target_list',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
