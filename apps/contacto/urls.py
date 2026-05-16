from django.urls import path

from .views import ContactoView


app_name = "contacto"

urlpatterns = [
    path("", ContactoView.as_view(), name="index"),
]
