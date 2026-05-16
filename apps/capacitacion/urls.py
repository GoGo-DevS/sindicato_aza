from django.urls import path

from .views import ayuda_list

app_name = "capacitacion"

urlpatterns = [
    path("", ayuda_list, name="list"),
]
