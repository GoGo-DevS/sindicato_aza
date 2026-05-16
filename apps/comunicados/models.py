from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


def comunicado_image_upload_to(instance, filename):
    return f"comunicados/{filename}"


class CategoriaComunicado(models.Model):
    nombre = models.CharField("nombre", max_length=100, unique=True)
    slug = models.SlugField("slug", max_length=120, unique=True, blank=True)
    descripcion = models.CharField("descripcion", max_length=180, blank=True)
    activo = models.BooleanField("activa", default=True)
    created_at = models.DateTimeField("creada", auto_now_add=True)

    class Meta:
        verbose_name = "categoria de comunicado"
        verbose_name_plural = "categorias de comunicados"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)


class Comunicado(models.Model):
    categoria = models.ForeignKey(
        CategoriaComunicado,
        on_delete=models.PROTECT,
        related_name="comunicados",
        verbose_name="categoria",
    )
    titulo = models.CharField("titulo", max_length=180)
    slug = models.SlugField("slug", max_length=200, unique=True, blank=True)
    extracto = models.CharField("extracto", max_length=300)
    contenido = models.TextField("contenido")
    imagen = models.ImageField(
        "imagen",
        upload_to=comunicado_image_upload_to,
        blank=True,
        null=True,
    )
    publicado = models.BooleanField("publicado", default=False)
    destacado = models.BooleanField("destacado", default=False)
    fecha_publicacion = models.DateTimeField(
        "fecha de publicacion",
        default=timezone.now,
        help_text="Se usa para ordenar y publicar el comunicado.",
    )
    created_at = models.DateTimeField("creado", auto_now_add=True)
    updated_at = models.DateTimeField("actualizado", auto_now=True)

    class Meta:
        verbose_name = "comunicado"
        verbose_name_plural = "comunicados"
        ordering = ["-fecha_publicacion", "-created_at"]

    def __str__(self):
        return self.titulo

    def clean(self):
        super().clean()
        if self.destacado and not self.publicado:
            raise ValidationError(
                {"destacado": "Un comunicado destacado debe estar publicado."}
            )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)
