from gra_rpg_app.models import Weapon, Armor, Enemy, User, Profile
from django.test import Client
import pytest


@pytest.fixture
def weapon():
    weapon = Weapon.objects.create(name='NewWeapon', damage=100, chance_of_hit=0.5, price=500)
    return weapon


@pytest.fixture
def armor():
    armor = Armor.objects.create(name='NewArmor', damage_reduction=0.8, price=300)
    return armor


@pytest.fixture
def enemy():
    enemy = Enemy.objects.create(name='NewEnemy', damage=100, chance_of_hit=0.5, gold=100, health=1000, experience=50)
    return enemy


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def newuser():
    user = {
        'username': 'NewUser',
        'password': 'password123'
    }
    newuser = User.objects.create_user(**user)
    Profile.objects.create(user=newuser)
    return newuser
