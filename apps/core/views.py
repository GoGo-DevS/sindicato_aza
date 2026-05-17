from django.utils import timezone
from django.views.generic import TemplateView

from apps.beneficios.models import Beneficio
from apps.comunicados.models import Comunicado
from apps.documentos.models import Documento


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()

        comunicados_qs = Comunicado.objects.filter(
            publicado=True, fecha_publicacion__lte=now
        )
        documentos_qs = Documento.objects.filter(
            publico=True, categoria__activo=True
        )
        beneficios_qs = Beneficio.objects.filter(
            activo=True, categoria__activo=True
        )

        context["comunicados_destacados"] = (
            comunicados_qs
            .select_related("categoria")
            .order_by("-destacado", "-fecha_publicacion")[:3]
        )
        context["documentos_destacados"] = (
            documentos_qs
            .select_related("categoria")
            .filter(destacado=True)
            .order_by("-fecha", "titulo")[:4]
        )
        context["beneficios_destacados"] = (
            beneficios_qs
            .select_related("categoria")
            .filter(destacado=True)
            .order_by("vigencia", "titulo")[:3]
        )

        context["total_comunicados"] = comunicados_qs.count()
        context["total_documentos"] = documentos_qs.count()
        context["total_beneficios"] = beneficios_qs.count()

        return context
