from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from app.models import Server, UserProfile


class RegisterForm(UserCreationForm):
    name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ["name", "username", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            name = self.cleaned_data['name']
            UserProfile.objects.create(user=user, name=name)
        return user

class ServerForm(forms.ModelForm):
    class Meta:
        model = Server
        fields = ["name", "logo"]
