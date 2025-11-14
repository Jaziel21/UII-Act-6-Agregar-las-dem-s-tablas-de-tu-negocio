from django.contrib import admin
from .models import Autor, Libro, Venta, Editorial, Cliente, DetalleVenta

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nacionalidad', 'email', 'activo')
    list_filter = ('activo', 'nacionalidad')
    search_fields = ('nombre', 'email')
    ordering = ('nombre',)

@admin.register(Editorial)
class EditorialAdmin(admin.ModelAdmin):
    list_display = ('nombreeditorial', 'paisorigen', 'emailcontacto', 'telefono')
    list_filter = ('paisorigen',)
    search_fields = ('nombreeditorial', 'emailcontacto')
    ordering = ('nombreeditorial',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'email', 'telefono', 'fecharegistro')
    list_filter = ('fecharegistro',)
    search_fields = ('nombre', 'apellido', 'email')
    ordering = ('apellido', 'nombre')

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'isbn', 'genero', 'precio', 'stock', 'editorial', 'disponible')
    list_filter = ('genero', 'editorial')
    search_fields = ('titulo', 'isbn')
    filter_horizontal = ('autores',)
    ordering = ('titulo',)

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente_email', 'fecha_venta', 'total', 'estado', 'cliente')
    list_filter = ('estado', 'fecha_venta')
    search_fields = ('cliente_email', 'cliente__nombre', 'cliente__apellido')
    ordering = ('-fecha_venta',)

@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ('detalleDeLaVentaid', 'venta', 'libro', 'cantidad', 'precioUnitario', 'subtotal')
    list_filter = ('venta__fecha_venta',)
    search_fields = ('libro__titulo', 'venta__cliente_email')
    ordering = ('-venta__fecha_venta',)