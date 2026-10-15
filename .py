[1mdiff --git a/romatravel/urls.py b/romatravel/urls.py[m
[1mindex b98f1b7..8d0b549 100644[m
[1m--- a/romatravel/urls.py[m
[1m+++ b/romatravel/urls.py[m
[36m@@ -1,17 +1,40 @@[m
[32m+[m
 from django.contrib import admin[m
 from django.urls import path, include[m
[32m+[m[32mfrom django.contrib.auth import views as auth_views[m
 [m
 [m
 urlpatterns = [[m
 [m
[32m+[m[32m    # Panel de administración Django[m
     path([m
         'admin/',[m
         admin.site.urls[m
     ),[m
 [m
[32m+[m[32m    # Inicio de sesión[m
[32m+[m[32m    path([m
[32m+[m[32m        'login/',[m
[32m+[m[32m        auth_views.LoginView.as_view([m
[32m+[m[32m            template_name='agencia/login.html',[m
[32m+[m[32m            redirect_authenticated_user=True[m
[32m+[m[32m        ),[m
[32m+[m[32m        name='login'[m
[32m+[m[32m    ),[m
[32m+[m
[32m+[m[32m    # Cierre de sesión[m
[32m+[m[32m    path([m
[32m+[m[32m        'logout/',[m
[32m+[m[32m        auth_views.LogoutView.as_view([m
[32m+[m[32m            next_page='inicio'[m
[32m+[m[32m        ),[m
[32m+[m[32m        name='logout'[m
[32m+[m[32m    ),[m
[32m+[m
[32m+[m[32m    # Rutas de la agencia[m
     path([m
         '',[m
         include('agencia.urls')[m
     ),[m
 [m
[31m-][m
\ No newline at end of file[m
[32m+[m[32m][m
