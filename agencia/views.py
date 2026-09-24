from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.db import transaction

from .models import Viaje, Reserva
from .forms import ViajeForm, ReservaForm


# =========================
# INICIO
# =========================

def inicio(request):

    return render(
        request,
        'agencia/inicio.html'
    )


# =========================
# SOBRE NOSOTROS
# =========================

def sobre_nosotros(request):

    return render(
        request,
        'agencia/sobre_nosotros.html'
    )


# =========================
# VIAJES DISPONIBLES
# =========================

def viajes_disponibles(request):

    viajes = Viaje.objects.filter(
        cupos__gt=0
    ).order_by(
        'fecha_salida'
    )

    return render(
        request,
        'agencia/viajes_disponibles.html',
        {
            'viajes': viajes
        }
    )


# =========================
# RESERVAR
# =========================

def reservar_viaje(request, id):

    viaje = get_object_or_404(
        Viaje,
        id=id
    )

    if request.method == 'POST':

        formulario = ReservaForm(
            request.POST
        )

        if formulario.is_valid():

            cantidad = formulario.cleaned_data[
                'cantidad_personas'
            ]

            if cantidad > viaje.cupos:

                formulario.add_error(
                    'cantidad_personas',
                    'No existen suficientes cupos disponibles.'
                )

            else:

                total = viaje.precio * cantidad

                with transaction.atomic():

                    reserva = formulario.save(
                        commit=False
                    )

                    reserva.viaje = viaje

                    reserva.precio_total = total

                    reserva.save()

                    viaje.cupos -= cantidad

                    viaje.save()

                return render(
                    request,
                    'agencia/reserva_exitosa.html',
                    {
                        'reserva': reserva
                    }
                )

    else:

        formulario = ReservaForm()

    return render(
        request,
        'agencia/reservar_viaje.html',
        {
            'viaje': viaje,
            'formulario': formulario
        }
    )


# =========================
# LISTA DE RESERVAS
# =========================

def lista_reservas(request):

    reservas = Reserva.objects.select_related(
        'viaje'
    ).order_by(
        '-fecha_reserva'
    )

    return render(
        request,
        'agencia/lista_reservas.html',
        {
            'reservas': reservas
        }
    )


# =========================
# ADMINISTRAR VIAJES
# =========================

def administrar_viajes(request):

    viajes = Viaje.objects.all().order_by(
        'fecha_salida'
    )

    return render(
        request,
        'agencia/administrar_viajes.html',
        {
            'viajes': viajes
        }
    )


# =========================
# CREAR VIAJE
# =========================

def crear_viaje(request):

    if request.method == 'POST':

        formulario = ViajeForm(
            request.POST
        )

        if formulario.is_valid():

            formulario.save()

            return redirect(
                'administrar_viajes'
            )

    else:

        formulario = ViajeForm()

    return render(
        request,
        'agencia/crear_viaje.html',
        {
            'formulario': formulario
        }
    )


# =========================
# EDITAR VIAJE
# =========================

def editar_viaje(request, id):

    viaje = get_object_or_404(
        Viaje,
        id=id
    )

    if request.method == 'POST':

        formulario = ViajeForm(
            request.POST,
            instance=viaje
        )

        if formulario.is_valid():

            formulario.save()

            return redirect(
                'administrar_viajes'
            )

    else:

        formulario = ViajeForm(
            instance=viaje
        )

    return render(
        request,
        'agencia/editar_viaje.html',
        {
            'formulario': formulario,
            'viaje': viaje
        }
    )


# =========================
# ELIMINAR VIAJE
# =========================

def eliminar_viaje(request, id):

    viaje = get_object_or_404(
        Viaje,
        id=id
    )

    if request.method == 'POST':

        viaje.delete()

        return redirect(
            'administrar_viajes'
        )

    return render(
        request,
        'agencia/eliminar_viaje.html',
        {
            'viaje': viaje
        }
    )
