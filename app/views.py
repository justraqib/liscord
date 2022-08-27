from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from app.models import Channel, Message, Server


@login_required
def profile_index(request):
    template_name = "profiles/index.html"
    ctx = {
        "user": request.user,
    }
    return render(request, template_name, ctx)

@login_required
def lobby_index(request):
    ctx = {
        "servers": Server.objects.all(),
        "user": request.user,
    }
    template_name = "lobby/index.html"
    return render(request, template_name, ctx)

@login_required
def server_view(request, server_id):
    selected_server = Server.objects.get(id=server_id)
    ctx = {
        "servers": Server.objects.all(),
        "selected_server": selected_server,
        "channels": Channel.objects.filter(server=selected_server),
        "user": request.user,
    }
    template_name = "lobby/server.html"
    return render(request, template_name, ctx)

@login_required
def channel_view(request, channel_id):
    if request.method == "POST":
        message = request.POST.get("message")
        Message.objects.create(message=message, channel_id=channel_id, created_by=request.user)

    selected_channel = Channel.objects.get(id=channel_id)
    selected_server = selected_channel.server
    ctx = {
        "servers": Server.objects.all(),
        "selected_server": selected_server,
        "channels": Channel.objects.filter(server=selected_server),
        "selected_channel": selected_channel,
        "messages": Message.objects.filter(channel=selected_channel),
        "user": request.user,
    }
    template_name = "lobby/channel.html"
    return render(request, template_name, ctx)
