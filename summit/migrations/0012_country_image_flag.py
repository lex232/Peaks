# Generated by Django 4.0.2 on 2023-01-24 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summit', '0011_alter_aboutsummit_title_alter_country_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='image_flag',
            field=models.ImageField(default='default_flag.jpg', upload_to='country_flags'),
        ),
    ]
