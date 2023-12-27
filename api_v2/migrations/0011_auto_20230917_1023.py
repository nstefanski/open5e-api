# Generated by Django 3.2.20 on 2023-09-17 10:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_v2', '0010_rename_suggestedcharacteristics_characteristics'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='background',
            name='characteristics',
        ),
        migrations.AddField(
            model_name='characteristics',
            name='background',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='api_v2.background'),
            preserve_default=False,
        ),
    ]
