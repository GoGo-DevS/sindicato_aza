from django.contrib import admin

from .models import Capacitacion, CategoriaCapacitacion


@admin.register(CategoriaCapacitacion)
class CategoriaCapacitacionAdmin(admin.ModelAdmin):
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


@admin.register(Capacitacion)
class CapacitacionAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "categoria",
        "modalidad",
        "fecha",
        "cupos",
        "activo",
        "destacado",
    )
    list_filter = ("activo", "destacado", "modalidad", "categoria")
    search_fields = ("titulo", "descripcion_corta", "contenido")
    prepopulated_fields = {"slug": ("titulo",)}
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "fecha"
    list_editable = ("activo", "destacado")
    fieldsets = (
        (
            "Contenido",
            {
                "fields": (
                    "categoria",
                    "titulo",
                    "slug",
                    "descripcion_corta",
                    "contenido",
                    "imagen",
                )
            },
        ),
        (
            "Detalles",
            {
                "fields": (
                    "modalidad",
                    "duracion",
                    "fecha",
                    "cupos",
                )
            },
        ),
        (
            "Estado",
            {
                "fields": (
                    "activo",
                    "destacado",
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
