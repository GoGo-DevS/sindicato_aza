from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.db import models


hex_color_validator = RegexValidator(
    regex=r"^#(?:[0-9a-fA-F]{3}){1,2}$",
    message="Ingresa un color hexadecimal valido, por ejemplo #0F4C5C.",
)


def siteconfig_upload_to(instance, filename):
    return f"siteconfig/{filename}"


class SiteConfiguration(models.Model):
    site_name = models.CharField("nombre del sitio", max_length=150)
    site_tagline = models.CharField("bajada del sitio", max_length=200, blank=True)
    meta_description = models.CharField(
        "meta descripcion",
        max_length=255,
        blank=True,
        help_text="Descripcion breve para SEO y navegadores.",
    )
    logo = models.ImageField("logo", upload_to=siteconfig_upload_to, blank=True, null=True)
    primary_color = models.CharField(
        "color principal",
        max_length=7,
        default="#0F4C5C",
        validators=[hex_color_validator],
        help_text="Color institucional principal en formato hexadecimal.",
    )
    secondary_color = models.CharField(
        "color secundario",
        max_length=7,
        default="#1F2937",
        validators=[hex_color_validator],
        help_text="Color secundario en formato hexadecimal.",
    )
    accent_color = models.CharField(
        "color de acento",
        max_length=7,
        default="#EAB308",
        validators=[hex_color_validator],
        help_text="Color de apoyo para llamados a la accion.",
    )
    contact_email = models.EmailField("correo de contacto", blank=True)
    contact_phone = models.CharField("telefono de contacto", max_length=30, blank=True)
    whatsapp_number = models.CharField("WhatsApp", max_length=30, blank=True)
    address = models.CharField("direccion", max_length=255, blank=True)
    facebook_url = models.URLField("Facebook", blank=True)
    instagram_url = models.URLField("Instagram", blank=True)
    x_url = models.URLField("X / Twitter", blank=True)
    youtube_url = models.URLField("YouTube", blank=True)
    linkedin_url = models.URLField("LinkedIn", blank=True)
    hero_title = models.CharField("titulo hero", max_length=160, blank=True)
    hero_text = models.TextField("texto hero", blank=True)
    hero_image = models.ImageField(
        "imagen hero",
        upload_to=siteconfig_upload_to,
        blank=True,
        null=True,
    )
    updated_at = models.DateTimeField("actualizado", auto_now=True)

    class Meta:
        verbose_name = "configuracion del sitio"
        verbose_name_plural = "configuracion del sitio"

    def __str__(self):
        return self.site_name or "Configuracion del sitio"

    def clean(self):
        super().clean()
        if (
            not self.pk
            and SiteConfiguration.objects.exclude(pk=self.pk).exists()
        ):
            raise ValidationError("Solo puede existir una configuracion del sitio.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        return cls.objects.first()
