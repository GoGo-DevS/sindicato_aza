from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import MensajeContactoForm
from .models import MensajeContacto


class ContactoView(SuccessMessageMixin, CreateView):
    model = MensajeContacto
    form_class = MensajeContactoForm
    template_name = "contacto/contacto_form.html"
    success_url = reverse_lazy("contacto:index")
    success_message = "Tu mensaje fue enviado correctamente. Te contactaremos pronto."
