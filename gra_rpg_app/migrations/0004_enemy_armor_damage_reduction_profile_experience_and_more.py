# Generated by Django 4.0.2 on 2022-02-20 18:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gra_rpg_app', '0003_profile_chosen_armor_profile_chosen_weapon_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enemy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('damage', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('chance_of_hit', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
                ('gold', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('health', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('experience', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.AddField(
            model_name='armor',
            name='damage_reduction',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)]),
        ),
        migrations.AddField(
            model_name='profile',
            name='experience',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='health',
            field=models.IntegerField(default=100),
        ),
        migrations.AddField(
            model_name='weapon',
            name='chance_of_hit',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)]),
        ),
        migrations.AddField(
            model_name='weapon',
            name='damage',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='armor',
            name='price',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='chosen_armor',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='chosen_weapon',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='weapon',
            name='price',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
