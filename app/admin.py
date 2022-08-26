from django.contrib import admin
from .models import Channel, Message, Server, UserProfile

admin.site.register(Channel)
admin.site.register(Message)
admin.site.register(Server)
admin.site.register(UserProfile)
