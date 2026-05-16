from django.contrib import admin

from .models import CategoriaComunicado, Comunicado


@admin.register(CategoriaComunicado)
class CategoriaComunicadoAdmin(admin.ModelAdmin):
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


@admin.register(Comunicado)
class ComunicadoAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "categoria",
        "publicado",
        "destacado",
        "fecha_publicacion",
    )
    list_filter = (
        "publicado",
        "destacado",
        "categoria",
        "fecha_publicacion",
    )
    search_fields = ("titulo", "extracto", "contenido")
    prepopulated_fields = {"slug": ("titulo",)}
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "fecha_publicacion"
    list_editable = ("publicado", "destacado")
    fieldsets = (
        (
            "Contenido",
            {
                "fields": (
                    "categoria",
                    "titulo",
                    "slug",
                    "extracto",
                    "contenido",
                    "imagen",
                )
            },
        ),
        (
            "Publicacion",
            {
                "fields": (
                    "publicado",
                    "destacado",
                    "fecha_publicacion",
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
