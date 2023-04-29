from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

class Base(models.Model):
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __repr__(self):
        if hasattr(self, "name"):
            return f"<{self.__class__.__name__}: {self.name}>"
        return f"<{self.__class__.__name__}: {self.id}>"

    def __str__(self):
        return self.__repr__()


class UserProfile(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    phone = PhoneNumberField(null=True)
    about = models.CharField(max_length=500, null=True)


class Server(Base):
    logo = models.ImageField(upload_to="server/")
    header_image = models.ImageField(upload_to="server/", null=True)
    name = models.CharField(max_length=128)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

class Channel(Base):
    name = models.CharField(max_length=128)
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

class Message(Base):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    message = models.TextField(max_length=1024)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.message[:32]}>"
