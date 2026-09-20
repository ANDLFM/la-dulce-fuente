from django.db import models
from django.contrib.auth.models import User


# =========================================================
# PRODUCTOS
# =========================================================

class Producto(models.Model):

    CATEGORIAS = [
        ('Pastel', 'Pastel'),
        ('Cupcake', 'Cupcake'),
        ('Postre', 'Postre'),
        ('Personalizado', 'Personalizado'),
    ]

    nombre = models.CharField(
        max_length=100
    )

    descripcion = models.TextField(
        max_length=300
    )

    categoria = models.CharField(
        max_length=30,
        choices=CATEGORIAS
    )

    precio = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    imagen = models.ImageField(
        upload_to='productos/',
        blank=True,
        null=True
    )

    disponible = models.BooleanField(
        default=True
    )

    fecha_registro = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.nombre


# =========================================================
# PEDIDOS
# =========================================================

class Pedido(models.Model):

    TAMANOS = [
        ('Chico', 'Chico'),
        ('Mediano', 'Mediano'),
        ('Grande', 'Grande'),
    ]

    SABORES = [
        ('Chocolate', 'Chocolate'),
        ('Vainilla', 'Vainilla'),
        ('Fresa', 'Fresa'),
        ('Tres Leches', 'Tres Leches'),
        ('Red Velvet', 'Red Velvet'),
        ('Oreo', 'Oreo'),
    ]

    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('Preparando', 'Preparando'),
        ('Listo', 'Listo'),
        ('Entregado', 'Entregado'),
    ]

    cliente = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    pastel = models.CharField(
        max_length=100
    )

    sabor = models.CharField(
        max_length=50,
        choices=SABORES
    )

    tamano = models.CharField(
        max_length=20,
        choices=TAMANOS
    )

    mensaje = models.CharField(
        max_length=150,
        blank=True
    )

    fecha_entrega = models.DateField()

    fecha_pedido = models.DateTimeField(
        auto_now_add=True
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='Pendiente'
    )

    def __str__(self):

        return (
            f"{self.cliente.username} - "
            f"{self.pastel}"
        )


# =========================================================
# CONTACTO
# =========================================================

class Contacto(models.Model):

    nombre = models.CharField(
        max_length=100
    )

    correo = models.EmailField()

    celular = models.CharField(
        max_length=20
    )

    asunto = models.CharField(
        max_length=150
    )

    mensaje = models.TextField()

    fecha_envio = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f"{self.nombre} - "
            f"{self.asunto}"
        )