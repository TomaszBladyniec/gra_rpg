from django.shortcuts import render

# Create your views here.

import random
from .forms import LoginForm, RegisterForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Weapon, Armor, Profile, Enemy
from django.views import View


class LoginView(View):
    """
    Widok logowania
    """
    def get(self, request):
        form = LoginForm()
        return render(request, 'gra_rpg_app/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user_login = form.cleaned_data['login']
            user_password = form.cleaned_data['password']
            user = authenticate(username=user_login, password=user_password)
            if user is None:  # zły login albo/i hasło
                return render(request, 'gra_rpg_app/login.html', {'form': form, 'alert_flag': True})
            else:  # user znaleziony, można zalogować
                login(request, user)
                return redirect('/')
        else:
            return render(request, 'gra_rpg_app/login.html', {'form': form})


class LogoutView(LoginRequiredMixin, View):
    """
    Formularz wylogowania
    """
    def get(self, request):
        logout(request)
        return redirect('/login')


class DeleteAccountView(LoginRequiredMixin, View):
    """
    Widok kasowania konta
    """
    def get(self, request):
        user = User.objects.get(username=request.user.username)
        user.delete()
        return redirect('/login')


class RegisterView(View):
    """
    Widok rejestracji
    """
    def get(self, request):
        form = RegisterForm()
        return render(request, 'gra_rpg_app/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['pass1']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            Profile.objects.create(user=user)
            return redirect('/login/')
        else:
            return render(request, 'gra_rpg_app/register.html', {'form': form})


class MainView(LoginRequiredMixin, View):
    """
    Widok strony głównej (wioski)
    """
    def get(self, request):
        user = User.objects.get(username=request.user.username)
        profile = Profile.objects.get(user_id=request.user.id)
        return render(request, 'gra_rpg_app/main.html', {'user': user, 'profile': profile})


class ShopView(LoginRequiredMixin, View):
    """
    Widok sklepu
    """
    def get(self, request):
        user = User.objects.get(username=request.user.username)
        profile = Profile.objects.get(user_id=request.user.id)
        weapon = Weapon.objects.all()
        armor = Armor.objects.all()
        return render(request, 'gra_rpg_app/shop.html', {'user': user, 'profile': profile, 'weapon': weapon, 'armor': armor})


class EnemiesView(LoginRequiredMixin, View):
    """
    Widok bestiariusza
    """
    def get(self, request):
        user = User.objects.get(username=request.user.username)
        profile = Profile.objects.get(user_id=request.user.id)
        enemy1 = Enemy.objects.all()
        return render(request, 'gra_rpg_app/enemies.html', {'user': user, 'profile': profile, 'enemy': enemy1})


class EnemyDetailsView(LoginRequiredMixin, View):
    """
    Widok szczegółów przeciwnika
    """
    def get(self, request, enemy_id):
        user = User.objects.get(username=request.user.username)
        profile = Profile.objects.get(user_id=request.user.id)
        enemy1 = Enemy.objects.get(id=enemy_id)
        return render(request, 'gra_rpg_app/enemy_details.html', {'user': user, 'profile': profile, 'enemy': enemy1})


class ArmorDetailsView(LoginRequiredMixin, View):
    """
    Widok szczegółów pancerza
    """
    def get(self, request, armor_id):
        user = User.objects.get(username=request.user.username)
        profile = Profile.objects.get(user_id=request.user.id)
        armor = Armor.objects.get(id=armor_id)
        return render(request, 'gra_rpg_app/armor_details.html', {'user': user, 'profile': profile, 'armor': armor})

    def post(self, request, armor_id):
        armor = Armor.objects.get(id=int(request.POST['armor_bought']))
        profile = Profile.objects.get(user_id=request.user.id)
        profile.gold = profile.gold - armor.price
        profile.armors.add(armor)
        profile.save()
        return redirect('/shop/')


class WeaponDetailsView(LoginRequiredMixin, View):
    """
    Widok szczegółów broni
    """
    def get(self, request, weapon_id):
        user = User.objects.get(username=request.user.username)
        profile = Profile.objects.get(user_id=request.user.id)
        weapon = Weapon.objects.get(id=weapon_id)
        return render(request, 'gra_rpg_app/weapon_details.html', {'user': user, 'profile': profile, 'weapon': weapon})

    def post(self, request, weapon_id):
        weapon = Weapon.objects.get(id=int(request.POST['weapon_bought']))
        profile = Profile.objects.get(user_id=request.user.id)
        profile.gold = profile.gold - weapon.price
        profile.weapons.add(weapon)
        profile.save()
        return redirect('/shop/')


class MedicView(LoginRequiredMixin, View):
    """
    Widok medyka
    """
    def get(self, request):
        user = User.objects.get(username=request.user.username)
        profile = Profile.objects.get(user_id=request.user.id)
        if profile.health >= 100:
            return render(request, 'gra_rpg_app/medic_full_health.html', {'user': user, 'profile': profile})
        elif profile.gold <= 0:
            return render(request, 'gra_rpg_app/medic_no_gold.html', {'user': user, 'profile': profile})
        else:
            return render(request, 'gra_rpg_app/medic.html', {'user': user, 'profile': profile})


    def post(self, request):
        user = User.objects.get(username=request.user.username)
        profile = Profile.objects.get(user_id=request.user.id)
        profile.health += 10
        profile.gold -= 50
        profile.save()
        if profile.gold <= 0:
            return render(request, 'gra_rpg_app/medic_no_gold.html', {'user': user, 'profile': profile})
        if profile.health < 100:
            return render(request, 'gra_rpg_app/medic.html', {'user': user, 'profile': profile})
        else:
            return render(request, 'gra_rpg_app/medic_full_health.html', {'user': user, 'profile': profile})



class Dungeon1View(LoginRequiredMixin, View):
    """
    Widok lochów
    """
    def get(self, request):
        user = User.objects.get(username=request.user.username)
        profile = Profile.objects.get(user_id=request.user.id)
        enemy_list = list(Enemy.objects.all())
        random.shuffle(enemy_list)
        global enemy
        enemy = enemy_list[0]
        enemy_health = enemy.health
        profile.enemy_health = enemy_health
        profile.save()
        if profile.health <= 0:
            return render(request, 'gra_rpg_app/dungeon_no_health.html', {'user': user, 'profile': profile})
        if profile.chosen_weapon == 0:
            return render(request, 'gra_rpg_app/dungeon_no_weapon.html', {'user': user, 'profile': profile})
        else:
            return render(request, 'gra_rpg_app/dungeon1.html', {'user': user, 'profile': profile, 'enemy': enemy,
                                                             'enemy_health': enemy_health})

    def post(self, request):
        user = User.objects.get(username=request.user.username)
        profile = Profile.objects.get(user_id=request.user.id)
        weapon = Weapon.objects.get(id=profile.chosen_weapon)
        armor = Armor.objects.get(id=profile.chosen_armor)
        if random.randint(0, 10) <= weapon.chance_of_hit * 10:
            enemy_health = profile.enemy_health - weapon.damage
            profile.enemy_health = enemy_health
            profile.save()
        if random.randint(0, 10) <= enemy.chance_of_hit * 10:
            profile.health = profile.health - enemy.damage * armor.damage_reduction
            profile.save()
        # return HttpResponse(weapon.damage)
        if profile.health <= 0:
            return render(request, 'gra_rpg_app/game_over.html', {'user': user, 'profile': profile, 'enemy': enemy})
        if enemy_health <= 0:
            profile.gold += enemy.gold
            profile.experience += enemy.experience
            profile.save()
            return render(request, 'gra_rpg_app/dungeon_win.html', {'user': user, 'profile': profile, 'enemy': enemy})
        else:
            return render(request, 'gra_rpg_app/dungeon1.html', {'user': user, 'profile': profile, 'enemy': enemy,
                                                             'enemy_health': enemy_health})



class OutfitView(LoginRequiredMixin, View):
    """
    Widok ekwipunku
    """
    def get(self, request):
        user = User.objects.get(username=request.user.username)
        profile = Profile.objects.get(user_id=request.user.id)
        if profile.chosen_weapon != 0:
            chosen_weapon_name = Weapon.objects.get(id=profile.chosen_weapon).name
        else:
            chosen_weapon_name = 'żadna'
        if profile.chosen_armor != 0:
            chosen_armor_name = Armor.objects.get(id=profile.chosen_armor).name
        else:
            chosen_armor_name = 'żaden'
        weapons = profile.weapons.all()
        armors = profile.armors.all()
        return render(request, 'gra_rpg_app/outfit.html', {'user': user, 'profile': profile, 'weapons': weapons,
                                                           'armors': armors, 'chosen_weapon_name': chosen_weapon_name,
                                                           'chosen_armor_name': chosen_armor_name})

    def post(self, request):
        try:
            chosen_weapon = request.POST['weapon_choice']
            chosen_armor = request.POST['armor_choice']
        except:
            return redirect('/outfit')

        profile = Profile.objects.get(user_id=request.user.id)
        profile.chosen_weapon = chosen_weapon
        profile.chosen_armor = chosen_armor
        profile.save()
        return redirect('/outfit')
