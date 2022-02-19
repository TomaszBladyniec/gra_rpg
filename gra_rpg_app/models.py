from django.db import models

# Create your models here.

from django.db import models
from django.core.validators import MinValueValidator


class Weapon(models.Model):
    name = models.CharField(max_length=64)
    price = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return self.name
