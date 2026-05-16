from django.contrib import admin

from .models import MensajeContacto


@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "email",
        "asunto",
        "leido",
        "respondido",
        "created_at",
    )
    list_filter = ("leido", "respondido", "created_at")
    search_fields = ("nombre", "email", "asunto", "mensaje")
    readonly_fields = ("nombre", "email", "telefono", "asunto", "mensaje", "created_at")
    date_hierarchy = "created_at"
    list_editable = ("leido", "respondido")
    fieldsets = (
        (
            "Datos del remitente",
            {
                "fields": (
                    "nombre",
                    "email",
                    "telefono",
                )
            },
        ),
        (
            "Mensaje recibido",
            {
                "fields": (
                    "asunto",
                    "mensaje",
                    "created_at",
                )
            },
        ),
        (
            "Seguimiento",
            {
                "fields": (
                    "leido",
                    "respondido",
                )
            },
        ),
    )
