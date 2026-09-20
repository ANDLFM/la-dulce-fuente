from django.contrib import admin

from .models import (
    Producto,
    Pedido,
    Contacto
)


# =========================================================
# PRODUCTOS
# =========================================================

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'nombre',
        'categoria',
        'precio',
        'disponible',
    )

    list_filter = (
        'categoria',
        'disponible',
    )

    search_fields = (
        'nombre',
        'descripcion',
    )

    list_editable = (
        'precio',
        'disponible',
    )


# =========================================================
# PEDIDOS
# =========================================================

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'cliente',
        'pastel',
        'sabor',
        'tamano',
        'fecha_entrega',
        'estado',
    )

    list_filter = (
        'estado',
        'sabor',
        'tamano',
    )

    search_fields = (
        'cliente__username',
        'cliente__first_name',
        'pastel',
    )

    list_editable = (
        'estado',
    )


# =========================================================
# MENSAJES DE CONTACTO
# =========================================================

@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'nombre',
        'correo',
        'celular',
        'asunto',
        'fecha_envio',
    )

    search_fields = (
        'nombre',
        'correo',
        'celular',
        'asunto',
        'mensaje',
    )

    ordering = (
        '-fecha_envio',
    )