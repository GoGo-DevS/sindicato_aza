from django.utils import timezone
from django.views.generic import TemplateView

from apps.beneficios.models import Beneficio
from apps.comunicados.models import Comunicado
from apps.documentos.models import Documento


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comunicados_destacados"] = (
            Comunicado.objects.select_related("categoria")
            .filter(publicado=True, fecha_publicacion__lte=timezone.now())
            .order_by("-destacado", "-fecha_publicacion")[:3]
        )
        context["documentos_destacados"] = (
            Documento.objects.select_related("categoria")
            .filter(publico=True, destacado=True, categoria__activo=True)
            .order_by("-fecha", "titulo")[:4]
        )
        context["beneficios_destacados"] = (
            Beneficio.objects.select_related("categoria")
            .filter(activo=True, destacado=True, categoria__activo=True)
            .order_by("vigencia", "titulo")[:3]
        )
        # Centro de Ayuda es solo para admins autenticados — no aparece en home
        context["capacitaciones_destacadas"] = []
        return context
