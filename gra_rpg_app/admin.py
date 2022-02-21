from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Weapon, Armor, User, Profile, Enemy

admin.site.register(Weapon)
admin.site.register(Armor)
admin.site.register(Profile)
admin.site.register(Enemy)
