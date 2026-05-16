from django.contrib import admin

from .models import RecursoAyuda, TipoAyuda


@admin.register(TipoAyuda)
class TipoAyudaAdmin(admin.ModelAdmin):
    list_display = ["nombre"]
    search_fields = ["nombre"]


@admin.register(RecursoAyuda)
class RecursoAyudaAdmin(admin.ModelAdmin):
    list_display  = ["titulo", "tipo", "activo", "orden"]
    list_editable = ["activo", "orden"]
    list_filter   = ["tipo", "activo"]
    search_fields = ["titulo", "descripcion"]
    fieldsets = (
        ("Contenido", {
            "fields": ("titulo", "descripcion", "tipo")
        }),
        ("Recursos", {
            "fields": ("url_video", "archivo"),
            "description": "Completa segun el tipo de recurso.",
        }),
        ("Presencial", {
            "fields": ("fecha_presencial", "lugar"),
            "classes": ("collapse",),
        }),
        ("Control", {
            "fields": ("activo", "orden"),
        }),
    )
