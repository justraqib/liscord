from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def profile_index(request):
    user = request.user
    template_name = "profiles/index.html"
    ctx = {
        "user": user,
    }
    return render(request, template_name, ctx)
