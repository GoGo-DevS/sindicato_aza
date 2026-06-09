"""
Reasigna las imagenes del hero y de los comunicados a partir de los archivos
ya versionados en media/. Necesario porque db.sqlite3 esta en .gitignore: las
fotos viajan por git, pero las asignaciones (campos ImageField) viven en la BD
y no se transfieren. Ejecutar tras un git pull en otra maquina (ej. notebook).

Uso:  python manage.py cargar_imagenes_demo

Es idempotente y empareja por titulo (no por pk), asi funciona aunque los pk
difieran entre bases de datos.
"""
from django.conf import settings
from django.core.management.base import BaseCommand
from django.apps import apps


class Command(BaseCommand):
    help = "Reasigna hero y fotos de comunicados desde los archivos en media/."

    # substring del titulo (en minuscula)  ->  ruta relativa dentro de MEDIA_ROOT
    COMUNICADOS = {
        "programa": "comunicados/com-escolaridad.jpg",
        "asamblea": "comunicados/com-asamblea.jpg",
        "convenio": "comunicados/com-convenio.jpg",
        "procesos": "comunicados/com-procedimientos.jpg",
        "jornada": "comunicados/com-mesa-trabajo.jpg",
    }
    HERO = "siteconfig/hero-aza.jpg"

    def _existe(self, rel):
        return (settings.MEDIA_ROOT / rel).exists()

    def handle(self, *args, **options):
        # --- HERO ---
        SiteConfiguration = apps.get_model("siteconfig", "SiteConfiguration")
        sc = SiteConfiguration.objects.first()
        if sc is None:
            self.stdout.write(self.style.WARNING(
                "No hay SiteConfiguration. Corre primero: python manage.py populate_aza"))
        elif not self._existe(self.HERO):
            self.stdout.write(self.style.WARNING(f"Falta el archivo media/{self.HERO}"))
        else:
            sc.hero_image.name = self.HERO
            sc.save(update_fields=["hero_image"])
            self.stdout.write(self.style.SUCCESS(f"Hero -> {self.HERO}"))

        # --- COMUNICADOS ---
        Comunicado = apps.get_model("comunicados", "Comunicado")
        asignados = 0
        for needle, rel in self.COMUNICADOS.items():
            if not self._existe(rel):
                self.stdout.write(self.style.WARNING(f"Falta el archivo media/{rel}"))
                continue
            c = Comunicado.objects.filter(titulo__icontains=needle).first()
            if c is None:
                self.stdout.write(self.style.WARNING(
                    f"Sin comunicado que contenga '{needle}' en el titulo"))
                continue
            c.imagen.name = rel
            c.save(update_fields=["imagen"])
            asignados += 1
            self.stdout.write(self.style.SUCCESS(f"'{c.titulo[:45]}' -> {rel}"))

        self.stdout.write(self.style.SUCCESS(
            f"\nListo. {asignados}/{len(self.COMUNICADOS)} comunicados con foto."))
