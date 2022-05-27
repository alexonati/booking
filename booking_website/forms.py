from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password, password_validators_help_text_html

AuthUser = get_user_model()


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=128, required=True, label='First name')
    last_name = forms.CharField(max_length=128, required=True, label='Last name')
    username = forms.CharField(max_length=128, required=True)
    email = forms.EmailField(max_length=128, required=True)
    password = forms.CharField(max_length=128, required=True, widget=forms.PasswordInput, help_text=password_validators_help_text_html)
    password_confirmation = forms.CharField(max_length=128, required=True, widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']

        try:
            AuthUser.objects.get(username=username)
        except AuthUser.DoesNotExist:
            # There isn't any user with this username. Do nothing.
            pass
        else:
            raise forms.ValidationError('Username is already taken.')

        return username

    def clean_email(self):
        email = self.cleaned_data['email']

        try:
            AuthUser.objects.get(email=email)
        except AuthUser.DoesNotExist:
            # There isn't any user with this email. Do nothing.
            pass
        else:
            raise forms.ValidationError('E-mail address is already taken.')

        return email

    def clean_password(self):
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data['password']

        user = AuthUser(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email
        )
        validate_password(password, user=user)

        return password

    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data['password_confirmation']

        if password != password_confirmation:
            raise forms.ValidationError('Password not confirmed.')

        return password_confirmation

    def save(self):
        # Create user in DB
        user = None
        return user
