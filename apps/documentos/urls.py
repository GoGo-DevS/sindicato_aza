from django.urls import path

from .views import DocumentoListView


app_name = "documentos"

urlpatterns = [
    path("", DocumentoListView.as_view(), name="list"),
]
