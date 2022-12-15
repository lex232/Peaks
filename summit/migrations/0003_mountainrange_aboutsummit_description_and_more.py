# Generated by Django 4.0.2 on 2022-12-12 13:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('summit', '0002_aboutsummit_rename_genre_country_delete_film_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MountainRange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=150)),
            ],
        ),
        migrations.AddField(
            model_name='aboutsummit',
            name='description',
            field=models.TextField(default=None),
        ),
        migrations.AlterField(
            model_name='aboutsummit',
            name='high',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='aboutsummit',
            name='title',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(default=None, max_length=150),
        ),
        migrations.AddField(
            model_name='aboutsummit',
            name='mountainrange',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='summit.mountainrange'),
            preserve_default=False,
        ),
    ]