from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Autor(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre completo")
    nacionalidad = models.CharField(max_length=50, verbose_name="Nacionalidad")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento")
    fecha_fallecimiento = models.DateField(null=True, blank=True, verbose_name="Fecha de fallecimiento")
    biografia = models.TextField(verbose_name="Biografía", help_text="Breve biografía del autor")
    email = models.EmailField(verbose_name="Email de contacto", blank=True)
    activo = models.BooleanField(default=True, verbose_name="Autor activo")
    
    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

class Editorial(models.Model):
    editorialid = models.AutoField(primary_key=True)
    nombreeditorial = models.CharField(max_length=255, unique=True, verbose_name="Nombre de la Editorial")
    direccion = models.CharField(max_length=255, verbose_name="Dirección")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    emailcontacto = models.EmailField(verbose_name="Email de Contacto")
    sitioweb = models.URLField(blank=True, verbose_name="Sitio Web")
    paisorigen = models.CharField(max_length=50, verbose_name="País de Origen")
    
    class Meta:
        verbose_name = "Editorial"
        verbose_name_plural = "Editoriales"
        ordering = ['nombreeditorial']
    
    def __str__(self):
        return self.nombreeditorial

class Cliente(models.Model):
    clienteid = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    apellido = models.CharField(max_length=100, verbose_name="Apellido")
    email = models.EmailField(unique=True, verbose_name="Email")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    direccion = models.CharField(max_length=255, verbose_name="Dirección")
    fecharegistro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    preferenciasgenero = models.TextField(blank=True, verbose_name="Preferencias de Género")
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['apellido', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

class Libro(models.Model):
    GENEROS = [
        ('FIC', 'Ficción'),
        ('ROM', 'Romance'),
        ('TER', 'Terror'),
        ('CIE', 'Ciencia Ficción'),
        ('FAN', 'Fantasía'),
        ('HIS', 'Histórico'),
        ('BIO', 'Biografía'),
        ('INF', 'Infantil'),
    ]
    
    titulo = models.CharField(max_length=200, verbose_name="Título del libro")
    isbn = models.CharField(max_length=13, unique=True, verbose_name="ISBN")
    genero = models.CharField(max_length=3, choices=GENEROS, verbose_name="Género")
    fecha_publicacion = models.DateField(verbose_name="Fecha de publicación")
    precio = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Precio")
    stock = models.PositiveIntegerField(default=0, verbose_name="Cantidad en stock")
    descripcion = models.TextField(verbose_name="Descripción", blank=True)
    
    # Relaciones
    autores = models.ManyToManyField(Autor, related_name='libros', verbose_name="Autores")
    editorial = models.ForeignKey(
        Editorial,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='libros',
        verbose_name="Editorial"
    )
    
    class Meta:
        verbose_name = "Libro"
        verbose_name_plural = "Libros"
        ordering = ['titulo']
    
    def __str__(self):
        return self.titulo
    
    def disponible(self):
        return self.stock > 0

class Venta(models.Model):
    ESTADOS_VENTA = [
        ('PEN', 'Pendiente'),
        ('COM', 'Completada'),
        ('CAN', 'Cancelada'),
        ('DEV', 'Devuelta'),
    ]
    
    id = models.AutoField(primary_key=True)
    fecha_venta = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Venta")
    cantidad_total = models.PositiveIntegerField(verbose_name="Cantidad Total", default=1)
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total", default=0.00)
    estado = models.CharField(max_length=3, choices=ESTADOS_VENTA, default='PEN', verbose_name="Estado")
    cliente_email = models.EmailField(verbose_name="Email del Cliente")
    libro = models.ForeignKey(
        Libro, 
        on_delete=models.PROTECT, 
        related_name='ventas_principal',
        verbose_name="Libro Principal"
    )
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name='ventas',
        verbose_name="Cliente",
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado en")
    
    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ['-fecha_venta']
    
    def __str__(self):
        return f"Venta #{self.id} - {self.cliente_email}"

class DetalleVenta(models.Model):
    detalleDeLaVentaid = models.AutoField(primary_key=True)
    precioUnitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Unitario")
    iva = models.DecimalField(max_digits=5, decimal_places=2, default=0.16, verbose_name="IVA")
    venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE,
        related_name='detalles',
        verbose_name="Venta"
    )
    libro = models.ForeignKey(
        Libro,
        on_delete=models.PROTECT,
        related_name='detalles_venta',
        verbose_name="Libro"
    )
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Subtotal")
    
    class Meta:
        verbose_name = "Detalle de Venta"
        verbose_name_plural = "Detalles de Venta"
        ordering = ['-venta__fecha_venta']
    
    def __str__(self):
        return f"Detalle {self.detalleDeLaVentaid} - Venta {self.venta.id}"
    
    def save(self, *args, **kwargs):
        # Calcular subtotal automáticamente
        self.subtotal = self.precioUnitario * self.cantidad
        super().save(*args, **kwargs)