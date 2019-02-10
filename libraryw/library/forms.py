from django import forms
from django.contrib.auth.models import User
from .models import UserProfileInfo


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UserProfileInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfileInfo
        fields = ['Roll_no', 'Name', 'Course', 'Department', 'Phone_no', 'Hostel_no', 'Room_no', 'Permanent_address']
