from django.urls import path

from . import views


urlpatterns = [

    path(
        '',
        views.inicio,
        name='inicio'
    ),

    path(
        'registro/',
        views.registro,
        name='registro'
    ),

    path(
        'login/',
        views.iniciar_sesion,
        name='login'
    ),

    path(
        'logout/',
        views.cerrar_sesion,
        name='logout'
    ),

    path(
        'pedido/',
        views.hacer_pedido,
        name='hacer_pedido'
    ),

    path(
        'mis-pedidos/',
        views.mis_pedidos,
        name='mis_pedidos'
    ),

    path(
        'contacto/',
        views.contacto,
        name='contacto'
    ),

]
