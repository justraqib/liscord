from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, render
from django.contrib.auth import login
from django.http import HttpResponse
from app.constants import DEFAULT_CHANNEL_NAME

from app.models import Channel, Message, Server, ServerMembers
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
    if request.method == "POST":
        chosen_server_id = request.POST.get("chosenServer")
        kwargs = {
            "user": request.user,
            "server_id": chosen_server_id
        }
        is_member = ServerMembers.objects.filter(**kwargs).exists()
        if is_member:
            ServerMembers.objects.filter(**kwargs).delete()
        else:
            ServerMembers.objects.create(**kwargs)

    joined_servers = request.user.servers_joined.all()
    server_to_first_channel_map = {}
    for server in joined_servers:
        server_to_first_channel_map[server.id] = Channel.objects.filter(server=server).first().id

    ctx = {
        "all_servers": Server.objects.all(),
        "server_to_first_channel_map": server_to_first_channel_map,
        "joined_servers": joined_servers,
        "user": request.user,
        "server_form": ServerForm(),
    }
    template_name = "lobby/index.html"
    return render(request, template_name, ctx)

@login_required
def channel_view(request, channel_id):
    selected_channel = Channel.objects.get(id=channel_id)
    selected_server = selected_channel.server
    joined_servers = request.user.servers_joined.all()

    server_to_first_channel_map = {}
    for server in joined_servers:
        server_to_first_channel_map[server.id] = Channel.objects.filter(server=server).first().id

    is_member = joined_servers.filter(id=selected_server.id).exists()
    if not is_member:
        return HttpResponse("Error, you don't have the permission to view this server.")

    ctx = {
        "joined_servers": joined_servers,
        "server_to_first_channel_map": server_to_first_channel_map,
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
    form = ServerForm(request.POST, request.FILES)
    if form.is_valid():
        name = form.cleaned_data["name"]
        logo = form.cleaned_data["logo"]
        server = Server.objects.create(name=name, logo=logo)
        Channel.objects.create(server=server, name=DEFAULT_CHANNEL_NAME, created_by=request.user)
        ServerMembers.objects.create(server=server, user=request.user, is_admin=True)
    next_page = request.POST.get("currentPageUrl")
    return HttpResponseRedirect(next_page)

@login_required
def create_channel(request):
    name = request.POST.get("name")
    server_id = request.POST.get("selectedServerId")
    is_admin = ServerMembers.objects.filter(server_id=server_id, user=request.user, is_admin=True).exists()
    if not is_admin:
        return HttpResponse("Error, you don't have the permission to create a channel in this server.")

    Channel.objects.create(name=name, created_by=request.user, server_id=server_id)

    next_page = request.POST.get("currentPageUrl")
    return HttpResponseRedirect(next_page)
