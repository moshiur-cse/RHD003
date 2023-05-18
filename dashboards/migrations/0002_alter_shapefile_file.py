# Generated by Django 4.1.3 on 2023-05-17 10:10

import dashboards.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shapefile',
            name='file',
            field=models.FileField(blank=True, max_length=500, null=True, upload_to=dashboards.models.get_upload_path),
        ),
    ]
