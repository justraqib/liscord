from django.contrib.auth.models import User
from django.shortcuts import render

def profile_index(request):
    # TODO use authenticated user instead of first user
    user = User.objects.first()
    template_name = "index.html"
    ctx = {
        "user": user,
    }
    return render(request, template_name, ctx)
