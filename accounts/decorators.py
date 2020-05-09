from django.http import HttpResponse
from django.shortcuts import redirect

# Función para validar si el usuario esta registrado o no
def unauthenticated_user(views_func):
    def wrapper_func(request, *args, **kwargs):
        # Si el usuario ya esta en su cuenta e intenta ir a la página de login
        if request.user.is_authenticated:
            # Lo devolvemos a la página del dashboard
            return redirect('home')
        else:
            # Se devuelva la función de nuestro archivo views.py
            return views_func(request, *args, **kwargs)

    return wrapper_func
