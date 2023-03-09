from django.urls import path
from .views import index, ContactFormView

urlpatterns = [
    path("", index, name="index"),
    path("configuration/", ContactFormView.as_view(), name="configuration"),
]