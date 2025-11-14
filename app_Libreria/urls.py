from django.urls import path
from . import views

urlpatterns = [
    # Página principal
    path('', views.inicio_libreria, name='inicio_libreria'),
    
    # URLs para Autores
    path('autores/agregar/', views.agregar_autor, name='agregar_autor'),
    path('autores/', views.ver_autores, name='ver_autores'),
    path('autores/actualizar/<int:autor_id>/', views.actualizar_autor, name='actualizar_autor'),
    path('autores/realizar_actualizacion/<int:autor_id>/', views.realizar_actualizacion_autor, name='realizar_actualizacion_autor'),
    path('autores/borrar/<int:autor_id>/', views.borrar_autor, name='borrar_autor'),
    path('autores/confirmar_borrar/<int:autor_id>/', views.confirmar_borrar_autor, name='confirmar_borrar_autor'),
    
    # URLs para Editoriales
    path('editoriales/agregar/', views.agregar_editorial, name='agregar_editorial'),
    path('editoriales/', views.ver_editoriales, name='ver_editoriales'),
    path('editoriales/actualizar/<int:editorial_id>/', views.actualizar_editorial, name='actualizar_editorial'),
    path('editoriales/realizar_actualizacion/<int:editorial_id>/', views.realizar_actualizacion_editorial, name='realizar_actualizacion_editorial'),
    path('editoriales/borrar/<int:editorial_id>/', views.borrar_editorial, name='borrar_editorial'),
    path('editoriales/confirmar_borrar/<int:editorial_id>/', views.confirmar_borrar_editorial, name='confirmar_borrar_editorial'),
    
    # URLs para Libros
    path('libros/agregar/', views.agregar_libro, name='agregar_libro'),
    path('libros/', views.ver_libros, name='ver_libros'),
    path('libros/actualizar/<int:libro_id>/', views.actualizar_libro, name='actualizar_libro'),
    path('libros/realizar_actualizacion/<int:libro_id>/', views.realizar_actualizacion_libro, name='realizar_actualizacion_libro'),
    path('libros/borrar/<int:libro_id>/', views.borrar_libro, name='borrar_libro'),
    path('libros/confirmar_borrar/<int:libro_id>/', views.confirmar_borrar_libro, name='confirmar_borrar_libro'),
    
    # URLs para Clientes
    path('clientes/agregar/', views.agregar_cliente, name='agregar_cliente'),
    path('clientes/', views.ver_clientes, name='ver_clientes'),
    path('clientes/actualizar/<int:cliente_id>/', views.actualizar_cliente, name='actualizar_cliente'),
    path('clientes/realizar_actualizacion/<int:cliente_id>/', views.realizar_actualizacion_cliente, name='realizar_actualizacion_cliente'),
    path('clientes/borrar/<int:cliente_id>/', views.borrar_cliente, name='borrar_cliente'),
    path('clientes/confirmar_borrar/<int:cliente_id>/', views.confirmar_borrar_cliente, name='confirmar_borrar_cliente'),
    
    # URLs para Ventas
    path('ventas/agregar/', views.agregar_venta, name='agregar_venta'),
    path('ventas/', views.ver_ventas, name='ver_ventas'),
    path('ventas/actualizar/<int:venta_id>/', views.actualizar_venta, name='actualizar_venta'),
    path('ventas/realizar_actualizacion/<int:venta_id>/', views.realizar_actualizacion_venta, name='realizar_actualizacion_venta'),
    path('ventas/borrar/<int:venta_id>/', views.borrar_venta, name='borrar_venta'),
    path('ventas/confirmar_borrar/<int:venta_id>/', views.confirmar_borrar_venta, name='confirmar_borrar_venta'),
    
    # URLs para Detalles de Venta
    path('ventas/<int:venta_id>/detalles/', views.ver_detalles_venta, name='ver_detalles_venta'),
    path('ventas/<int:venta_id>/detalles/agregar/', views.agregar_detalle_venta, name='agregar_detalle_venta'),
]