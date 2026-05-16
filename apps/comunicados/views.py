from django.utils import timezone
from django.views.generic import DetailView, ListView

from .models import Comunicado


class ComunicadoListView(ListView):
    model = Comunicado
    template_name = "comunicados/comunicado_list.html"
    context_object_name = "comunicados"
    paginate_by = 9

    def get_queryset(self):
        return (
            Comunicado.objects.select_related("categoria")
            .filter(publicado=True, fecha_publicacion__lte=timezone.now())
            .order_by("-destacado", "-fecha_publicacion")
        )


class ComunicadoDetailView(DetailView):
    model = Comunicado
    template_name = "comunicados/comunicado_detail.html"
    context_object_name = "comunicado"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Comunicado.objects.select_related("categoria").filter(
            publicado=True,
            fecha_publicacion__lte=timezone.now(),
        )
