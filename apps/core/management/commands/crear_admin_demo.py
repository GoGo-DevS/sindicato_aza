"""
Crea un superusuario si no existe ninguno. Idem potente.
Lee credenciales de env vars; si no están definidas, usa valores demo.

Uso: python manage.py crear_admin_demo
"""
import os
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Crea un superusuario si no existe ninguno."

    def handle(self, *args, **options):
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write("Superusuario ya existe, nada que hacer.")
            return

        username = os.getenv("ADMIN_USERNAME", "gogo")
        email = os.getenv("ADMIN_EMAIL", "admin@sindicatoaza.cl")
        password = os.getenv("ADMIN_PASSWORD", "GogoAza2026!")

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(
            f"Superusuario creado: {username} / {'*' * len(password)}"
        ))
