# Generated by Django 4.0.2 on 2022-02-19 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gra_rpg_app', '0002_profile_armors_profile_weapons'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='chosen_armor',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='chosen_weapon',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gold',
            field=models.IntegerField(default=1000),
        ),
    ]
