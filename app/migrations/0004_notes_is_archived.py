# Generated by Django 4.2.17 on 2024-12-20 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_notes_is_pinned'),
    ]

    operations = [
        migrations.AddField(
            model_name='notes',
            name='is_archived',
            field=models.BooleanField(default=False),
        ),
    ]
