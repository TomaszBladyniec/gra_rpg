from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import django.forms as forms


class LoginForm(forms.Form):
    login = forms.CharField(label='Nazwa użytkownika')
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput)


def validate_username_is_not_taken(value):
    if User.objects.filter(username=value):
        raise ValidationError('Ten login jest już zajęty')


class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        label='Nazwa użytkownika',
        validators=[validate_username_is_not_taken]
    )
    pass1 = forms.CharField(label='Hasło', widget=forms.PasswordInput, max_length=100)
    pass2 = forms.CharField(label='Powtórz hasło', widget=forms.PasswordInput, max_length=100)
    first_name = forms.CharField(label='Imię', max_length=50)
    last_name = forms.CharField(label='Nazwisko', max_length=50)
    email = forms.EmailField(label='Adres e-mail')

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['pass1'] != cleaned_data['pass2']:
            raise ValidationError('Hasła nie są takie same!')
        return cleaned_data
