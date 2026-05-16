from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse

from .models import SiteConfiguration


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = (
        "site_name",
        "contact_email",
        "contact_phone",
        "updated_at",
    )
    search_fields = (
        "site_name",
        "site_tagline",
        "meta_description",
        "contact_email",
        "contact_phone",
        "address",
    )
    readonly_fields = ("updated_at",)
    fieldsets = (
        (
            "Identidad del sitio",
            {
                "description": (
                    "Crea y manten aqui la unica configuracion del portal. "
                    "Si aun no existe, este sera el primer registro que definira nombre, "
                    "logo, textos base y metadatos del sitio."
                ),
                "fields": (
                    "site_name",
                    "site_tagline",
                    "meta_description",
                    "logo",
                )
            },
        ),
        (
            "Colores institucionales",
            {
                "fields": (
                    "primary_color",
                    "secondary_color",
                    "accent_color",
                )
            },
        ),
        (
            "Hero principal",
            {
                "description": "Estos textos e imagen se muestran en la portada del portal.",
                "fields": (
                    "hero_title",
                    "hero_text",
                    "hero_image",
                )
            },
        ),
        (
            "Datos de contacto",
            {
                "description": "Estos datos se reutilizan en footer, contacto y elementos institucionales.",
                "fields": (
                    "contact_email",
                    "contact_phone",
                    "whatsapp_number",
                    "address",
                )
            },
        ),
        (
            "Redes sociales",
            {
                "fields": (
                    "facebook_url",
                    "instagram_url",
                    "x_url",
                    "youtube_url",
                    "linkedin_url",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Control",
            {
                "fields": ("updated_at",),
            },
        ),
    )

    def has_add_permission(self, request):
        if SiteConfiguration.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        configuration = SiteConfiguration.get_solo()
        if configuration:
            url = reverse("admin:siteconfig_siteconfiguration_change", args=[configuration.pk])
            return redirect(url)
        return redirect(reverse("admin:siteconfig_siteconfiguration_add"))
