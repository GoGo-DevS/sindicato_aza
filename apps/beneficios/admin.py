from django.contrib import admin

from .models import Beneficio, CategoriaBeneficio


@admin.register(CategoriaBeneficio)
class CategoriaBeneficioAdmin(admin.ModelAdmin):
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


@admin.register(Beneficio)
class BeneficioAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "categoria",
        "activo",
        "destacado",
        "vigencia",
    )
    list_filter = ("activo", "destacado", "categoria", "vigencia")
    search_fields = ("titulo", "descripcion_corta", "contenido")
    prepopulated_fields = {"slug": ("titulo",)}
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "vigencia"
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
            "Estado y vigencia",
            {
                "fields": (
                    "activo",
                    "destacado",
                    "vigencia",
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
