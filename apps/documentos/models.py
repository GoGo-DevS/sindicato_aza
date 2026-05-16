from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


def documento_upload_to(instance, filename):
    return f"documentos/{filename}"


class CategoriaDocumento(models.Model):
    nombre = models.CharField("nombre", max_length=100, unique=True)
    slug = models.SlugField("slug", max_length=120, unique=True, blank=True)
    descripcion = models.CharField("descripcion", max_length=180, blank=True)
    activo = models.BooleanField("activa", default=True)
    created_at = models.DateTimeField("creada", auto_now_add=True)

    class Meta:
        verbose_name = "categoria de documento"
        verbose_name_plural = "categorias de documentos"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)


class Documento(models.Model):
    categoria = models.ForeignKey(
        CategoriaDocumento,
        on_delete=models.PROTECT,
        related_name="documentos",
        verbose_name="categoria",
    )
    titulo = models.CharField("titulo", max_length=180)
    slug = models.SlugField("slug", max_length=200, unique=True, blank=True)
    archivo = models.FileField("archivo", upload_to=documento_upload_to)
    descripcion = models.CharField("descripcion", max_length=300, blank=True)
    publico = models.BooleanField("publico", default=True)
    destacado = models.BooleanField("destacado", default=False)
    fecha = models.DateField("fecha", default=timezone.localdate)
    created_at = models.DateTimeField("creado", auto_now_add=True)
    updated_at = models.DateTimeField("actualizado", auto_now=True)

    class Meta:
        verbose_name = "documento"
        verbose_name_plural = "documentos"
        ordering = ["-fecha", "titulo"]

    def __str__(self):
        return self.titulo

    def clean(self):
        super().clean()
        if self.destacado and not self.publico:
            raise ValidationError(
                {"destacado": "Un documento destacado debe ser publico."}
            )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)
