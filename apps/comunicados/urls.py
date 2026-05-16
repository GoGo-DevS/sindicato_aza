from django.urls import path

from .views import ComunicadoDetailView, ComunicadoListView


app_name = "comunicados"

urlpatterns = [
    path("", ComunicadoListView.as_view(), name="list"),
    path("<slug:slug>/", ComunicadoDetailView.as_view(), name="detail"),
]
