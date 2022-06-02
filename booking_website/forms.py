from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password, password_validators_help_text_html

AuthUser = get_user_model()


class RegisterForm(forms.ModelForm):
    class Meta:
        model = AuthUser
        fields = ['first_name', 'last_name', 'username', 'email', 'is_staff']
        help_texts = {
            'is_staff': 'Only check this if you are a restaurant owner.',
        }

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['is_staff'].label = "Restaurant Account"

    password = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.PasswordInput,
        help_text=password_validators_help_text_html
    )
    password_confirmation = forms.CharField(max_length=128, required=True, widget=forms.PasswordInput)

    def clean_password(self):
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data['password']
        is_staff = self.cleaned_data['is_staff']

        user = AuthUser(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            is_staff=is_staff
        )
        validate_password(password, user=user)

        return password

    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data['password_confirmation']

        if password != password_confirmation:
            raise forms.ValidationError('Password not confirmed.')

        return password_confirmation

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit is True:
            user.save()

        return user
