from django import forms
from .models import Prestamo


class PrestamoForm(forms.ModelForm):
    # Formulario para crear y editar prestamos desde la interfaz web.

    class Meta:
        model = Prestamo
        fields = ["nombre_usuario", "nombre_libro", "fecha_devolucion_esperada", "prestamo_activo"]
        widgets = {
            # Clases de Bootstrap directamente en los widgets
            "nombre_usuario": forms.Select(attrs={"class": "form-select"}),
            "nombre_libro": forms.Select(attrs={"class": "form-select"}),
            "fecha_devolucion_esperada": forms.DateInput(
                attrs={"class": "form-control", "type": "date"},
                format="%Y-%m-%d",
            ),
            "prestamo_activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_fecha_devolucion_esperada(self):
        # Se valida que la fecha de devolucion no sea en el pasado
        from datetime import date

        fecha = self.cleaned_data.get("fecha_devolucion_esperada")
        if fecha and fecha < date.today():
            raise forms.ValidationError("La fecha de devolución no puede ser en el pasado.")
        return fecha
