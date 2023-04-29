from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from app.models import Message


@csrf_exempt
def add_message(request):
    message = request.POST.get("message")
    channel_id = request.POST.get("channelId")
    message = Message.objects.create(message=message, channel_id=channel_id, created_by=request.user)

    ctx = {"message": message}
    template_name = "lobby/message.html"
    return render(request, template_name, ctx)
