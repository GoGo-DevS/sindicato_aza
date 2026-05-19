import os
from datetime import date, timedelta

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import models
from django.utils import timezone

from apps.beneficios.models import Beneficio, CategoriaBeneficio
from apps.comunicados.models import CategoriaComunicado, Comunicado
from apps.documentos.models import CategoriaDocumento, Documento


class Command(BaseCommand):
    help = "Carga datos realistas para video de presentacion del portal Sindicato AZA."

    def handle(self, *args, **options):
        self._clean_qa_data()
        self._create_comunicados()
        self._create_documentos()
        self._create_beneficios()

        total_c = Comunicado.objects.filter(publicado=True).count()
        total_d = Documento.objects.filter(publico=True).count()
        total_b = Beneficio.objects.filter(activo=True).count()

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("[OK] Web AZA lista para grabar video"))
        self.stdout.write(self.style.SUCCESS(
            f"[OK] Comunicados: {total_c} | Documentos: {total_d} | Beneficios: {total_b}"
        ))
        self.stdout.write(self.style.SUCCESS("[OK] URLs listas para el recorrido del video"))

    # ── Limpieza ────────────────────────────────────────────────────────────────

    def _clean_qa_data(self):
        deleted_b, _ = Beneficio.objects.filter(titulo__icontains="QA").delete()
        deleted_d, _ = Documento.objects.filter(titulo__icontains="QA").delete()
        deleted_c, _ = Comunicado.objects.filter(titulo__icontains="QA").delete()
        total = deleted_b + deleted_d + deleted_c
        if total:
            self.stdout.write(f"Datos QA eliminados: {total} registros.")
        else:
            self.stdout.write("No habia datos QA.")

    # ── Comunicados ─────────────────────────────────────────────────────────────

    def _create_comunicados(self):
        cats = {
            "Administrativo": "Avisos y gestiones administrativas del sindicato.",
            "Laboral": "Informacion sobre condiciones laborales y negociaciones.",
            "Bienestar": "Actividades y programas de bienestar para los socios.",
        }
        cat_map = {}
        for nombre, desc in cats.items():
            obj, _ = CategoriaComunicado.objects.get_or_create(
                nombre=nombre, defaults={"descripcion": desc, "activo": True}
            )
            cat_map[nombre] = obj

        now = timezone.now()

        comunicados = [
            {
                "slug": "convocatoria-asamblea-ordinaria-de-socios",
                "titulo": "Convocatoria asamblea ordinaria de socios",
                "categoria": cat_map["Administrativo"],
                "extracto": (
                    "Se convoca a todos los socios a la asamblea ordinaria del mes de mayo "
                    "para revisar el balance anual, elegir nueva directiva y votar propuestas de mejora."
                ),
                "contenido": (
                    "Se convoca a todos los socios a la asamblea ordinaria del mes de mayo "
                    "para revisar el balance anual, elegir nueva directiva y votar propuestas "
                    "de mejora. La reunion se realizara en las instalaciones AZA el dia "
                    "viernes 23 de mayo a las 18:00 hrs."
                ),
                "publicado": True,
                "destacado": True,
                "fecha_publicacion": now - timedelta(days=5),
                "color_svg": "#1565C0",
            },
            {
                "slug": "actualizacion-de-procedimientos-internos-2026",
                "titulo": "Actualizacion de procedimientos internos 2026",
                "categoria": cat_map["Administrativo"],
                "extracto": (
                    "A partir del 1 de junio entran en vigencia los nuevos procedimientos "
                    "internos aprobados en asamblea extraordinaria. El documento completo "
                    "esta disponible en la seccion de documentos."
                ),
                "contenido": (
                    "Se informa a todos los socios que a partir del 1 de junio entran en "
                    "vigencia los nuevos procedimientos internos aprobados en asamblea "
                    "extraordinaria. El documento completo esta disponible en la seccion "
                    "de documentos."
                ),
                "publicado": True,
                "destacado": False,
                "fecha_publicacion": now - timedelta(days=12),
                "color_svg": None,
            },
            {
                "slug": "actualizacion-de-convenio-colectivo-vigente",
                "titulo": "Actualizacion de convenio colectivo vigente",
                "categoria": cat_map["Laboral"],
                "extracto": (
                    "Se informa sobre los acuerdos alcanzados en la ultima ronda de "
                    "negociacion colectiva. Los nuevos beneficios entran en vigencia "
                    "a partir del proximo mes."
                ),
                "contenido": (
                    "Se informa sobre los acuerdos alcanzados en la ultima ronda de "
                    "negociacion colectiva. Los nuevos beneficios entran en vigencia "
                    "a partir del proximo mes. Revisa el convenio completo en la "
                    "seccion de documentos."
                ),
                "publicado": True,
                "destacado": True,
                "fecha_publicacion": now - timedelta(days=8),
                "color_svg": "#00695C",
            },
            {
                "slug": "resultados-mesa-de-trabajo-con-empresa-aza",
                "titulo": "Resultados mesa de trabajo con empresa AZA",
                "categoria": cat_map["Laboral"],
                "extracto": (
                    "Tras tres semanas de reuniones con la empresa, la directiva informa "
                    "los acuerdos logrados en materia de condiciones laborales, beneficios "
                    "y protocolo de seguridad."
                ),
                "contenido": (
                    "Tras tres semanas de reuniones con la empresa, la directiva informa "
                    "los acuerdos logrados en materia de condiciones laborales, beneficios "
                    "y protocolo de seguridad."
                ),
                "publicado": True,
                "destacado": False,
                "fecha_publicacion": now - timedelta(days=20),
                "color_svg": None,
            },
            {
                "slug": "programa-de-actividades-primer-semestre-2026",
                "titulo": "Programa de actividades primer semestre 2026",
                "categoria": cat_map["Bienestar"],
                "extracto": (
                    "Se publica el calendario completo de actividades de bienestar "
                    "planificadas para el primer semestre: talleres de salud, actividades "
                    "familiares y jornadas deportivas."
                ),
                "contenido": (
                    "Se publica el calendario completo de actividades de bienestar "
                    "planificadas para el primer semestre. Incluye talleres de salud, "
                    "actividades familiares y jornadas deportivas para socios y sus familias."
                ),
                "publicado": True,
                "destacado": True,
                "fecha_publicacion": now - timedelta(days=3),
                "color_svg": "#2E7D32",
            },
            {
                "slug": "jornada-de-salud-preventiva-inscripciones-abiertas",
                "titulo": "Jornada de salud preventiva - inscripciones abiertas",
                "categoria": cat_map["Bienestar"],
                "extracto": (
                    "El sindicato organiza una jornada gratuita de salud preventiva con "
                    "examenes basicos, atencion medica y orientacion nutricional para "
                    "socios y su grupo familiar directo."
                ),
                "contenido": (
                    "El sindicato organiza una jornada gratuita de salud preventiva con "
                    "examenes basicos, atencion medica y orientacion nutricional para "
                    "todos los socios y su grupo familiar directo."
                ),
                "publicado": True,
                "destacado": False,
                "fecha_publicacion": now - timedelta(days=15),
                "color_svg": None,
            },
        ]

        for item in comunicados:
            color = item.pop("color_svg")
            slug = item["slug"]
            obj, created = Comunicado.objects.update_or_create(
                slug=slug, defaults=item
            )
            if created and color:
                obj.imagen.save(
                    f"{slug}.svg",
                    ContentFile(self._svg_comunicado(obj.titulo, color)),
                    save=True,
                )

        self.stdout.write("Comunicados listos.")

    # ── Documentos ──────────────────────────────────────────────────────────────

    def _create_documentos(self):
        cats = {
            "Reglamentos": "Documentos normativos internos del sindicato.",
            "Formularios": "Plantillas y formularios de uso frecuente.",
            "Actas": "Registros de asambleas y reuniones de directorio.",
        }
        cat_map = {}
        for nombre, desc in cats.items():
            obj, _ = CategoriaDocumento.objects.get_or_create(
                nombre=nombre, defaults={"descripcion": desc, "activo": True}
            )
            cat_map[nombre] = obj

        hoy = timezone.localdate()
        documentos = [
            {
                "slug": "estatutos-del-sindicato-aza",
                "titulo": "Estatutos del Sindicato AZA",
                "categoria": cat_map["Reglamentos"],
                "descripcion": "Documento fundacional que rige el funcionamiento del sindicato.",
                "publico": True,
                "destacado": True,
                "fecha": hoy - timedelta(days=1),
            },
            {
                "slug": "reglamento-interno-de-funcionamiento",
                "titulo": "Reglamento interno de funcionamiento",
                "categoria": cat_map["Reglamentos"],
                "descripcion": "Normas internas de operacion y conducta del sindicato.",
                "publico": True,
                "destacado": False,
                "fecha": hoy - timedelta(days=2),
            },
            {
                "slug": "formulario-de-solicitud-de-beneficios",
                "titulo": "Formulario de solicitud de beneficios",
                "categoria": cat_map["Formularios"],
                "descripcion": "Solicitud formal para acceder a los beneficios disponibles.",
                "publico": True,
                "destacado": True,
                "fecha": hoy - timedelta(days=3),
            },
            {
                "slug": "formulario-de-incorporacion-de-socios",
                "titulo": "Formulario de incorporacion de socios",
                "categoria": cat_map["Formularios"],
                "descripcion": "Formulario para nuevos socios que desean incorporarse al sindicato.",
                "publico": True,
                "destacado": False,
                "fecha": hoy - timedelta(days=4),
            },
            {
                "slug": "acta-asamblea-general-ordinaria-marzo-2026",
                "titulo": "Acta asamblea general ordinaria marzo 2026",
                "categoria": cat_map["Actas"],
                "descripcion": "Registro oficial de acuerdos de la asamblea del mes de marzo.",
                "publico": True,
                "destacado": True,
                "fecha": hoy - timedelta(days=5),
            },
        ]

        for item in documentos:
            slug = item["slug"]
            titulo = item["titulo"]
            categoria_nombre = item["categoria"].nombre
            obj, created = Documento.objects.update_or_create(
                slug=slug, defaults=item
            )
            if created:
                pdf_content = (
                    b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
                    b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
                    + f"% {titulo} — Sindicato AZA — Categoria: {categoria_nombre}\n".encode()
                )
                obj.archivo.save(f"{slug}.pdf", ContentFile(pdf_content), save=True)

        self.stdout.write("Documentos listos.")

    # ── Beneficios ──────────────────────────────────────────────────────────────

    def _create_beneficios(self):
        cats = {
            "Salud": "Convenios y beneficios de salud para socios.",
            "Educacion": "Beneficios en programas formativos y becas.",
            "Bienestar": "Beneficios complementarios de bienestar.",
        }
        cat_map = {}
        for nombre, desc in cats.items():
            obj, _ = CategoriaBeneficio.objects.get_or_create(
                nombre=nombre, defaults={"descripcion": desc, "activo": True}
            )
            cat_map[nombre] = obj

        beneficios = [
            {
                "slug": "convenio-con-centro-medico-asociado",
                "titulo": "Convenio con centro medico asociado",
                "categoria": cat_map["Salud"],
                "descripcion_corta": (
                    "Atencion preferente y valores referenciales en prestaciones seleccionadas."
                ),
                "contenido": (
                    "El sindicato mantiene convenio con red de centros medicos que ofrece "
                    "a los socios y su grupo familiar atencion medica preferente, descuentos "
                    "en consultas y examenes, y acceso a especialistas con menor tiempo de espera."
                ),
                "activo": True,
                "destacado": True,
                "vigencia": date(2026, 12, 31),
            },
            {
                "slug": "seguro-de-vida-colectivo",
                "titulo": "Seguro de vida colectivo",
                "categoria": cat_map["Salud"],
                "descripcion_corta": (
                    "Cobertura de vida y accidentes para todos los socios y sus beneficiarios."
                ),
                "contenido": (
                    "El sindicato gestiona una poliza de seguro de vida colectivo que cubre "
                    "a todos los socios activos y sus beneficiarios directos ante fallecimiento "
                    "o accidente grave, asegurando proteccion economica a las familias."
                ),
                "activo": True,
                "destacado": True,
                "vigencia": date(2026, 12, 31),
            },
            {
                "slug": "descuento-en-programas-de-capacitacion",
                "titulo": "Descuento en programas de capacitacion",
                "categoria": cat_map["Educacion"],
                "descripcion_corta": (
                    "Acceso preferencial y descuentos en instituciones educativas convenidas."
                ),
                "contenido": (
                    "Los socios acceden a descuentos en programas de capacitacion y formacion "
                    "profesional en instituciones convenidas, incluyendo cursos tecnicos, "
                    "diplomaturas y talleres de desarrollo personal."
                ),
                "activo": True,
                "destacado": True,
                "vigencia": date(2026, 6, 30),
            },
            {
                "slug": "becas-de-estudio-para-hijos-de-socios",
                "titulo": "Becas de estudio para hijos de socios",
                "categoria": cat_map["Educacion"],
                "descripcion_corta": (
                    "Apoyo economico anual para estudios superiores de hijos de socios activos."
                ),
                "contenido": (
                    "El sindicato entrega anualmente becas de apoyo economico a hijos de "
                    "socios activos que ingresan o continuan estudios de educacion superior, "
                    "tecnica o universitaria, segun criterios de merito y necesidad."
                ),
                "activo": True,
                "destacado": False,
                "vigencia": date(2026, 11, 30),
            },
            {
                "slug": "red-de-apoyo-en-servicios-complementarios",
                "titulo": "Red de apoyo en servicios complementarios",
                "categoria": cat_map["Bienestar"],
                "descripcion_corta": (
                    "Acceso a servicios de optica, dental y farmacias con precios preferenciales."
                ),
                "contenido": (
                    "Red de prestadores convenidos que ofrece descuentos en optica, servicios "
                    "dentales y farmacias a todos los socios y su grupo familiar, contribuyendo "
                    "al bienestar integral de la comunidad sindical."
                ),
                "activo": True,
                "destacado": True,
                "vigencia": date(2026, 12, 31),
            },
            {
                "slug": "orientacion-preventiva-y-jornadas-tematicas",
                "titulo": "Orientacion preventiva y jornadas tematicas",
                "categoria": cat_map["Bienestar"],
                "descripcion_corta": (
                    "Talleres y jornadas gratuitas de salud mental, nutricion y bienestar familiar."
                ),
                "contenido": (
                    "El sindicato organiza periodicamente talleres y jornadas tematicas "
                    "de caracter preventivo en areas de salud mental, nutricion y bienestar "
                    "familiar, abiertas a todos los socios y sus familias sin costo adicional."
                ),
                "activo": True,
                "destacado": False,
                "vigencia": date(2026, 9, 30),
            },
        ]

        media_beneficios = os.path.join(settings.MEDIA_ROOT, "beneficios")
        colores_svg = {
            "Salud": "#1565C0",
            "Educacion": "#6A1B9A",
            "Bienestar": "#2E7D32",
        }

        for item in beneficios:
            slug = item["slug"]
            cat_nombre = item["categoria"].nombre
            obj, created = Beneficio.objects.update_or_create(
                slug=slug, defaults=item
            )
            if not obj.imagen:
                existing_path = os.path.join(media_beneficios, f"{slug}.svg")
                if os.path.exists(existing_path):
                    Beneficio.objects.filter(pk=obj.pk).update(imagen=f"beneficios/{slug}.svg")
                else:
                    color = colores_svg.get(cat_nombre, "#263238")
                    obj.imagen.save(
                        f"{slug}.svg",
                        ContentFile(self._svg_beneficio(obj.titulo, color)),
                        save=True,
                    )

        self.stdout.write("Beneficios listos.")

    # ── SVG builders ────────────────────────────────────────────────────────────

    def _svg_comunicado(self, titulo, color):
        label = titulo[:32]
        return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="480" viewBox="0 0 1200 480">
  <rect width="1200" height="480" fill="{color}"/>
  <rect x="0" y="0" width="1200" height="480" fill="url(#g1)" opacity="0.35"/>
  <defs>
    <linearGradient id="g1" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.20"/>
    </linearGradient>
  </defs>
  <circle cx="980" cy="80" r="200" fill="#ffffff" opacity="0.06"/>
  <circle cx="100" cy="400" r="160" fill="#ffffff" opacity="0.05"/>
  <rect x="72" y="180" width="48" height="48" rx="12" fill="#ffffff" opacity="0.18"/>
  <line x1="72" y1="264" x2="600" y2="264" stroke="#ffffff" stroke-width="2" opacity="0.18"/>
  <text x="72" y="164" font-family="Arial, sans-serif" font-size="16" fill="#ffffff" opacity="0.70" font-weight="600" letter-spacing="3">SINDICATO AZA — COMUNICADO OFICIAL</text>
  <text x="72" y="340" font-family="Arial Black, Arial, sans-serif" font-size="52" fill="#ffffff" font-weight="900">{label}</text>
  <rect x="72" y="390" width="180" height="4" rx="2" fill="#ffffff" opacity="0.40"/>
</svg>""".encode("utf-8")

    def _svg_beneficio(self, titulo, color):
        label = titulo[:30]
        return f"""<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600">
  <rect width="800" height="600" fill="#f8fafc"/>
  <rect x="40" y="40" width="720" height="520" rx="28" fill="{color}" opacity="0.92"/>
  <circle cx="660" cy="160" r="120" fill="#ffffff" opacity="0.08"/>
  <circle cx="120" cy="480" r="90" fill="#ffffff" opacity="0.06"/>
  <text x="80" y="240" font-family="Arial, sans-serif" font-size="36" fill="#ffffff" font-weight="700">{label}</text>
  <rect x="80" y="280" width="340" height="6" rx="3" fill="#ffffff" opacity="0.25"/>
  <rect x="80" y="304" width="260" height="6" rx="3" fill="#ffffff" opacity="0.18"/>
</svg>""".encode("utf-8")
