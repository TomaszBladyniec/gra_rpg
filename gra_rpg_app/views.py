from django.shortcuts import render

# Create your views here.

from .forms import LoginForm, RegisterForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View


class LoginView(View):  # bug
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
    def get(self, request):
        logout(request)
        return redirect('/login')


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'gra_rpg_app/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        user = request.user
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['pass1']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            return redirect('/login/')
        else:
            return render(request, 'gra_rpg_app/register.html', {'form': form})


class MainView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'gra_rpg_app/main.html')


class ShopView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'gra_rpg_app/shop.html')


class InnView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'gra_rpg_app/inn.html')


class Dungeon1View(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'gra_rpg_app/dungeon1.html')
