from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify


def beneficio_image_upload_to(instance, filename):
    return f"beneficios/{filename}"


class CategoriaBeneficio(models.Model):
    nombre = models.CharField("nombre", max_length=100, unique=True)
    slug = models.SlugField("slug", max_length=120, unique=True, blank=True)
    descripcion = models.CharField("descripcion", max_length=180, blank=True)
    activo = models.BooleanField("activa", default=True)
    created_at = models.DateTimeField("creada", auto_now_add=True)

    class Meta:
        verbose_name = "categoria de beneficio"
        verbose_name_plural = "categorias de beneficios"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)


class Beneficio(models.Model):
    categoria = models.ForeignKey(
        CategoriaBeneficio,
        on_delete=models.PROTECT,
        related_name="beneficios",
        verbose_name="categoria",
    )
    titulo = models.CharField("titulo", max_length=180)
    slug = models.SlugField("slug", max_length=200, unique=True, blank=True)
    descripcion_corta = models.CharField("descripcion corta", max_length=250)
    contenido = models.TextField("contenido")
    imagen = models.ImageField(
        "imagen",
        upload_to=beneficio_image_upload_to,
        blank=True,
        null=True,
    )
    activo = models.BooleanField("activo", default=True)
    destacado = models.BooleanField("destacado", default=False)
    vigencia = models.DateField(
        "vigencia",
        blank=True,
        null=True,
        help_text="Fecha hasta la que el beneficio se considera vigente.",
    )
    created_at = models.DateTimeField("creado", auto_now_add=True)
    updated_at = models.DateTimeField("actualizado", auto_now=True)

    class Meta:
        verbose_name = "beneficio"
        verbose_name_plural = "beneficios"
        ordering = ["-destacado", "titulo"]

    def __str__(self):
        return self.titulo

    def clean(self):
        super().clean()
        if self.destacado and not self.activo:
            raise ValidationError(
                {"destacado": "Un beneficio destacado debe estar activo."}
            )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)
