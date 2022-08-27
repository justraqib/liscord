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
from .views import create_server, profile_index, lobby_index, channel_view, server_view, create_channel

urlpatterns = [ 
    path("", lobby_index, name="lobby-index"),
    path("servers/create/", create_server, name="create-server"),
    path("channels/create/", create_channel, name="create-channel"),
    path("servers/<int:server_id>/", server_view, name="server-view"),
    path("channels/<int:channel_id>", channel_view, name="channel-view"),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("profile/", profile_index, name="profile-index"),
    path('avatar/', include('avatar.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
