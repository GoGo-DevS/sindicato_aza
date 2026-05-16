from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.beneficios.models import Beneficio, CategoriaBeneficio
from apps.capacitacion.models import Capacitacion, CategoriaCapacitacion
from apps.comunicados.models import CategoriaComunicado, Comunicado
from apps.documentos.models import CategoriaDocumento, Documento


class Command(BaseCommand):
    help = "Carga datos de ejemplo para el portal Sindicato AZA."

    def handle(self, *args, **options):
        self.create_comunicados()
        self.create_documentos()
        self.create_beneficios()
        self.create_capacitaciones()
        self.stdout.write(self.style.SUCCESS("Datos AZA cargados correctamente."))

    def create_comunicados(self):
        categorias_data = [
            ("Administrativo", "Avisos y gestiones administrativas del sindicato."),
            ("Laboral", "Informacion sobre condiciones laborales y negociaciones."),
            ("Bienestar", "Actividades y programas de bienestar para los socios."),
        ]
        cat_map = {}
        for nombre, desc in categorias_data:
            cat, _ = CategoriaComunicado.objects.get_or_create(
                nombre=nombre,
                defaults={"descripcion": desc, "activo": True},
            )
            cat_map[nombre] = cat

        now = timezone.now()
        comunicados = [
            {
                "categoria": cat_map["Administrativo"],
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
                "categoria": cat_map["Laboral"],
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
                "categoria": cat_map["Bienestar"],
                "titulo": "Programa de actividades primer semestre",
                "slug": "programa-actividades-primer-semestre",
                "extracto": "Conoce el calendario de actividades de bienestar planificadas para los socios y sus familias.",
                "contenido": (
                    "El area de bienestar del sindicato ha preparado un programa de actividades "
                    "que incluye talleres, jornadas recreativas y beneficios para los socios. "
                    "Revisa el calendario adjunto y reserva tu lugar."
                ),
                "publicado": True,
                "destacado": True,
                "fecha_publicacion": now - timedelta(days=10),
            },
        ]

        for item in comunicados:
            Comunicado.objects.get_or_create(slug=item["slug"], defaults=item)
        self.stdout.write("  Comunicados AZA listos.")

    def create_documentos(self):
        categorias_data = [
            ("Reglamentos", "Documentos normativos internos del sindicato."),
            ("Formularios", "Plantillas y formularios de uso frecuente."),
            ("Actas", "Actas de asambleas y reuniones de directorio."),
        ]
        cat_map = {}
        for nombre, desc in categorias_data:
            cat, _ = CategoriaDocumento.objects.get_or_create(
                nombre=nombre,
                defaults={"descripcion": desc, "activo": True},
            )
            cat_map[nombre] = cat

        today = timezone.localdate()
        documentos = [
            {
                "categoria": cat_map["Reglamentos"],
                "titulo": "Estatutos del Sindicato AZA",
                "slug": "estatutos-sindicato-aza",
                "descripcion": "Estatutos vigentes que rigen el funcionamiento del sindicato.",
                "publico": True,
                "destacado": True,
                "fecha": today - timedelta(days=30),
            },
            {
                "categoria": cat_map["Formularios"],
                "titulo": "Formulario de solicitud de beneficio",
                "slug": "formulario-solicitud-beneficio",
                "descripcion": "Formato para solicitar beneficios sociales disponibles para los socios.",
                "publico": True,
                "destacado": False,
                "fecha": today - timedelta(days=15),
            },
            {
                "categoria": cat_map["Actas"],
                "titulo": "Acta asamblea general extraordinaria",
                "slug": "acta-asamblea-general-extraordinaria",
                "descripcion": "Registro de acuerdos de la ultima asamblea general extraordinaria.",
                "publico": True,
                "destacado": True,
                "fecha": today - timedelta(days=7),
            },
        ]

        from django.core.files.base import ContentFile

        for item in documentos:
            slug = item["slug"]
            titulo = item["titulo"]
            categoria_nombre = item["categoria"].nombre
            doc, created = Documento.objects.get_or_create(slug=slug, defaults=item)
            if created:
                doc.archivo.save(
                    f"{slug}.txt",
                    ContentFile(
                        f"{titulo}\n\nCategoria: {categoria_nombre}\n\n"
                        "Documento de ejemplo generado para el portal Sindicato AZA.\n".encode("utf-8")
                    ),
                    save=True,
                )
        self.stdout.write("  Documentos AZA listos.")

    def create_beneficios(self):
        categorias_data = [
            ("Salud", "Convenios y beneficios de salud para socios."),
            ("Capacitacion", "Beneficios en programas formativos."),
            ("Bienestar", "Beneficios complementarios de bienestar."),
        ]
        cat_map = {}
        for nombre, desc in categorias_data:
            cat, _ = CategoriaBeneficio.objects.get_or_create(
                nombre=nombre,
                defaults={"descripcion": desc, "activo": True},
            )
            cat_map[nombre] = cat

        today = timezone.localdate()
        beneficios = [
            {
                "categoria": cat_map["Salud"],
                "titulo": "Convenio optico con descuento para socios",
                "slug": "convenio-optico-descuento-socios",
                "descripcion_corta": "Descuento del 30% en lentes y examenes de vista en opticas convenidas.",
                "contenido": "Los socios y su grupo familiar acceden a descuentos especiales en opticas asociadas.",
                "activo": True,
                "destacado": True,
                "vigencia": today + timedelta(days=180),
            },
            {
                "categoria": cat_map["Capacitacion"],
                "titulo": "Acceso a plataforma de e-learning",
                "slug": "acceso-plataforma-elearning",
                "descripcion_corta": "Acceso gratuito a cursos en linea de capacitacion profesional.",
                "contenido": "Los socios tienen acceso ilimitado a la plataforma de cursos en linea durante el periodo de vigencia.",
                "activo": True,
                "destacado": True,
                "vigencia": today + timedelta(days=120),
            },
            {
                "categoria": cat_map["Bienestar"],
                "titulo": "Caja de navidad para socios activos",
                "slug": "caja-navidad-socios-activos",
                "descripcion_corta": "Entrega de caja de navidad anual para todos los socios activos.",
                "contenido": "El sindicato entrega una caja de navidad a todos los socios con cotizaciones al dia.",
                "activo": True,
                "destacado": True,
                "vigencia": today + timedelta(days=220),
            },
            {
                "categoria": cat_map["Salud"],
                "titulo": "Seguro complementario de salud",
                "slug": "seguro-complementario-salud",
                "descripcion_corta": "Reembolso de gastos medicos para socios y su grupo familiar.",
                "contenido": "Cobertura complementaria que reimbolsa gastos medicos, dentales y de hospitalizacion.",
                "activo": True,
                "destacado": False,
                "vigencia": today + timedelta(days=300),
            },
        ]

        for item in beneficios:
            Beneficio.objects.get_or_create(slug=item["slug"], defaults=item)
        self.stdout.write("  Beneficios AZA listos.")

    def create_capacitaciones(self):
        categorias_data = [
            ("Tecnica", "Capacitaciones de habilidades tecnicas y operativas."),
            ("Liderazgo", "Desarrollo de habilidades de liderazgo y gestion."),
            ("Seguridad", "Capacitaciones en seguridad y salud ocupacional."),
        ]
        cat_map = {}
        for nombre, desc in categorias_data:
            cat, _ = CategoriaCapacitacion.objects.get_or_create(
                nombre=nombre,
                defaults={"descripcion": desc, "activo": True},
            )
            cat_map[nombre] = cat

        today = timezone.localdate()
        capacitaciones = [
            {
                "categoria": cat_map["Tecnica"],
                "titulo": "Manejo de herramientas digitales para el trabajo",
                "slug": "manejo-herramientas-digitales-trabajo",
                "descripcion_corta": "Curso practico sobre uso de plataformas digitales en el entorno laboral.",
                "contenido": (
                    "Este curso cubre el uso de herramientas digitales de uso frecuente en el trabajo: "
                    "hojas de calculo, procesadores de texto, correo electronico y plataformas colaborativas. "
                    "Orientado a socios que quieran mejorar su productividad digital."
                ),
                "modalidad": "presencial",
                "duracion": "8 horas",
                "fecha": today + timedelta(days=14),
                "cupos": 20,
                "activo": True,
                "destacado": True,
            },
            {
                "categoria": cat_map["Liderazgo"],
                "titulo": "Liderazgo sindical y representacion efectiva",
                "slug": "liderazgo-sindical-representacion-efectiva",
                "descripcion_corta": "Taller para dirigentes y socios interesados en fortalecer la representacion sindical.",
                "contenido": (
                    "Taller intensivo sobre comunicacion efectiva, negociacion, gestion de conflictos "
                    "y representacion sindical. Incluye casos practicos y metodologias participativas."
                ),
                "modalidad": "hibrida",
                "duracion": "16 horas",
                "fecha": today + timedelta(days=21),
                "cupos": 15,
                "activo": True,
                "destacado": True,
            },
            {
                "categoria": cat_map["Seguridad"],
                "titulo": "Prevencion de riesgos en el lugar de trabajo",
                "slug": "prevencion-riesgos-lugar-trabajo",
                "descripcion_corta": "Capacitacion obligatoria en seguridad y salud ocupacional segun normativa vigente.",
                "contenido": (
                    "Capacitacion en identificacion de riesgos, uso de elementos de proteccion personal, "
                    "procedimientos de emergencia y normativa legal aplicable. "
                    "Certificacion incluida al finalizar el curso."
                ),
                "modalidad": "online",
                "duracion": "4 horas",
                "fecha": today + timedelta(days=7),
                "cupos": 50,
                "activo": True,
                "destacado": True,
            },
        ]

        for item in capacitaciones:
            Capacitacion.objects.get_or_create(slug=item["slug"], defaults=item)
        self.stdout.write("  Capacitaciones AZA listas.")
