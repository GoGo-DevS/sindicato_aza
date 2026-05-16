from django.db import models
from django.utils.text import slugify


def capacitacion_image_upload_to(instance, filename):
    return f"capacitacion/{filename}"


class CategoriaCapacitacion(models.Model):
    nombre = models.CharField("nombre", max_length=100, unique=True)
    slug = models.SlugField("slug", max_length=120, unique=True, blank=True)
    descripcion = models.CharField("descripcion", max_length=180, blank=True)
    activo = models.BooleanField("activa", default=True)
    created_at = models.DateTimeField("creada", auto_now_add=True)

    class Meta:
        verbose_name = "categoria de capacitacion"
        verbose_name_plural = "categorias de capacitacion"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)


class Capacitacion(models.Model):
    MODALIDAD_CHOICES = [
        ("presencial", "Presencial"),
        ("online", "Online"),
        ("hibrida", "Hibrida"),
    ]

    categoria = models.ForeignKey(
        CategoriaCapacitacion,
        on_delete=models.PROTECT,
        related_name="capacitaciones",
        verbose_name="categoria",
    )
    titulo = models.CharField("titulo", max_length=180)
    slug = models.SlugField("slug", max_length=200, unique=True, blank=True)
    descripcion_corta = models.CharField("descripcion corta", max_length=250)
    contenido = models.TextField("contenido")
    imagen = models.ImageField(
        "imagen",
        upload_to=capacitacion_image_upload_to,
        blank=True,
        null=True,
    )
    modalidad = models.CharField(
        "modalidad",
        max_length=20,
        choices=MODALIDAD_CHOICES,
        default="presencial",
    )
    duracion = models.CharField(
        "duracion",
        max_length=80,
        help_text='Ej: "8 horas", "2 dias"',
    )
    fecha = models.DateField("fecha")
    cupos = models.IntegerField("cupos", default=0)
    activo = models.BooleanField("activo", default=True)
    destacado = models.BooleanField("destacado", default=False)
    created_at = models.DateTimeField("creado", auto_now_add=True)
    updated_at = models.DateTimeField("actualizado", auto_now=True)

    class Meta:
        verbose_name = "capacitacion"
        verbose_name_plural = "capacitaciones"
        ordering = ["fecha", "titulo"]

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)
