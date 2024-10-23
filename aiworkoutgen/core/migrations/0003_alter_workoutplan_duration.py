# Generated by Django 5.1.2 on 2024-10-23 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_workoutplan_sections"),
    ]

    operations = [
        migrations.AlterField(
            model_name="workoutplan",
            name="duration",
            field=models.CharField(
                choices=[
                    ("15", "15 minutes"),
                    ("30", "30 minutes"),
                    ("45", "45 minutes"),
                    ("60", "60 minutes"),
                    ("75", "75 minutes"),
                    ("90", "90 minutes"),
                ],
                max_length=5,
            ),
        ),
    ]
