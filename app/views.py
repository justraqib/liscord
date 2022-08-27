from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import HttpResponseRedirect, render
from django.contrib.auth import login

from app.models import Channel, Message, Server, UserProfile
from app.forms import RegisterForm, ServerForm

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            next_page_url = request.POST.get("nextPageUrl", "/")
            return HttpResponseRedirect(next_page_url)
    else:
        form = RegisterForm()

    ctx = {"form": form}
    template_name = "registration/register.html"
    return render(request, template_name, ctx)

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
        "server_form": ServerForm(),
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
        "server_form": ServerForm(),
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
        "server_form": ServerForm(),
    }
    template_name = "lobby/channel.html"
    return render(request, template_name, ctx)

@login_required
def create_server(request):
    form = ServerForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data["name"]
        logo = form.cleaned_data["logo"]
        Server.objects.create(name=name, logo=logo, created_by=request.user)
    next_page = request.POST.get("currentPageUrl")
    return HttpResponseRedirect(next_page)

@login_required
def create_channel(request):
    name = request.POST.get("name")
    server_id = request.POST.get("selectedServerId")
    Channel.objects.create(name=name, created_by=request.user, server_id=server_id)

    next_page = request.POST.get("currentPageUrl")
    return HttpResponseRedirect(next_page)
