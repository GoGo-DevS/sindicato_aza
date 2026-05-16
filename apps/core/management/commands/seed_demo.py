from datetime import timedelta

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.beneficios.models import Beneficio, CategoriaBeneficio
from apps.comunicados.models import CategoriaComunicado, Comunicado
from apps.documentos.models import CategoriaDocumento, Documento
from apps.siteconfig.models import SiteConfiguration


class Command(BaseCommand):
    help = "Carga datos iniciales para el portal Sindicato Unificado AZA."

    def handle(self, *args, **options):
        self.create_site_configuration()
        self.create_comunicados()
        self.create_documentos()
        self.create_beneficios()
        self.stdout.write(self.style.SUCCESS("Datos AZA cargados correctamente."))

    def create_site_configuration(self):
        configuration = SiteConfiguration.get_solo()
        if configuration:
            self.stdout.write("SiteConfiguration ya existe. Se mantiene la configuracion actual.")
            return

        configuration = SiteConfiguration.objects.create(
            site_name="Sindicato Unificado AZA",
            site_tagline="Juntos somos mas fuertes",
            meta_description="Portal oficial del Sindicato Unificado AZA. Informacion, beneficios y comunicados para todos los socios.",
            primary_color="#1565C0",
            secondary_color="#263238",
            accent_color="#2E7D32",
            contact_email="contacto@sindicatoaza.cl",
            contact_phone="+56 2 2345 6789",
            whatsapp_number="+56 9 8765 4321",
            address="Instalaciones AZA, Santiago",
            facebook_url="https://facebook.com/sindicatoaza",
            instagram_url="https://instagram.com/sindicatoaza",
            linkedin_url="https://linkedin.com/company/sindicatoaza",
            hero_title="Mas fuertes juntos, mejor protegidos siempre",
            hero_text=(
                "Portal oficial del Sindicato Unificado AZA. Accede a comunicados, "
                "documentos, beneficios y toda la informacion relevante para los socios."
            ),
        )
        configuration.logo.save(
            "logo-aza.svg",
            ContentFile(self.build_logo_svg()),
            save=True,
        )
        configuration.hero_image.save(
            "hero-aza.svg",
            ContentFile(self.build_hero_svg()),
            save=True,
        )
        self.stdout.write("SiteConfiguration AZA creada.")

    def create_comunicados(self):
        categories = [
            ("Administrativo", "Avisos y gestiones administrativas del sindicato."),
            ("Laboral", "Informacion sobre condiciones laborales y negociaciones."),
            ("Bienestar", "Actividades y programas de bienestar para los socios."),
        ]
        category_map = {}
        for name, description in categories:
            category, _ = CategoriaComunicado.objects.get_or_create(
                nombre=name,
                defaults={"descripcion": description, "activo": True},
            )
            category_map[name] = category

        now = timezone.now()
        comunicados = [
            {
                "categoria": category_map["Administrativo"],
                "titulo": "Convocatoria asamblea ordinaria de socios",
                "slug": "convocatoria-asamblea-ordinaria-de-socios",
                "extracto": "Se convoca a todos los socios a la asamblea ordinaria para revisar el balance anual.",
                "contenido": (
                    "El directorio del Sindicato AZA informa que la proxima asamblea ordinaria "
                    "se realizara en la sede sindical. Se revisara el balance del periodo, "
                    "informe de actividades y se recibiran consultas de los socios."
                ),
                "publicado": True,
                "destacado": True,
                "fecha_publicacion": now - timedelta(days=2),
            },
            {
                "categoria": category_map["Laboral"],
                "titulo": "Actualizacion de convenio colectivo vigente",
                "slug": "actualizacion-convenio-colectivo-vigente",
                "extracto": "Se informa sobre los acuerdos alcanzados en la ultima ronda de negociacion colectiva.",
                "contenido": (
                    "Tras las reuniones sostenidas con la empresa, el sindicato alcanzo acuerdos "
                    "en materias de reajuste salarial, beneficios adicionales y condiciones de jornada. "
                    "El convenio entra en vigencia a partir del presente mes."
                ),
                "publicado": True,
                "destacado": True,
                "fecha_publicacion": now - timedelta(days=5),
            },
            {
                "categoria": category_map["Bienestar"],
                "titulo": "Programa de actividades primer semestre",
                "slug": "programa-actividades-primer-semestre",
                "extracto": "Conoce el calendario de actividades de bienestar planificadas para los socios y sus familias.",
                "contenido": (
                    "El area de bienestar del sindicato ha preparado un programa de actividades "
                    "que incluye talleres, jornadas recreativas y beneficios para los socios. "
                    "Revisa el calendario adjunto y reserva tu lugar."
                ),
                "publicado": True,
                "destacado": False,
                "fecha_publicacion": now - timedelta(days=10),
            },
        ]

        for item in comunicados:
            comunicado, created = Comunicado.objects.get_or_create(
                slug=item["slug"],
                defaults=item,
            )
            if created:
                comunicado.imagen.save(
                    f"{item['slug']}.svg",
                    ContentFile(self.build_card_svg(item["titulo"], "#1565C0")),
                    save=True,
                )
        self.stdout.write("Comunicados AZA listos.")

    def create_documentos(self):
        categories = [
            ("Reglamentos", "Documentos normativos internos del sindicato."),
            ("Actas", "Registros de asambleas y reuniones de directorio."),
            ("Formularios", "Plantillas y formularios de uso frecuente."),
        ]
        category_map = {}
        for name, description in categories:
            category, _ = CategoriaDocumento.objects.get_or_create(
                nombre=name,
                defaults={"descripcion": description, "activo": True},
            )
            category_map[name] = category

        documentos = [
            ("Estatutos del Sindicato AZA", "estatutos-sindicato-aza", "Reglamentos", True),
            ("Acta asamblea general extraordinaria", "acta-asamblea-general-extraordinaria", "Actas", True),
            ("Formulario de solicitud de beneficio", "formulario-solicitud-beneficio", "Formularios", False),
            ("Reglamento interno de funcionamiento", "reglamento-interno-funcionamiento", "Reglamentos", True),
            ("Ficha de actualizacion de datos del socio", "ficha-actualizacion-datos-socio", "Formularios", False),
        ]

        for index, (title, slug, category_name, featured) in enumerate(documentos, start=1):
            document, created = Documento.objects.get_or_create(
                slug=slug,
                defaults={
                    "categoria": category_map[category_name],
                    "titulo": title,
                    "descripcion": "Documento oficial del Sindicato Unificado AZA.",
                    "publico": True,
                    "destacado": featured,
                    "fecha": timezone.localdate() - timedelta(days=index),
                },
            )
            if created:
                document.archivo.save(
                    f"{slug}.txt",
                    ContentFile(self.build_document_text(title, category_name)),
                    save=True,
                )
        self.stdout.write("Documentos AZA listos.")

    def create_beneficios(self):
        categories = [
            ("Salud", "Convenios y beneficios de salud para socios."),
            ("Capacitacion", "Beneficios en programas formativos."),
            ("Bienestar", "Beneficios complementarios de bienestar."),
        ]
        category_map = {}
        for name, description in categories:
            category, _ = CategoriaBeneficio.objects.get_or_create(
                nombre=name,
                defaults={"descripcion": description, "activo": True},
            )
            category_map[name] = category

        benefits = [
            {
                "categoria": category_map["Salud"],
                "titulo": "Seguro complementario de salud",
                "slug": "seguro-complementario-salud",
                "descripcion_corta": "Reembolso de gastos medicos para socios y su grupo familiar.",
                "contenido": "Cobertura complementaria que reembolsa gastos medicos, dentales y de hospitalizacion.",
                "activo": True,
                "destacado": True,
                "vigencia": timezone.localdate() + timedelta(days=300),
            },
            {
                "categoria": category_map["Capacitacion"],
                "titulo": "Acceso a plataforma de e-learning",
                "slug": "acceso-plataforma-elearning",
                "descripcion_corta": "Acceso gratuito a cursos en linea de capacitacion profesional.",
                "contenido": "Los socios tienen acceso ilimitado a la plataforma de cursos en linea durante el periodo de vigencia.",
                "activo": True,
                "destacado": True,
                "vigencia": timezone.localdate() + timedelta(days=120),
            },
            {
                "categoria": category_map["Bienestar"],
                "titulo": "Caja de navidad para socios activos",
                "slug": "caja-navidad-socios-activos",
                "descripcion_corta": "Entrega de caja de navidad anual para todos los socios activos.",
                "contenido": "El sindicato entrega una caja de navidad a todos los socios con cotizaciones al dia.",
                "activo": True,
                "destacado": True,
                "vigencia": timezone.localdate() + timedelta(days=220),
            },
            {
                "categoria": category_map["Salud"],
                "titulo": "Convenio optico con descuento para socios",
                "slug": "convenio-optico-descuento-socios",
                "descripcion_corta": "Descuento del 30% en lentes y examenes de vista en opticas convenidas.",
                "contenido": "Los socios y su grupo familiar acceden a descuentos especiales en opticas asociadas.",
                "activo": True,
                "destacado": False,
                "vigencia": timezone.localdate() + timedelta(days=180),
            },
        ]

        for item in benefits:
            benefit, created = Beneficio.objects.get_or_create(
                slug=item["slug"],
                defaults=item,
            )
            if created:
                benefit.imagen.save(
                    f"{item['slug']}.svg",
                    ContentFile(self.build_card_svg(item["titulo"], "#263238")),
                    save=True,
                )
        self.stdout.write("Beneficios AZA listos.")

    def build_logo_svg(self):
        return b"""
<svg xmlns="http://www.w3.org/2000/svg" width="240" height="240" viewBox="0 0 240 240">
  <rect width="240" height="240" rx="40" fill="#1565C0"/>
  <circle cx="120" cy="120" r="74" fill="#2E7D32" opacity="0.20"/>
  <text x="120" y="112" text-anchor="middle" font-size="58" font-family="Arial Black, Arial, sans-serif" font-weight="900" fill="#ffffff">AZA</text>
  <text x="120" y="168" text-anchor="middle" font-size="13" font-family="Arial, sans-serif" fill="#C8E6C9" letter-spacing="3">SINDICATO</text>
</svg>
""".strip()

    def build_hero_svg(self):
        return b"""
<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="900" viewBox="0 0 1280 900">
  <rect width="1280" height="900" fill="#EEF2FF"/>
  <rect x="72" y="90" width="1136" height="720" rx="36" fill="#ffffff" stroke="#C5CAE9"/>
  <rect x="132" y="160" width="420" height="32" rx="16" fill="#1565C0" opacity="0.12"/>
  <rect x="132" y="220" width="510" height="72" rx="16" fill="#1565C0"/>
  <rect x="132" y="320" width="420" height="20" rx="10" fill="#263238" opacity="0.16"/>
  <rect x="132" y="356" width="380" height="20" rx="10" fill="#263238" opacity="0.12"/>
  <rect x="132" y="420" width="180" height="56" rx="18" fill="#2E7D32"/>
  <rect x="332" y="420" width="180" height="56" rx="18" fill="#ffffff" stroke="#1565C0" stroke-width="3"/>
  <rect x="706" y="170" width="392" height="540" rx="28" fill="#f8fafc" stroke="#dbe2ea"/>
  <rect x="760" y="240" width="280" height="170" rx="24" fill="#1565C0"/>
  <rect x="760" y="446" width="280" height="28" rx="14" fill="#263238" opacity="0.18"/>
  <rect x="760" y="492" width="230" height="28" rx="14" fill="#263238" opacity="0.12"/>
  <rect x="760" y="560" width="130" height="88" rx="20" fill="#2E7D32" opacity="0.25"/>
  <rect x="912" y="560" width="128" height="88" rx="20" fill="#1565C0" opacity="0.10"/>
</svg>
""".strip()

    def build_card_svg(self, title, color):
        return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="720" viewBox="0 0 1200 720">
  <rect width="1200" height="720" fill="#EEF2FF"/>
  <rect x="60" y="60" width="1080" height="600" rx="34" fill="{color}" opacity="0.94"/>
  <rect x="120" y="130" width="220" height="18" rx="9" fill="#ffffff" opacity="0.32"/>
  <text x="120" y="250" font-size="54" font-family="Arial, sans-serif" fill="#ffffff">{title[:28]}</text>
  <rect x="120" y="310" width="420" height="18" rx="9" fill="#ffffff" opacity="0.18"/>
  <rect x="120" y="344" width="360" height="18" rx="9" fill="#ffffff" opacity="0.14"/>
  <circle cx="940" cy="220" r="90" fill="#2E7D32" opacity="0.20"/>
  <circle cx="1010" cy="470" r="120" fill="#ffffff" opacity="0.08"/>
</svg>
""".strip().encode("utf-8")

    def build_document_text(self, title, category):
        return (
            f"{title}\n\n"
            f"Categoria: {category}\n\n"
            "Documento oficial del Sindicato Unificado AZA.\n"
        ).encode("utf-8")
