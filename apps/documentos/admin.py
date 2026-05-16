from django.contrib import admin

from .models import CategoriaDocumento, Documento


@admin.register(CategoriaDocumento)
class CategoriaDocumentoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "activo", "created_at")
    list_filter = ("activo",)
    search_fields = ("nombre", "descripcion")
    prepopulated_fields = {"slug": ("nombre",)}
    readonly_fields = ("created_at",)
    fieldsets = (
        (
            "Informacion general",
            {
                "fields": (
                    "nombre",
                    "slug",
                    "descripcion",
                    "activo",
                )
            },
        ),
        (
            "Control",
            {
                "fields": ("created_at",),
            },
        ),
    )


@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "categoria",
        "publico",
        "destacado",
        "fecha",
    )
    list_filter = ("publico", "destacado", "categoria", "fecha")
    search_fields = ("titulo", "descripcion")
    prepopulated_fields = {"slug": ("titulo",)}
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "fecha"
    list_editable = ("publico", "destacado")
    fieldsets = (
        (
            "Archivo y contenido",
            {
                "fields": (
                    "categoria",
                    "titulo",
                    "slug",
                    "archivo",
                    "descripcion",
                )
            },
        ),
        (
            "Visibilidad",
            {
                "fields": (
                    "publico",
                    "destacado",
                    "fecha",
                )
            },
        ),
        (
            "Control",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
