from django.urls import path, include
from . import views

urlpatterns = [
    path("chat", views.chat),
    path("api/me", views.me),
    path("api/projects", views.list_projects),
    path("api/messages", views.messages_list),
    path("api/send", views.send),
]
