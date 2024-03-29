# Generated by Django 4.0.2 on 2023-01-24 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summit', '0010_aboutsummit_country_2_alter_aboutsummit_country_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aboutsummit',
            name='title',
            field=models.CharField(default=None, max_length=200, unique=True, verbose_name='Name of mountain'),
        ),
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(default=None, max_length=150, unique=True),
        ),
        migrations.AlterField(
            model_name='mountainrange',
            name='name',
            field=models.CharField(default=None, max_length=150, unique=True),
        ),
    ]
