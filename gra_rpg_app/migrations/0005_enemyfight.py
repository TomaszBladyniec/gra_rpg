# Generated by Django 4.0.2 on 2022-02-21 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gra_rpg_app', '0004_enemy_armor_damage_reduction_profile_experience_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EnemyFight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('health', models.IntegerField(null=True)),
            ],
        ),
    ]
