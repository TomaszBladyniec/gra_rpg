from django.db import models

# Create your models here.


from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Weapon(models.Model):
    """
    Model broni
    """
    name = models.CharField(max_length=64)
    damage = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    chance_of_hit = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])
    price = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.name


class Armor(models.Model):
    """
    Model pancerzy
    """
    name = models.CharField(max_length=64)
    damage_reduction = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])
    price = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.name


class Profile(models.Model):
    """
    Rozszerzenie modelu User o dodatkowe parametry potrzebne w grze
    """
    gold = models.IntegerField(default=1000)
    health = models.IntegerField(default=100)
    experience = models.IntegerField(default=0)
    weapons = models.ManyToManyField(Weapon)
    chosen_weapon = models.IntegerField(default=0, null=False)
    armors = models.ManyToManyField(Armor)
    chosen_armor = models.IntegerField(default=0, null=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enemy_health = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user} {self.gold}'


class Enemy(models.Model):
    """
    Model przeciwników
    """
    name = models.CharField(max_length=64)
    damage = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    chance_of_hit = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])
    gold = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    health = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    experience = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.name} {self.experience}'
