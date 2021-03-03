from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import UserInfo


def validate_geeks_mail(value):
    if "@gmail.com" in value:
        return value
    else:
        raise ValidationError("This field accepts mail id of google only")


class UserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        # Should be valid according to User
        fields = (
            'first_name', 'last_name', 'email', 'password1', 'password2'
        )
        labels = {
            'password1': 'Password',
            'password2': 'Confirm Password'
        }

    def clean_first_name(self):
        firstname = self.cleaned_data['first_name']
        if len(firstname) < 4:
            raise forms.ValidationError('Enter more than 4 char')
        return firstname

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class UserInfoForm(forms.ModelForm):
    phone_number = forms.CharField(required=False)
    location = forms.CharField(required=False)
    user_types = [
        ('student', 'student'),
        ('professor', 'professor'),
    ]
    user_type = forms.ChoiceField(required=True, choices=user_types)

    class Meta:
        model = UserInfo
        fields = ('phone_number', 'location', 'user_type')


class EditAccountForm(UserChangeForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.CharField(required=True, validators=['validate_geeks_mail'])
    password = None

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
        ]
        labels = {'email': 'Email'}
