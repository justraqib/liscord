from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from app.models import Channel, Server


@login_required
def profile_index(request):
    user = request.user
    template_name = "profiles/index.html"
    ctx = {
        "user": user,
    }
    return render(request, template_name, ctx)

def lobby_index(request):
    ctx = {
        "servers": Server.objects.all(),
    }
    template_name = "lobby/index.html"
    return render(request, template_name, ctx)

def server_view(request, server_id):
    ctx = {
        "servers": Server.objects.all(),
        "channels": Channel.objects.filter(server=server_id)
    }
    template_name = "lobby/server.html"
    return render(request, template_name, ctx)
