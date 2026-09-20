from datetime import date
from pathlib import Path

from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth import (
    authenticate,
    login,
    logout
)

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import (
    Pedido,
    Producto,
    Contacto
)


# =========================================================
# LEER PROMOCIONES DESDE TXT
# =========================================================

def obtener_promociones():

    ruta_promociones = (
        Path(settings.BASE_DIR)
        / 'promociones.txt'
    )

    promociones = []

    try:

        with open(
            ruta_promociones,
            'r',
            encoding='utf-8'
        ) as archivo:

            for linea in archivo:

                promocion = linea.strip()

                if promocion:
                    promociones.append(
                        promocion
                    )

    except FileNotFoundError:

        promociones = []

    return promociones


# =========================================================
# INICIO
# =========================================================

def inicio(request):

    productos = Producto.objects.filter(
        disponible=True
    ).order_by(
        '-fecha_registro'
    )

    promociones = obtener_promociones()

    return render(
        request,
        'pasteleria/index.html',
        {
            'productos': productos,
            'promociones': promociones,
        }
    )


# =========================================================
# REGISTRO
# =========================================================

def registro(request):

    if request.user.is_authenticated:
        return redirect('inicio')

    if request.method == 'POST':

        nombre = request.POST.get(
            'nombre',
            ''
        ).strip()

        usuario = request.POST.get(
            'usuario',
            ''
        ).strip()

        correo = request.POST.get(
            'correo',
            ''
        ).strip()

        password = request.POST.get(
            'password',
            ''
        )

        confirmar = request.POST.get(
            'confirmar',
            ''
        )

        if (
            not nombre
            or not usuario
            or not correo
            or not password
            or not confirmar
        ):

            messages.error(
                request,
                'Por favor completa todos '
                'los campos.'
            )

            return redirect(
                'registro'
            )

        if password != confirmar:

            messages.error(
                request,
                'Las contraseñas no coinciden.'
            )

            return redirect(
                'registro'
            )

        if User.objects.filter(
            username=usuario
        ).exists():

            messages.error(
                request,
                'Ese nombre de usuario '
                'ya existe.'
            )

            return redirect(
                'registro'
            )

        if User.objects.filter(
            email=correo
        ).exists():

            messages.error(
                request,
                'Ese correo electrónico '
                'ya está registrado.'
            )

            return redirect(
                'registro'
            )

        User.objects.create_user(
            username=usuario,
            email=correo,
            password=password,
            first_name=nombre
        )

        messages.success(
            request,
            'Tu cuenta fue creada '
            'correctamente. '
            'Ahora inicia sesión.'
        )

        return redirect(
            'login'
        )

    return render(
        request,
        'pasteleria/registro.html'
    )


# =========================================================
# LOGIN
# =========================================================

def iniciar_sesion(request):

    if request.user.is_authenticated:
        return redirect('inicio')

    if request.method == 'POST':

        usuario = request.POST.get(
            'usuario',
            ''
        ).strip()

        password = request.POST.get(
            'password',
            ''
        )

        user = authenticate(
            request,
            username=usuario,
            password=password
        )

        if user is not None:

            login(
                request,
                user
            )

            messages.success(
                request,
                f'¡Bienvenido a '
                f'La Dulce Fuente, '
                f'{user.first_name or user.username}! 🎂'
            )

            return redirect(
                'inicio'
            )

        else:

            messages.error(
                request,
                'Usuario o contraseña '
                'incorrectos.'
            )

    return render(
        request,
        'pasteleria/login.html'
    )


# =========================================================
# CERRAR SESIÓN
# =========================================================

def cerrar_sesion(request):

    logout(request)

    return redirect(
        'inicio'
    )


# =========================================================
# HACER PEDIDO
# =========================================================

@login_required(login_url='login')
def hacer_pedido(request):

    productos = Producto.objects.filter(
        disponible=True
    ).order_by(
        'nombre'
    )

    producto_seleccionado = None

    producto_id_get = request.GET.get(
        'producto'
    )

    if producto_id_get:

        try:

            producto_seleccionado = (
                Producto.objects.get(
                    id=producto_id_get,
                    disponible=True
                )
            )

        except (
            Producto.DoesNotExist,
            ValueError
        ):

            messages.error(
                request,
                'El producto seleccionado '
                'no existe o ya no está '
                'disponible.'
            )

            return redirect(
                'inicio'
            )


    # =====================================================
    # GUARDAR PEDIDO
    # =====================================================

    if request.method == 'POST':

        producto_id = request.POST.get(
            'producto_id'
        )

        sabor = request.POST.get(
            'sabor'
        )

        tamano = request.POST.get(
            'tamano'
        )

        mensaje = request.POST.get(
            'mensaje',
            ''
        ).strip()

        fecha_entrega = request.POST.get(
            'fecha_entrega'
        )


        if not producto_id:

            messages.error(
                request,
                'Selecciona un producto.'
            )

            return redirect(
                'hacer_pedido'
            )


        try:

            producto = Producto.objects.get(
                id=producto_id,
                disponible=True
            )

        except (
            Producto.DoesNotExist,
            ValueError
        ):

            messages.error(
                request,
                'El producto seleccionado '
                'ya no está disponible.'
            )

            return redirect(
                'inicio'
            )


        if (
            not sabor
            or not tamano
            or not fecha_entrega
        ):

            messages.error(
                request,
                'Completa todos los '
                'datos del pedido.'
            )

            url = reverse(
                'hacer_pedido'
            )

            return redirect(
                f'{url}?producto={producto.id}'
            )


        sabores_validos = [
            opcion[0]
            for opcion in Pedido.SABORES
        ]

        if sabor not in sabores_validos:

            messages.error(
                request,
                'El sabor seleccionado '
                'no es válido.'
            )

            url = reverse(
                'hacer_pedido'
            )

            return redirect(
                f'{url}?producto={producto.id}'
            )


        tamanos_validos = [
            opcion[0]
            for opcion in Pedido.TAMANOS
        ]

        if tamano not in tamanos_validos:

            messages.error(
                request,
                'El tamaño seleccionado '
                'no es válido.'
            )

            url = reverse(
                'hacer_pedido'
            )

            return redirect(
                f'{url}?producto={producto.id}'
            )


        try:

            fecha_seleccionada = (
                date.fromisoformat(
                    fecha_entrega
                )
            )

        except ValueError:

            messages.error(
                request,
                'La fecha seleccionada '
                'no es válida.'
            )

            url = reverse(
                'hacer_pedido'
            )

            return redirect(
                f'{url}?producto={producto.id}'
            )


        if (
            fecha_seleccionada
            < date.today()
        ):

            messages.error(
                request,
                'La fecha de entrega '
                'no puede ser anterior '
                'a hoy.'
            )

            url = reverse(
                'hacer_pedido'
            )

            return redirect(
                f'{url}?producto={producto.id}'
            )


        Pedido.objects.create(
            cliente=request.user,
            pastel=producto.nombre,
            sabor=sabor,
            tamano=tamano,
            mensaje=mensaje,
            fecha_entrega=fecha_seleccionada
        )


        messages.success(
            request,
            f'¡Tu pedido de '
            f'{producto.nombre} '
            f'fue registrado '
            f'correctamente! 🎂'
        )


        return redirect(
            'mis_pedidos'
        )


    contexto = {

        'productos':
            productos,

        'producto_seleccionado':
            producto_seleccionado,

        'sabores':
            Pedido.SABORES,

        'tamanos':
            Pedido.TAMANOS,

        'fecha_min':
            date.today().isoformat(),
    }


    return render(
        request,
        'pasteleria/pedido.html',
        contexto
    )


# =========================================================
# MIS PEDIDOS
# =========================================================

@login_required(login_url='login')
def mis_pedidos(request):

    pedidos = Pedido.objects.filter(
        cliente=request.user
    ).order_by(
        '-fecha_pedido'
    )

    return render(
        request,
        'pasteleria/mis_pedidos.html',
        {
            'pedidos': pedidos
        }
    )


# =========================================================
# CONTACTO
# =========================================================

def contacto(request):

    if request.method == 'POST':

        nombre = request.POST.get(
            'nombre',
            ''
        ).strip()

        correo = request.POST.get(
            'correo',
            ''
        ).strip()

        celular = request.POST.get(
            'celular',
            ''
        ).strip()

        asunto = request.POST.get(
            'asunto',
            ''
        ).strip()

        mensaje = request.POST.get(
            'mensaje',
            ''
        ).strip()


        # VALIDAR CAMPOS

        if (
            not nombre
            or not correo
            or not celular
            or not asunto
            or not mensaje
        ):

            messages.error(
                request,
                'Por favor completa '
                'todos los campos.'
            )

            return redirect(
                'contacto'
            )


        # GUARDAR MENSAJE

        Contacto.objects.create(

            nombre=nombre,

            correo=correo,

            celular=celular,

            asunto=asunto,

            mensaje=mensaje

        )


        messages.success(
            request,
            '¡Tu mensaje fue enviado '
            'correctamente! ✉️'
        )


        return redirect(
            'contacto'
        )


    return render(
        request,
        'pasteleria/contacto.html'
    )