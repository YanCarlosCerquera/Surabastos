# Generated by Django 4.2.2 on 2024-02-13 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Perfiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='ubicacion_especifica',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
