from django.urls import path

from . import views


urlpatterns = [

    path(
        '',
        views.inicio,
        name='inicio'
    ),

    path(
        'sobre-nosotros/',
        views.sobre_nosotros,
        name='sobre_nosotros'
    ),

    path(
        'viajes/',
        views.viajes_disponibles,
        name='viajes_disponibles'
    ),

    path(
        'viajes/reservar/<int:id>/',
        views.reservar_viaje,
        name='reservar_viaje'
    ),

    path(
        'reservas/',
        views.lista_reservas,
        name='lista_reservas'
    ),

    path(
        'administrar/',
        views.administrar_viajes,
        name='administrar_viajes'
    ),

    path(
        'administrar/crear/',
        views.crear_viaje,
        name='crear_viaje'
    ),

    path(
        'administrar/editar/<int:id>/',
        views.editar_viaje,
        name='editar_viaje'
    ),

    path(
        'administrar/eliminar/<int:id>/',
        views.eliminar_viaje,
        name='eliminar_viaje'
    ),

]