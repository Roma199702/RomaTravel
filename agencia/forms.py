from django import forms
from django.utils import timezone

from .models import Viaje, Reserva


# ==================================================
# FUNCIÓN PARA VALIDAR RUT CHILENO
# ==================================================

def validar_rut_chileno(rut):

    # Quitamos puntos, guion y espacios
    rut_limpio = (
        rut.replace('.', '')
        .replace('-', '')
        .replace(' ', '')
        .upper()
    )

    # Debe contener al menos cuerpo + dígito verificador
    if len(rut_limpio) < 2:
        raise forms.ValidationError(
            'Ingrese un RUT válido.'
        )

    cuerpo = rut_limpio[:-1]
    dv_ingresado = rut_limpio[-1]

    # El cuerpo del RUT solamente puede contener números
    if not cuerpo.isdigit():
        raise forms.ValidationError(
            'El RUT solo puede contener números, puntos y guion.'
        )

    # El dígito verificador solamente puede ser número o K
    if not (
        dv_ingresado.isdigit()
        or dv_ingresado == 'K'
    ):
        raise forms.ValidationError(
            'El dígito verificador del RUT debe ser un número o K.'
        )

    # Calcular dígito verificador
    suma = 0
    multiplicador = 2

    for numero in reversed(cuerpo):

        suma += int(numero) * multiplicador

        multiplicador += 1

        if multiplicador == 8:
            multiplicador = 2

    resto = 11 - (suma % 11)

    if resto == 11:
        dv_calculado = '0'

    elif resto == 10:
        dv_calculado = 'K'

    else:
        dv_calculado = str(resto)

    # Comparar dígito verificador
    if dv_ingresado != dv_calculado:

        raise forms.ValidationError(
            'El RUT ingresado no es válido.'
        )

    return rut


# ==================================================
# FORMULARIO VIAJE
# ==================================================

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
                'placeholder': 'Ej: Cancún',
                'maxlength': '100'
            }),

            'pais': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: México',
                'maxlength': '100'
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
                'min': '0',
                'placeholder': 'Ej: 20'
            }),

            'tipo_viaje': forms.Select(attrs={
                'class': 'form-select'
            }),

            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '3',
                'maxlength': '100',
                'placeholder': 'Descripción del viaje (máximo 100 caracteres)'
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

        fecha = self.cleaned_data.get(
            'fecha_salida'
        )

        if fecha and fecha < timezone.localdate():

            raise forms.ValidationError(
                'La fecha de salida no puede ser anterior a hoy.'
            )

        return fecha

    def clean_fecha_regreso(self):

        fecha = self.cleaned_data.get(
            'fecha_regreso'
        )

        if fecha and fecha < timezone.localdate():

            raise forms.ValidationError(
                'La fecha de regreso no puede ser anterior a hoy.'
            )

        return fecha

    def clean(self):

        datos = super().clean()

        salida = datos.get(
            'fecha_salida'
        )

        regreso = datos.get(
            'fecha_regreso'
        )

        if salida and regreso:

            if regreso < salida:

                self.add_error(
                    'fecha_regreso',
                    'La fecha de regreso no puede ser anterior a la fecha de salida.'
                )

        return datos


# ==================================================
# FORMULARIO CREAR RESERVA
# ==================================================

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
                'placeholder': 'Ej: María Pérez',
                'maxlength': '100'
            }),

            'rut': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 12.345.678-5',
                'maxlength': '12'
            }),

            'correo': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: correo@gmail.com',
                'maxlength': '100'
            }),

            'cantidad_personas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
        }

    def clean_rut(self):

        rut = self.cleaned_data.get('rut')

        if not rut:
            return rut

        rut = rut.strip()

        validar_rut_chileno(rut)

        return rut


# ==================================================
# FORMULARIO EDITAR RESERVA
# ==================================================

class EditarReservaForm(forms.ModelForm):

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
                'maxlength': '100'
            }),

            'rut': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 12.345.678-5',
                'maxlength': '12'
            }),

            'correo': forms.EmailInput(attrs={
                'class': 'form-control',
                'maxlength': '100'
            }),

            'cantidad_personas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
        }

    def clean_rut(self):

        rut = self.cleaned_data.get('rut')

        if not rut:
            return rut

        rut = rut.strip()

        validar_rut_chileno(rut)

        return rut