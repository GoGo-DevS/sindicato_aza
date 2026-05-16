from django.urls import path

from .views import capacitacion_detail, capacitacion_list

app_name = "capacitacion"

urlpatterns = [
    path("", capacitacion_list, name="list"),
    path("<slug:slug>/", capacitacion_detail, name="detail"),
]
