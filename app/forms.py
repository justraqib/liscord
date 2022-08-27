from django import forms

from app.models import Server

class ServerForm(forms.ModelForm):
    class Meta:
        model = Server
        fields = ["name", "logo"]
