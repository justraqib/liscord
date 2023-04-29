from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    phone = PhoneNumberField(null=True)
    about = models.CharField(max_length=500, null=True)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.id}>"

    def __str__(self):
        return self.__repr__()
