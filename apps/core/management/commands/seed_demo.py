from datetime import timedelta

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.beneficios.models import Beneficio, CategoriaBeneficio
from apps.comunicados.models import CategoriaComunicado, Comunicado
from apps.documentos.models import CategoriaDocumento, Documento
from apps.siteconfig.models import SiteConfiguration


class Command(BaseCommand):
    help = "Carga datos demo reutilizables para el portal institucional."

    def handle(self, *args, **options):
        self.create_site_configuration()
        self.create_comunicados()
        self.create_documentos()
        self.create_beneficios()
        self.stdout.write(self.style.SUCCESS("Datos demo cargados correctamente."))

    def create_site_configuration(self):
        configuration = SiteConfiguration.get_solo()
        if configuration:
            self.stdout.write("SiteConfiguration ya existe. Se mantiene la configuracion actual.")
            return

        configuration = SiteConfiguration.objects.create(
            site_name="Portal Institucional",
            site_tagline="Portal institucional informativo y autoadministrable",
            meta_description="Centraliza la informacion y mejora la comunicacion con tu comunidad",
            primary_color="#0F4C5C",
            secondary_color="#1F2937",
            accent_color="#EAB308",
            contact_email="contacto@portalinstitucional.demo",
            contact_phone="+56 2 2345 6789",
            whatsapp_number="+56 9 8765 4321",
            address="Av. Institucional 123, Santiago",
            facebook_url="https://facebook.com/portalinstitucionaldemo",
            instagram_url="https://instagram.com/portalinstitucionaldemo",
            linkedin_url="https://linkedin.com/company/portalinstitucionaldemo",
            hero_title="Centraliza la informacion y mejora la comunicacion con tu comunidad",
            hero_text=(
                "Una base profesional para publicar comunicados, compartir documentos, "
                "mostrar beneficios y mantener abiertos los canales de contacto."
            ),
        )
        configuration.logo.save(
            "logo-demo.svg",
            ContentFile(self.build_logo_svg(configuration.site_name)),
            save=True,
        )
        configuration.hero_image.save(
            "hero-demo.svg",
            ContentFile(self.build_hero_svg()),
            save=True,
        )
        self.stdout.write("SiteConfiguration creada.")

    def create_comunicados(self):
        categories = [
            ("Informacion general", "Novedades institucionales de interes transversal."),
            ("Actividades", "Convocatorias, encuentros y actividades programadas."),
            ("Gestion interna", "Actualizaciones de procesos y coordinaciones internas."),
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
                "categoria": category_map["Informacion general"],
                "titulo": "Actualizacion del portal institucional",
                "slug": "actualizacion-del-portal-institucional",
                "extracto": "Se incorporaron nuevas secciones para centralizar la informacion y facilitar el acceso publico.",
                "contenido": (
                    "El portal institucional ya permite organizar comunicados, documentos "
                    "y beneficios en un mismo sitio. Esta estructura busca mejorar la "
                    "claridad de la informacion y reducir la dispersion de contenidos."
                ),
                "publicado": True,
                "destacado": True,
                "fecha_publicacion": now - timedelta(days=1),
            },
            {
                "categoria": category_map["Actividades"],
                "titulo": "Convocatoria a jornada informativa mensual",
                "slug": "convocatoria-a-jornada-informativa-mensual",
                "extracto": "Se invita a la comunidad a participar en una jornada abierta para revisar avances y prioridades.",
                "contenido": (
                    "La jornada informativa mensual permitira revisar hitos recientes, "
                    "aclarar dudas y presentar lineas de trabajo para el proximo periodo."
                ),
                "publicado": True,
                "destacado": False,
                "fecha_publicacion": now - timedelta(days=4),
            },
            {
                "categoria": category_map["Gestion interna"],
                "titulo": "Nuevo calendario de procesos administrativos",
                "slug": "nuevo-calendario-de-procesos-administrativos",
                "extracto": "Se publico un calendario referencial para ordenar fechas y entregables institucionales.",
                "contenido": (
                    "Con el objetivo de facilitar la planificacion, se consolido un "
                    "calendario con hitos, plazos y responsables de procesos frecuentes."
                ),
                "publicado": True,
                "destacado": True,
                "fecha_publicacion": now - timedelta(days=8),
            },
            {
                "categoria": category_map["Informacion general"],
                "titulo": "Canales oficiales de contacto actualizados",
                "slug": "canales-oficiales-de-contacto-actualizados",
                "extracto": "Se actualizaron los datos institucionales para mejorar la atencion y la respuesta a consultas.",
                "contenido": (
                    "Los canales de contacto del portal fueron revisados para mantener "
                    "informacion vigente y facilitar la comunicacion con la comunidad."
                ),
                "publicado": True,
                "destacado": False,
                "fecha_publicacion": now - timedelta(days=12),
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
                    ContentFile(self.build_card_svg(item["titulo"], "#0F4C5C")),
                    save=True,
                )
        self.stdout.write("Comunicados demo listos.")

    def create_documentos(self):
        categories = [
            ("Reglamentos", "Documentos normativos y lineamientos."),
            ("Actas", "Registros de reuniones y acuerdos."),
            ("Formularios", "Plantillas y formatos de uso frecuente."),
        ]
        category_map = {}
        for name, description in categories:
            category, _ = CategoriaDocumento.objects.get_or_create(
                nombre=name,
                defaults={"descripcion": description, "activo": True},
            )
            category_map[name] = category

        documentos = [
            ("Reglamento general del portal", "reglamento-general-del-portal", "Reglamentos", True),
            ("Acta de reunion informativa", "acta-de-reunion-informativa", "Actas", True),
            ("Formulario de solicitud interna", "formulario-de-solicitud-interna", "Formularios", False),
            ("Protocolo de comunicaciones", "protocolo-de-comunicaciones", "Reglamentos", True),
            ("Ficha de actualizacion de datos", "ficha-de-actualizacion-de-datos", "Formularios", False),
        ]

        for index, (title, slug, category_name, featured) in enumerate(documentos, start=1):
            document, created = Documento.objects.get_or_create(
                slug=slug,
                defaults={
                    "categoria": category_map[category_name],
                    "titulo": title,
                    "descripcion": "Documento demo para validar descargas y organizacion por categorias.",
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
        self.stdout.write("Documentos demo listos.")

    def create_beneficios(self):
        categories = [
            ("Salud", "Beneficios orientados al bienestar y apoyo."),
            ("Educacion", "Convenios y recursos formativos."),
            ("Bienestar", "Apoyos y beneficios complementarios."),
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
                "titulo": "Convenio con centro medico asociado",
                "slug": "convenio-con-centro-medico-asociado",
                "descripcion_corta": "Atencion preferente y valores referenciales en prestaciones seleccionadas.",
                "contenido": "Beneficio demo pensado para mostrar convenios activos con informacion breve y clara.",
                "activo": True,
                "destacado": True,
                "vigencia": timezone.localdate() + timedelta(days=90),
            },
            {
                "categoria": category_map["Educacion"],
                "titulo": "Descuento en programas de capacitacion",
                "slug": "descuento-en-programas-de-capacitacion",
                "descripcion_corta": "Acceso preferente a cursos, talleres y actividades formativas.",
                "contenido": "Convenio orientado al desarrollo de capacidades y actualizacion de conocimientos.",
                "activo": True,
                "destacado": True,
                "vigencia": timezone.localdate() + timedelta(days=120),
            },
            {
                "categoria": category_map["Bienestar"],
                "titulo": "Red de apoyo en servicios complementarios",
                "slug": "red-de-apoyo-en-servicios-complementarios",
                "descripcion_corta": "Acceso a beneficios en comercios y servicios aliados.",
                "contenido": "Beneficio flexible para mostrar acuerdos con instituciones y comercios externos.",
                "activo": True,
                "destacado": False,
                "vigencia": timezone.localdate() + timedelta(days=60),
            },
            {
                "categoria": category_map["Salud"],
                "titulo": "Orientacion preventiva y jornadas tematicas",
                "slug": "orientacion-preventiva-y-jornadas-tematicas",
                "descripcion_corta": "Instancias informativas y acciones de bienestar para la comunidad.",
                "contenido": "Espacios de apoyo y orientacion con foco en prevencion y acompanamiento institucional.",
                "activo": True,
                "destacado": True,
                "vigencia": timezone.localdate() + timedelta(days=150),
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
                    ContentFile(self.build_card_svg(item["titulo"], "#1F2937")),
                    save=True,
                )
        self.stdout.write("Beneficios demo listos.")

    def build_logo_svg(self, site_name):
        return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="240" height="240" viewBox="0 0 240 240">
  <rect width="240" height="240" rx="40" fill="#0F4C5C"/>
  <circle cx="120" cy="120" r="74" fill="#EAB308" opacity="0.15"/>
  <text x="120" y="104" text-anchor="middle" font-size="26" font-family="Arial, sans-serif" fill="#ffffff">Portal</text>
  <text x="120" y="138" text-anchor="middle" font-size="26" font-family="Arial, sans-serif" fill="#ffffff">Demo</text>
  <text x="120" y="182" text-anchor="middle" font-size="12" font-family="Arial, sans-serif" fill="#d9eef2">{site_name}</text>
</svg>
""".strip().encode("utf-8")

    def build_hero_svg(self):
        return b"""
<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="900" viewBox="0 0 1280 900">
  <rect width="1280" height="900" fill="#f4fafb"/>
  <rect x="72" y="90" width="1136" height="720" rx="36" fill="#ffffff" stroke="#dbe2ea"/>
  <rect x="132" y="160" width="420" height="32" rx="16" fill="#0F4C5C" opacity="0.15"/>
  <rect x="132" y="220" width="510" height="72" rx="16" fill="#0F4C5C"/>
  <rect x="132" y="320" width="420" height="20" rx="10" fill="#1F2937" opacity="0.18"/>
  <rect x="132" y="356" width="380" height="20" rx="10" fill="#1F2937" opacity="0.14"/>
  <rect x="132" y="420" width="180" height="56" rx="18" fill="#0F4C5C"/>
  <rect x="332" y="420" width="180" height="56" rx="18" fill="#ffffff" stroke="#0F4C5C" stroke-width="3"/>
  <rect x="706" y="170" width="392" height="540" rx="28" fill="#f8fafc" stroke="#dbe2ea"/>
  <rect x="760" y="240" width="280" height="170" rx="24" fill="#0F4C5C"/>
  <rect x="760" y="446" width="280" height="28" rx="14" fill="#1F2937" opacity="0.18"/>
  <rect x="760" y="492" width="230" height="28" rx="14" fill="#1F2937" opacity="0.12"/>
  <rect x="760" y="560" width="130" height="88" rx="20" fill="#EAB308" opacity="0.25"/>
  <rect x="912" y="560" width="128" height="88" rx="20" fill="#0F4C5C" opacity="0.1"/>
</svg>
""".strip()

    def build_card_svg(self, title, color):
        return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="720" viewBox="0 0 1200 720">
  <rect width="1200" height="720" fill="#f8fafc"/>
  <rect x="60" y="60" width="1080" height="600" rx="34" fill="{color}" opacity="0.94"/>
  <rect x="120" y="130" width="220" height="18" rx="9" fill="#ffffff" opacity="0.32"/>
  <text x="120" y="250" font-size="54" font-family="Arial, sans-serif" fill="#ffffff">{title[:28]}</text>
  <rect x="120" y="310" width="420" height="18" rx="9" fill="#ffffff" opacity="0.18"/>
  <rect x="120" y="344" width="360" height="18" rx="9" fill="#ffffff" opacity="0.14"/>
  <circle cx="940" cy="220" r="90" fill="#EAB308" opacity="0.20"/>
  <circle cx="1010" cy="470" r="120" fill="#ffffff" opacity="0.08"/>
</svg>
""".strip().encode("utf-8")

    def build_document_text(self, title, category):
        return (
            f"{title}\n\n"
            f"Categoria: {category}\n\n"
            "Este archivo fue generado como documento demo para validar descargas, "
            "organizacion por categorias y contenido publico en el portal institucional.\n"
        ).encode("utf-8")
