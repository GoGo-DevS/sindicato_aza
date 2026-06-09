from django import forms

from .models import MensajeContacto


class MensajeContactoForm(forms.ModelForm):
    # Honeypot anti-spam: campo oculto que los humanos no ven ni completan.
    # Si llega con contenido, es un bot -> se rechaza el envio.
    website = forms.CharField(
        required=False,
        label="No completar",
        widget=forms.TextInput(attrs={"tabindex": "-1", "autocomplete": "off"}),
    )

    def clean_website(self):
        if self.cleaned_data.get("website"):
            raise forms.ValidationError("Error de validacion.")
        return ""

    class Meta:
        model = MensajeContacto
        fields = ["nombre", "email", "telefono", "asunto", "mensaje"]
        widgets = {
            "nombre": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Tu nombre completo"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "nombre@correo.cl"}
            ),
            "telefono": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "+56 9 1234 5678"}
            ),
            "asunto": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Motivo del contacto"}
            ),
            "mensaje": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                    "placeholder": "Escribe tu mensaje aqui",
                }
            ),
        }
