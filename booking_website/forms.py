from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password, password_validators_help_text_html
from django.urls import reverse_lazy

from booking_website.models import Profile, Booking, BookingReview

AuthUser = get_user_model()


class RegisterForm(forms.ModelForm):
    class Meta:
        model = AuthUser
        fields = ['first_name', 'last_name', 'email', 'is_staff', ]
        help_texts = {
            'is_staff': 'Only check this if you are a restaurant business owner.',
        }

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['is_staff'].label = "Restaurant Business Account"
        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('register')
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Submit'))

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
        email = self.cleaned_data.get('email')
        password = self.cleaned_data['password']
        is_staff = self.cleaned_data['is_staff']

        user = AuthUser(
            first_name=first_name,
            last_name=last_name,
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


class ProfileAvatarForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
        labels = {
            'avatar': 'Choose Profile Picture:'
        }


class MakeBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
        }
        labels = {
            'date': 'Choose the date of the reservation:',
            'time': 'Choose the time of the reservation:'
        }

    def __init__(self, *args, user, restaurant, table, **kwargs):
        self._instance = kwargs.get('instance')
        self._user = user
        self._restaurant = restaurant
        self._table = table

        super().__init__(*args, **kwargs)

        self.fields['user'].required = False
        self.fields['restaurant'].required = False
        self.fields['table'].required = False
        self.fields['booking_fee_level'].required = False
        self.fields['QR_code'].required = False

    def save(self, commit=True):
        booking = super().save(commit=False)
        booking.user = self._user
        booking.restaurant = self._instance.restaurant if self._instance else self._restaurant
        booking.table = self._instance.table if self._instance else self._table

        if commit:
            booking.save()

        return booking

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.layout = Layout(
        Row(
            Column('date', css_class='form-group col-md-2 mb-0'),
            Column(),
            Column(),
            css_class='form-row'
        ),
        Row(css_class='form-control-lg'),
        Row(
            Column('time', css_class='form-group col-md-2 mb-0'),
            Column(),
            Column(),
            css_class='form-row'
        ),
        Row(css_class='form-control-lg'),
        Submit('submit', 'Make / Edit reservation')
    )


class MakeReviewForm(forms.ModelForm):
    class Meta:
        model = BookingReview
        fields = '__all__'
        widgets = {
            'review_text': forms.Textarea(attrs={'rows': 3, 'col': 6}),
        }
        labels = {
            'review_text': 'Feel free to add your thoughts about this particular experience:',
        }

    def __init__(self, *args, user, **kwargs):
        self._instance = kwargs.get('instance')
        self._user = user
        self._restaurant = self._instance.restaurant
        self._text = kwargs.get('text')

        super().__init__(*args, **kwargs)

        self.fields['user'].required = False
        self.fields['restaurant'].required = False

    def save(self, commit=True):
        review = super().save(commit=False)
        review.user = self._user
        review.text = self._text
        review.restaurant = self._instance.restaurant if self._instance else self._restaurant

        if commit:
            review.save()

        return review

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.layout = Layout(
        Row(
            Column('review_text', css_class='form-group col-md-4 mb-0'),
            css_class='form-row'
        ),
        Row(css_class='form-control-lg'),
        Submit('submit', 'Submit review')
    )


class EditReviewForm(forms.ModelForm):
    class Meta:
        model = BookingReview
        fields = '__all__'
        widgets = {
            'review_text': forms.Textarea(attrs={'rows': 3, 'col': 6}),
        }
        labels = {
            'review_text': 'Feel free to add your thoughts about this particular experience:',
        }

    def __init__(self, *args, **kwargs):
        self._instance = kwargs.get('instance')
        self._user = self._instance.user
        self._restaurant = self._instance.restaurant
        self._text = self._instance.text

        super().__init__(*args, **kwargs)

        self.fields['user'].required = False
        self.fields['restaurant'].required = False

    def save(self, commit=True):
        review = super().save(commit=False)
        review.user = self._user
        review.text = self._instance.text if self._instance else self._text
        review.restaurant = self._instance.restaurant if self._instance else self._restaurant

        if commit:
            review.save()

        return review

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.layout = Layout(
        Row(
            Column('review_text', css_class='form-group col-md-4 mb-0'),
            css_class='form-row'
        ),
        Row(css_class='form-control-lg'),
        Submit('submit', 'Edit review')
    )
