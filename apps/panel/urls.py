from django.urls import path

from . import views

app_name = "panel"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    # Comunicados
    path("comunicados/", views.comunicados_list, name="comunicados_list"),
    path("comunicados/nuevo/", views.comunicados_create, name="comunicados_create"),
    path("comunicados/<int:pk>/editar/", views.comunicados_edit, name="comunicados_edit"),
    path("comunicados/<int:pk>/eliminar/", views.comunicados_delete, name="comunicados_delete"),
    # Documentos
    path("documentos/", views.documentos_list, name="documentos_list"),
    path("documentos/subir/", views.documentos_create, name="documentos_create"),
    path("documentos/<int:pk>/editar/", views.documentos_edit, name="documentos_edit"),
    path("documentos/<int:pk>/eliminar/", views.documentos_delete, name="documentos_delete"),
    # Beneficios
    path("beneficios/", views.beneficios_list, name="beneficios_list"),
    path("beneficios/nuevo/", views.beneficios_create, name="beneficios_create"),
    path("beneficios/<int:pk>/editar/", views.beneficios_edit, name="beneficios_edit"),
    path("beneficios/<int:pk>/eliminar/", views.beneficios_delete, name="beneficios_delete"),
    # Mensajes
    path("mensajes/", views.mensajes_list, name="mensajes_list"),
    path("mensajes/<int:pk>/", views.mensaje_detail, name="mensaje_detail"),
]
