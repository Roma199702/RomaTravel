from django import forms
from django.utils import timezone

from .models import Viaje, Reserva


class ViajeForm(forms.ModelForm):

    class Meta:

        model = Viaje

        fields = [
            'destino',
            'pais',
            'fecha_salida',
            'fecha_regreso',
            'precio',
            'cupos',
            'tipo_viaje',
            'descripcion',
        ]

        labels = {
            'destino': 'Destino',
            'pais': 'País',
            'fecha_salida': 'Fecha de salida',
            'fecha_regreso': 'Fecha de regreso',
            'precio': 'Precio por persona',
            'cupos': 'Cupos disponibles',
            'tipo_viaje': 'Tipo de viaje',
            'descripcion': 'Descripción',
        }

        widgets = {

            'destino': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Cancún'
            }),

            'pais': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: México'
            }),

            'fecha_salida': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),

            'fecha_regreso': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),

            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'step': '1',
                'placeholder': 'Ej: 850000'
            }),

            'cupos': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),

            'tipo_viaje': forms.Select(attrs={
                'class': 'form-select'
            }),

            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción del viaje'
            }),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        hoy = timezone.localdate().isoformat()

        self.fields[
            'fecha_salida'
        ].widget.attrs['min'] = hoy

        self.fields[
            'fecha_regreso'
        ].widget.attrs['min'] = hoy

    def clean_fecha_salida(self):

        fecha_salida = self.cleaned_data.get(
            'fecha_salida'
        )

        if (
            fecha_salida
            and fecha_salida < timezone.localdate()
        ):

            raise forms.ValidationError(
                'La fecha de salida no puede ser anterior a hoy.'
            )

        return fecha_salida

    def clean_fecha_regreso(self):

        fecha_regreso = self.cleaned_data.get(
            'fecha_regreso'
        )

        if (
            fecha_regreso
            and fecha_regreso < timezone.localdate()
        ):

            raise forms.ValidationError(
                'La fecha de regreso no puede ser anterior a hoy.'
            )

        return fecha_regreso

    def clean(self):

        datos = super().clean()

        salida = datos.get('fecha_salida')
        regreso = datos.get('fecha_regreso')

        if salida and regreso:

            if regreso < salida:

                self.add_error(
                    'fecha_regreso',
                    'La fecha de regreso no puede ser anterior a la fecha de salida.'
                )

        return datos


class ReservaForm(forms.ModelForm):

    class Meta:

        model = Reserva

        fields = [
            'nombre',
            'rut',
            'correo',
            'cantidad_personas',
        ]

        labels = {
            'nombre': 'Nombre completo',
            'rut': 'RUT',
            'correo': 'Correo electrónico',
            'cantidad_personas': 'Cantidad de personas',
        }

        widgets = {

            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: María Pérez'
            }),

            'rut': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 12.345.678-9',
                'maxlength': '12'
            }),

            'correo': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: correo@gmail.com'
            }),

            'cantidad_personas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'value': '1'
            }),
        }

    def clean_rut(self):

        rut = self.cleaned_data.get('rut')

        if rut:
            rut = rut.strip()

        return rut