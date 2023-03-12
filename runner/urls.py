from django.urls import path
from .views import index, ContactFormView, scrapper_file

urlpatterns = [
    path("", index, name="index"),
    path("scrapper/", scrapper_file, name="scrapper"),
    path("configuration/", ContactFormView.as_view(), name="configuration"),
]