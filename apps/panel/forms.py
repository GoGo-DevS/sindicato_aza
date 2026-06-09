from django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile

from apps.beneficios.models import Beneficio, CategoriaBeneficio
from apps.comunicados.models import Comunicado, CategoriaComunicado
from apps.documentos.models import Documento, CategoriaDocumento

LG = "form-control form-control-lg"
SEL = "form-select form-select-lg"
FILE = "form-control form-control-lg"

# ── Validacion de archivos subidos ───────────────────────────────────────────
IMG_EXT = {"jpg", "jpeg", "png", "webp", "gif"}
DOC_EXT = {"pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "odt", "txt"}
MAX_IMG = 5 * 1024 * 1024    # 5 MB
MAX_DOC = 10 * 1024 * 1024   # 10 MB


def validar_archivo(f, allowed_ext, max_size):
    """Valida extension y tamano SOLO de archivos recien subidos."""
    if not f or not isinstance(f, UploadedFile):
        return f  # vacio o archivo ya guardado: no re-validar
    nombre = (getattr(f, "name", "") or "").lower()
    ext = nombre.rsplit(".", 1)[-1] if "." in nombre else ""
    if ext not in allowed_ext:
        raise ValidationError(
            "Formato no permitido. Permitidos: %s." % ", ".join(sorted(allowed_ext))
        )
    if getattr(f, "size", 0) > max_size:
        raise ValidationError(
            "El archivo supera el limite de %d MB." % (max_size // (1024 * 1024))
        )
    return f


class ComunicadoForm(forms.ModelForm):
    class Meta:
        model = Comunicado
        fields = [
            "titulo", "categoria", "extracto", "contenido",
            "imagen", "publicado", "destacado", "fecha_publicacion",
        ]
        labels = {
            "titulo":            "Titulo del comunicado",
            "categoria":         "Categoria",
            "extracto":          "Resumen breve",
            "contenido":         "Contenido completo",
            "imagen":            "Imagen (opcional)",
            "publicado":         "Publicar en el sitio web",
            "destacado":         "Destacar en la portada",
            "fecha_publicacion": "Fecha de publicacion",
        }
        help_texts = {
            "extracto":          "Una o dos oraciones que aparecen como vista previa.",
            "publicado":         "Si no esta marcado, el comunicado no sera visible para los socios.",
            "destacado":         "Los comunicados destacados aparecen en la pagina de inicio.",
            "imagen":            "Formatos aceptados: JPG, PNG. Opcional.",
        }
        widgets = {
            "titulo":            forms.TextInput(attrs={"class": LG, "placeholder": "Ej: Convocatoria asamblea ordinaria"}),
            "categoria":         forms.Select(attrs={"class": SEL}),
            "extracto":          forms.Textarea(attrs={"class": LG, "rows": 3, "placeholder": "Resumen breve del comunicado..."}),
            "contenido":         forms.Textarea(attrs={"class": LG, "rows": 9}),
            "imagen":            forms.ClearableFileInput(attrs={"class": FILE}),
            "fecha_publicacion": forms.DateTimeInput(attrs={"class": LG, "type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.fecha_publicacion:
            self.initial["fecha_publicacion"] = self.instance.fecha_publicacion.strftime("%Y-%m-%dT%H:%M")

    def clean_imagen(self):
        return validar_archivo(self.cleaned_data.get("imagen"), IMG_EXT, MAX_IMG)


class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = [
            "titulo", "categoria", "archivo", "descripcion",
            "publico", "destacado", "fecha",
        ]
        labels = {
            "titulo":      "Nombre del documento",
            "categoria":   "Categoria",
            "archivo":     "Archivo PDF",
            "descripcion": "Descripcion breve",
            "publico":     "Visible para todos los socios",
            "destacado":   "Destacar en la portada",
            "fecha":       "Fecha del documento",
        }
        help_texts = {
            "archivo":     "Seleccione el archivo PDF que desea subir.",
            "descripcion": "Explique brevemente de que trata este documento.",
            "destacado":   "Los documentos destacados aparecen en la pagina de inicio.",
        }
        widgets = {
            "titulo":      forms.TextInput(attrs={"class": LG, "placeholder": "Ej: Estatutos del Sindicato AZA"}),
            "categoria":   forms.Select(attrs={"class": SEL}),
            "descripcion": forms.Textarea(attrs={"class": LG, "rows": 3}),
            "archivo":     forms.ClearableFileInput(attrs={"class": FILE}),
            "fecha":       forms.DateInput(attrs={"class": LG, "type": "date"}),
        }

    def clean_archivo(self):
        return validar_archivo(self.cleaned_data.get("archivo"), DOC_EXT, MAX_DOC)


class BeneficioForm(forms.ModelForm):
    class Meta:
        model = Beneficio
        fields = [
            "titulo", "categoria", "descripcion_corta", "contenido",
            "imagen", "activo", "destacado", "vigencia",
        ]
        labels = {
            "titulo":           "Nombre del beneficio",
            "categoria":        "Tipo de beneficio",
            "descripcion_corta": "Descripcion breve",
            "contenido":        "Detalle completo del beneficio",
            "imagen":           "Imagen (opcional)",
            "activo":           "Beneficio vigente",
            "destacado":        "Destacar en la portada",
            "vigencia":         "Valido hasta",
        }
        help_texts = {
            "descripcion_corta": "Una o dos oraciones que aparecen como resumen.",
            "activo":            "Si no esta marcado, el beneficio no aparecera en el sitio.",
            "destacado":         "Los beneficios destacados aparecen en la pagina de inicio.",
        }
        widgets = {
            "titulo":            forms.TextInput(attrs={"class": LG, "placeholder": "Ej: Convenio optico con descuento"}),
            "categoria":         forms.Select(attrs={"class": SEL}),
            "descripcion_corta": forms.Textarea(attrs={"class": LG, "rows": 3}),
            "contenido":         forms.Textarea(attrs={"class": LG, "rows": 7}),
            "imagen":            forms.ClearableFileInput(attrs={"class": FILE}),
            "vigencia":          forms.DateInput(attrs={"class": LG, "type": "date"}),
        }

    def clean_imagen(self):
        return validar_archivo(self.cleaned_data.get("imagen"), IMG_EXT, MAX_IMG)


# ── Formularios de categorias ─────────────────────────────────────────────────

_CAT_LABELS = {"nombre": "Nombre de la categoria", "descripcion": "Descripcion (opcional)", "activo": "Activa"}
_CAT_WIDGETS = {
    "nombre": forms.TextInput(attrs={"class": LG, "placeholder": "Ej: Asamblea, Laboral, Bienestar"}),
    "descripcion": forms.TextInput(attrs={"class": LG, "placeholder": "Breve descripcion"}),
}


class CategoriaComunicadoForm(forms.ModelForm):
    class Meta:
        model = CategoriaComunicado
        fields = ["nombre", "descripcion", "activo"]
        labels = _CAT_LABELS
        widgets = _CAT_WIDGETS


class CategoriaDocumentoForm(forms.ModelForm):
    class Meta:
        model = CategoriaDocumento
        fields = ["nombre", "descripcion", "activo"]
        labels = _CAT_LABELS
        widgets = _CAT_WIDGETS


class CategoriaBeneficioForm(forms.ModelForm):
    class Meta:
        model = CategoriaBeneficio
        fields = ["nombre", "descripcion", "activo"]
        labels = _CAT_LABELS
        widgets = _CAT_WIDGETS
