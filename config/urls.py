from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Sindicato AZA — Administracion"
admin.site.site_title = "AZA Admin"
admin.site.index_title = "Panel de administracion"

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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
