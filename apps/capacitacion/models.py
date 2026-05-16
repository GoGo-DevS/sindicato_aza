from django.db import models


class TipoAyuda(models.Model):
    nombre = models.CharField(max_length=100)
    # Ejemplos: "Video tutorial", "Instructivo PDF", "Guia rapida"

    class Meta:
        verbose_name = "Tipo de ayuda"
        verbose_name_plural = "Tipos de ayuda"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class RecursoAyuda(models.Model):
    TIPO_CHOICES = [
        ("video",       "Video tutorial"),
        ("pdf",         "Instructivo PDF"),
        ("guia",        "Guia rapida"),
        ("presencial",  "Capacitacion presencial"),
    ]

    titulo             = models.CharField(max_length=200)
    descripcion        = models.TextField(blank=True)
    tipo               = models.CharField(max_length=20, choices=TIPO_CHOICES)
    # Para videos: URL de YouTube o Google Drive
    url_video          = models.URLField(blank=True)
    # Para PDFs o guias: archivo subible
    archivo            = models.FileField(upload_to="ayuda/", blank=True)
    # Para presencial: fecha y lugar
    fecha_presencial   = models.DateField(null=True, blank=True)
    lugar              = models.CharField(max_length=200, blank=True)
    activo             = models.BooleanField(default=True)
    orden              = models.PositiveIntegerField(default=0)
    creado             = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["orden", "-creado"]
        verbose_name = "Recurso de ayuda"
        verbose_name_plural = "Centro de ayuda"

    def __str__(self):
        return f"[{self.get_tipo_display()}] {self.titulo}"
