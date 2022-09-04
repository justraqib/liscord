from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from app.models import Channel, Message, ServerMembers


@csrf_exempt
def add_message(request):
    message = request.POST.get("message")
    channel_id = request.POST.get("channelId")
    message = Message.objects.create(message=message, channel_id=channel_id, created_by=request.user)

    ctx = {"message": message}
    template_name = "lobby/message.html"
    return render(request, template_name, ctx)

@csrf_exempt
def join_leave_server(request):
    chosen_server_id = request.POST.get("chosenServer")
    kwargs = {
        "server_id": chosen_server_id,
        "user": request.user
    }
    is_member = ServerMembers.objects.filter(**kwargs).exists()
    if is_member:
        server_member = ServerMembers.objects.filter(**kwargs).delete()
        return HttpResponse(status=204)
    else:
        server_member = ServerMembers.objects.create(**kwargs)
        server = server_member.server
        ctx = {
            "server": server,
            "server_to_first_channel_map": {
                server.id: Channel.objects.filter(server_id=server.id).first().id
            }
        }
        template_name = "lobby/server_icon.html"
        return render(request, template_name, ctx)
