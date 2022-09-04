"""liscord URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf.urls.static import static
from django.conf import settings
from .views import create_server, profile_index, register, lobby_index, channel_view, create_channel
from .ajax_views import add_message, join_leave_server

urlpatterns = [
    path("", lobby_index, name="lobby-index"),
    path("servers/create/", create_server, name="create-server"),
    path("servers/join-or-leave/", join_leave_server, name="join-or-leave-server"),
    path("channels/create/", create_channel, name="create-channel"),
    path("channels/<int:channel_id>", channel_view, name="channel-view"),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/register/", register, name="register"),
    path("profile/", profile_index, name="profile-index"),
    path("avatar/", include('avatar.urls')),
    path("messages/add/", add_message, name="add-message"),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
