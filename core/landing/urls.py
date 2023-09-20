from django.urls import include, path, reverse
from . import views
from .api import send_request_api_view

app_name = "landing"

urlpatterns = [
    path("", views.index, name="index"),
    path("send_request/", send_request_api_view, name="send_request_api"),
]
