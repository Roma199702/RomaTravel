from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.db import transaction

from .models import Viaje, Reserva

from .forms import (
    ViajeForm,
    ReservaForm,
    EditarReservaForm
)


# ==================================================
# PÁGINA PRINCIPAL
# ==================================================

def inicio(request):

    return render(
        request,
        'agencia/inicio.html'
    )


# ==================================================
# SOBRE NOSOTROS
# ==================================================

def sobre_nosotros(request):

    return render(
        request,
        'agencia/sobre_nosotros.html'
    )


# ==================================================
# VIAJES DISPONIBLES
# ==================================================

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


# ==================================================
# CREAR RESERVA
# ==================================================

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

                with transaction.atomic():

                    total = (
                        viaje.precio
                        * cantidad
                    )

                    reserva = formulario.save(
                        commit=False
                    )

                    reserva.viaje = viaje

                    reserva.precio_total = total

                    reserva.save()

                    viaje.cupos = (
                        viaje.cupos
                        - cantidad
                    )

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


# ==================================================
# LISTAR RESERVAS
# ==================================================

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


# ==================================================
# EDITAR RESERVA
# ==================================================

def editar_reserva(request, id):

    reserva = get_object_or_404(
        Reserva,
        id=id
    )

    viaje = reserva.viaje

    cantidad_anterior = (
        reserva.cantidad_personas
    )

    if request.method == 'POST':

        formulario = EditarReservaForm(
            request.POST,
            instance=reserva
        )

        if formulario.is_valid():

            nueva_cantidad = (
                formulario.cleaned_data[
                    'cantidad_personas'
                ]
            )

            # Cupos que realmente están disponibles,
            # considerando los que ya pertenecían
            # a esta reserva.

            cupos_disponibles = (
                viaje.cupos
                + cantidad_anterior
            )

            if nueva_cantidad > cupos_disponibles:

                formulario.add_error(
                    'cantidad_personas',
                    'No existen suficientes cupos disponibles.'
                )

            else:

                with transaction.atomic():

                    # Primero devolvemos los cupos
                    # de la reserva anterior.

                    viaje.cupos = (
                        viaje.cupos
                        + cantidad_anterior
                    )

                    # Después descontamos
                    # la nueva cantidad.

                    viaje.cupos = (
                        viaje.cupos
                        - nueva_cantidad
                    )

                    viaje.save()

                    reserva_editada = (
                        formulario.save(
                            commit=False
                        )
                    )

                    reserva_editada.precio_total = (
                        viaje.precio
                        * nueva_cantidad
                    )

                    reserva_editada.save()

                return redirect(
                    'lista_reservas'
                )

    else:

        formulario = EditarReservaForm(
            instance=reserva
        )

    return render(
        request,
        'agencia/editar_reserva.html',
        {
            'formulario': formulario,
            'reserva': reserva
        }
    )


# ==================================================
# ELIMINAR RESERVA
# ==================================================

def eliminar_reserva(request, id):

    reserva = get_object_or_404(
        Reserva,
        id=id
    )

    if request.method == 'POST':

        with transaction.atomic():

            viaje = reserva.viaje

            # Al eliminar la reserva,
            # devolvemos sus cupos.

            viaje.cupos = (
                viaje.cupos
                + reserva.cantidad_personas
            )

            viaje.save()

            reserva.delete()

        return redirect(
            'lista_reservas'
        )

    return render(
        request,
        'agencia/eliminar_reserva.html',
        {
            'reserva': reserva
        }
    )


# ==================================================
# CRUD PRINCIPAL: VIAJE
# CONSULTAR
# ==================================================

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


# ==================================================
# CRUD PRINCIPAL: VIAJE
# CREAR
# ==================================================

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


# ==================================================
# CRUD PRINCIPAL: VIAJE
# EDITAR
# ==================================================

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


# ==================================================
# CRUD PRINCIPAL: VIAJE
# ELIMINAR
# ==================================================

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