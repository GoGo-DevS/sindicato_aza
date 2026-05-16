from django.urls import path

from .views import BeneficioListView


app_name = "beneficios"

urlpatterns = [
    path("", BeneficioListView.as_view(), name="list"),
]
