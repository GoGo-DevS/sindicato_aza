from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve as serve_media

admin.site.site_header = "Sindicato Unificado AZA — Administración"
admin.site.site_title = "AZA Admin"
admin.site.index_title = "¿Qué deseas administrar hoy?"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("comunicados/", include("apps.comunicados.urls")),
    path("documentos/", include("apps.documentos.urls")),
    path("beneficios/", include("apps.beneficios.urls")),
    path("contacto/", include("apps.contacto.urls")),
    path("capacitacion/", include("apps.capacitacion.urls", namespace="capacitacion")),
    path("panel/", include("apps.panel.urls", namespace="panel")),
]

# Servir archivos de media (fotos de comunicados, beneficios, hero) tambien en
# produccion (DEBUG=False en Render). WhiteNoise solo sirve estaticos, no media.
urlpatterns += [
    re_path(r"^media/(?P<path>.*)$", serve_media, {"document_root": settings.MEDIA_ROOT}),
]
