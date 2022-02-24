import pytest
from django.urls import reverse
from .models import Weapon, Armor, Enemy, User, Profile

# Testy modułów --------------------------------------------------------------------------------------------------------


@pytest.mark.django_db
def test_weapon_model(weapon):
    """
    Testuje dodanie jednego elementu do bazy.
    """
    assert len(Weapon.objects.all()) == 1
    assert Weapon.objects.get(name='NewWeapon') == weapon


@pytest.mark.django_db
def test_armor_model(armor):
    """
    Testuje dodanie jednego elementu do bazy.
    """
    assert len(Armor.objects.all()) == 1
    assert Armor.objects.get(name='NewArmor') == armor


@pytest.mark.django_db
def test_enemy_model(enemy):
    """
    Testuje dodanie jednego elementu do bazy.
    """
    assert len(Enemy.objects.all()) == 1
    assert Enemy.objects.get(name='NewEnemy') == enemy


@pytest.mark.django_db
def test_user_model(newuser):
    """
    Testuje dodanie jednego elementu do bazy.
    """
    assert len(User.objects.all()) == 1
    assert User.objects.get(username='NewUser') == newuser


@pytest.mark.django_db
def test_profile_model(newuser):
    """
    Testuje czy model Profile poprawnie utworzył się po dodaniu użytkownika.
    """
    assert len(Profile.objects.all()) == 1
    profile = Profile.objects.get(user=newuser)
    assert profile.health == 100
    assert profile.experience == 0
    assert profile.gold == 1000

# Testy widoków --------------------------------------------------------------------------------------------------------
# Testy logowania, wylogowania, tworzenia i kasowania kont -------------------------------------------------------------


@pytest.mark.django_db
def test_loginview(client, newuser):
    """
    Testuje wejście metodą GET i POST, sprawdza poprawność logowania i przekierowania po zalogowaniu.
    """
    user = {
        'login': 'NewUser',
        'password': 'password123'
    }

    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200
    assert response.wsgi_request.user.is_authenticated is False
    response = client.post(url, user)
    assert response.wsgi_request.user.is_authenticated
    assert response.status_code == 302
    assert response.url == '/'


@pytest.mark.django_db
def test_logoutview(client, newuser):
    """
    Testuje wejście metodą GET, sprawdza poprawność wylogowania i przekierowania po wylogowaniu.
    """
    client.login(username='NewUser', password='password123')
    response = client.get('/logout/')
    assert response.wsgi_request.user.is_authenticated is False
    assert response.status_code == 302
    assert response.url == '/login'


@pytest.mark.django_db
def test_deleteaccountview(client, newuser):
    """
    Testuje wejście metodą GET, sprawdza poprawność usunięcia konta i przekierowania po skasowaniu.
    """
    client.login(username='NewUser', password='password123')
    response = client.get('/delete_account/')
    assert len(Profile.objects.all()) == 0
    assert response.status_code == 302
    assert response.url == '/login'


@pytest.mark.django_db
def test_registerview(client):
    """
    Testuje wejście metodą GET i POST, sprawdza poprawność rejestracji i przekierowania po rejestracji.
    """
    user = {
        'username': 'NewUser1',
        'pass1': 'password123',
        'pass2': 'password123',
        'first_name': 'New',
        'last_name': 'User',
        'email': 'new@user.org'
    }

    response = client.get('/register/')
    assert response.status_code == 200
    response = client.post('/register/', user)
    assert len(Profile.objects.all()) == 1
    assert User.objects.get(username='NewUser1').first_name == 'New'
    assert response.status_code == 302
    assert response.url == '/login/'

# Testy pozostałych widoków --------------------------------------------------------------------------------------------


@pytest.mark.django_db
def test_mainview(client, newuser):
    """
    Testuje wejście metodą GET
    """
    client.login(username='NewUser', password='password123')
    response = client.get('/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_shopview(client, newuser):
    """
    Testuje wejście metodą GET
    """
    client.login(username='NewUser', password='password123')
    response = client.get('/shop/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_weapon_details_view(client, newuser, weapon):
    """
    Testuje wejście metodą GET i POST, sprawdza poprawność przekierowania.
    """
    client.login(username='NewUser', password='password123')
    weapon = Weapon.objects.get(name='NewWeapon')
    weapon_id = weapon.id
    response = client.get(f'/shop/weapon_details/{weapon_id}/')
    assert response.status_code == 200
    weap = {'weapon_bought': {weapon.id}}
    response = client.post(f'/shop/weapon_details/{weapon_id}/', weap)
    assert response.status_code == 302
    assert response.url == '/shop/'


@pytest.mark.django_db
def test_armor_details_view(client, newuser, armor):
    """
    Testuje wejście metodą GET i POST, sprawdza poprawność przekierowania.
    """
    client.login(username='NewUser', password='password123')
    armor = Armor.objects.get(name='NewArmor')
    armor_id = armor.id
    response = client.get(f'/shop/armor_details/{armor_id}/')
    assert response.status_code == 200
    armo = {'armor_bought': {armor.id}}
    response = client.post(f'/shop/armor_details/{armor_id}/', armo)
    assert response.status_code == 302
    assert response.url == '/shop/'


@pytest.mark.django_db
def test_medicview(client, newuser):
    """
    Testuje wejście metodą GET i POST, sprawdza poprawność przekierowania.
    """
    client.login(username='NewUser', password='password123')
    response = client.get('/medic/')
    assert response.status_code == 200

    profile = Profile.objects.get(user=newuser)
    profile.health = 50
    profile.gold = 100
    profile.save()
    hea = {'health_bought': 'health_bought'}
    response = client.post('/medic/', hea)
    profile.refresh_from_db()
    assert profile.health == 60  # bug
    assert profile.gold == 50
    assert response.status_code == 200


@pytest.mark.django_db
def test_enemiesview(client, newuser):
    """
    Testuje wejście metodą GET.
    """
    client.login(username='NewUser', password='password123')
    response = client.get('/enemies/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_enemy_details_view(client, newuser, enemy):
    """
    Testuje wejście metodą GET.
    """
    client.login(username='NewUser', password='password123')
    enemy = Enemy.objects.get(name='NewEnemy')
    enemy_id = enemy.id
    response = client.get(f'/enemies/{enemy_id}/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_dungeon1view(client, newuser, enemy):
    """
    Testuje wejście metodą GET.
    """
    client.login(username='NewUser', password='password123')
    response = client.get('/dungeon1/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_outfit_view(client, newuser, enemy):
    """
    Testuje wejście metodą GET.
    """
    client.login(username='NewUser', password='password123')
    response = client.get('/outfit/')
    assert response.status_code == 200
