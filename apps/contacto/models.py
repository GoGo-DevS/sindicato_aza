from django.core.validators import MinLengthValidator
from django.db import models


class MensajeContacto(models.Model):
    nombre = models.CharField("nombre", max_length=120)
    email = models.EmailField("correo electronico")
    telefono = models.CharField("telefono", max_length=30, blank=True)
    asunto = models.CharField("asunto", max_length=150)
    mensaje = models.TextField(
        "mensaje",
        validators=[MinLengthValidator(10, "El mensaje debe tener al menos 10 caracteres.")],
    )
    leido = models.BooleanField("leido", default=False)
    respondido = models.BooleanField("respondido", default=False)
    created_at = models.DateTimeField("recibido", auto_now_add=True)

    class Meta:
        verbose_name = "mensaje de contacto"
        verbose_name_plural = "mensajes de contacto"
        ordering = ["leido", "-created_at"]

    def __str__(self):
        return f"{self.nombre} - {self.asunto}"
