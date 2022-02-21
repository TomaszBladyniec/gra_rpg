"""gra_rpg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Homecnn.com
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from gra_rpg_app.views import MainView, LoginView, RegisterView, LogoutView, ShopView, MedicView, Dungeon1View,\
    ArmorDetailsView, WeaponDetailsView, OutfitView, DeleteAccountView, EnemiesView, EnemyDetailsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name='main'),
    path('login/', LoginView.as_view(), name='login'),
    path('delete_account/', DeleteAccountView.as_view(), name='delete_account'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('medic/', MedicView.as_view(), name='medic'),
    path('dungeon1/', Dungeon1View.as_view(), name='dungeon1'),
    path('shop/armor_details/<int:armor_id>/', ArmorDetailsView.as_view(), name='armor_details'),
    path('shop/weapon_details/<int:weapon_id>/', WeaponDetailsView.as_view(), name='weapon_details'),
    path('enemies/', EnemiesView.as_view(), name='enemies'),
    path('enemies/<int:enemy_id>/', EnemyDetailsView.as_view(), name='enemy_detail'),
    path('outfit/', OutfitView.as_view(), name='outfit'),
]
