# Generated by Django 4.0.2 on 2023-01-26 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summit', '0012_country_image_flag'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
