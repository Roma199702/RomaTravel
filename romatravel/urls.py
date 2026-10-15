
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from agencia.forms_login import RomaTravelLoginForm


urlpatterns = [

    # Administración de Django
    path(
        'admin/',
        admin.site.urls
    ),

    # Inicio de sesión
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='agencia/login.html',
            authentication_form=RomaTravelLoginForm,
            redirect_authenticated_user=True
        ),
        name='login'
    ),

    # Cierre de sesión
    path(
        'logout/',
        auth_views.LogoutView.as_view(
            next_page='inicio'
        ),
        name='logout'
    ),

    # Rutas de RomaTravel
    path(
        '',
        include('agencia.urls')
    ),
]


