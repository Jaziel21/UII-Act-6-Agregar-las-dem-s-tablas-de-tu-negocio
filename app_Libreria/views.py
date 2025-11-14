from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Autor, Libro, Venta, Editorial, Cliente, DetalleVenta
from django.utils import timezone

def inicio_libreria(request):
    """Vista para la página de inicio"""
    # Obtener conteos para las estadísticas
    context = {
        'autores_count': Autor.objects.count(),
        'libros_count': Libro.objects.count(),
        'clientes_count': Cliente.objects.count(),
        'ventas_count': Venta.objects.count(),
    }
    
    return render(request, 'inicio.html', context)

# ==========================================
# VISTAS PARA AUTORES
# ==========================================

def agregar_autor(request):
    """Vista para agregar un nuevo autor"""
    if request.method == 'POST':
        # Procesar formulario sin usar Django Forms
        nombre = request.POST.get('nombre')
        nacionalidad = request.POST.get('nacionalidad')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        fecha_fallecimiento = request.POST.get('fecha_fallecimiento') or None
        biografia = request.POST.get('biografia')
        email = request.POST.get('email')
        activo = 'activo' in request.POST
        
        autor = Autor(
            nombre=nombre,
            nacionalidad=nacionalidad,
            fecha_nacimiento=fecha_nacimiento,
            fecha_fallecimiento=fecha_fallecimiento,
            biografia=biografia,
            email=email,
            activo=activo
        )
        autor.save()
        
        return redirect('ver_autores')
    
    return render(request, 'autor/agregar_autor.html')

def ver_autores(request):
    """Vista para ver todos los autores"""
    autores = Autor.objects.all()
    return render(request, 'autor/ver_autores.html', {'autores': autores})

def actualizar_autor(request, autor_id):
    """Vista para mostrar formulario de actualización"""
    autor = get_object_or_404(Autor, id=autor_id)
    return render(request, 'autor/actualizar_autor.html', {'autor': autor})

def realizar_actualizacion_autor(request, autor_id):
    """Vista para procesar la actualización del autor"""
    if request.method == 'POST':
        autor = get_object_or_404(Autor, id=autor_id)
        
        autor.nombre = request.POST.get('nombre')
        autor.nacionalidad = request.POST.get('nacionalidad')
        autor.fecha_nacimiento = request.POST.get('fecha_nacimiento')
        fecha_fallecimiento = request.POST.get('fecha_fallecimiento')
        autor.fecha_fallecimiento = fecha_fallecimiento if fecha_fallecimiento else None
        autor.biografia = request.POST.get('biografia')
        autor.email = request.POST.get('email')
        autor.activo = 'activo' in request.POST
        
        autor.save()
        
        return redirect('ver_autores')
    
    return redirect('ver_autores')

def borrar_autor(request, autor_id):
    """Vista para confirmar eliminación"""
    autor = get_object_or_404(Autor, id=autor_id)
    return render(request, 'autor/borrar_autor.html', {'autor': autor})

def confirmar_borrar_autor(request, autor_id):
    """Vista para procesar la eliminación"""
    if request.method == 'POST':
        autor = get_object_or_404(Autor, id=autor_id)
        autor.delete()
    return redirect('ver_autores')

# ==========================================
# VISTAS PARA EDITORIALES
# ==========================================

def agregar_editorial(request):
    """Vista para agregar una nueva editorial"""
    if request.method == 'POST':
        nombreeditorial = request.POST.get('nombreeditorial')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        emailcontacto = request.POST.get('emailcontacto')
        sitioweb = request.POST.get('sitioweb')
        paisorigen = request.POST.get('paisorigen')
        
        editorial = Editorial(
            nombreeditorial=nombreeditorial,
            direccion=direccion,
            telefono=telefono,
            emailcontacto=emailcontacto,
            sitioweb=sitioweb,
            paisorigen=paisorigen
        )
        editorial.save()
        
        return redirect('ver_editoriales')
    
    return render(request, 'editorial/agregar_editorial.html')

def ver_editoriales(request):
    """Vista para ver todas las editoriales"""
    editoriales = Editorial.objects.all()
    return render(request, 'editorial/ver_editoriales.html', {'editoriales': editoriales})

def actualizar_editorial(request, editorial_id):
    """Vista para mostrar formulario de actualización"""
    editorial = get_object_or_404(Editorial, editorialid=editorial_id)
    return render(request, 'editorial/actualizar_editorial.html', {'editorial': editorial})

def realizar_actualizacion_editorial(request, editorial_id):
    """Vista para procesar la actualización de editorial"""
    if request.method == 'POST':
        editorial = get_object_or_404(Editorial, editorialid=editorial_id)
        
        editorial.nombreeditorial = request.POST.get('nombreeditorial')
        editorial.direccion = request.POST.get('direccion')
        editorial.telefono = request.POST.get('telefono')
        editorial.emailcontacto = request.POST.get('emailcontacto')
        editorial.sitioweb = request.POST.get('sitioweb')
        editorial.paisorigen = request.POST.get('paisorigen')
        
        editorial.save()
        return redirect('ver_editoriales')
    
    return redirect('ver_editoriales')

def borrar_editorial(request, editorial_id):
    """Vista para confirmar eliminación"""
    editorial = get_object_or_404(Editorial, editorialid=editorial_id)
    return render(request, 'editorial/borrar_editorial.html', {'editorial': editorial})

def confirmar_borrar_editorial(request, editorial_id):
    """Vista para procesar la eliminación"""
    if request.method == 'POST':
        editorial = get_object_or_404(Editorial, editorialid=editorial_id)
        editorial.delete()
    return redirect('ver_editoriales')

# ==========================================
# VISTAS PARA LIBROS
# ==========================================

def ver_libros(request):
    """Vista para ver todos los libros"""
    libros = Libro.objects.all().prefetch_related('autores', 'editorial')
    return render(request, 'libro/ver_libros.html', {'libros': libros})

def agregar_libro(request):
    """Vista para agregar un nuevo libro"""
    autores = Autor.objects.all()
    editoriales = Editorial.objects.all()
    
    if request.method == 'POST':
        # Procesar formulario sin usar Django Forms
        titulo = request.POST.get('titulo')
        isbn = request.POST.get('isbn')
        genero = request.POST.get('genero')
        fecha_publicacion = request.POST.get('fecha_publicacion')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        descripcion = request.POST.get('descripcion')
        editorial_id = request.POST.get('editorial')
        autores_seleccionados = request.POST.getlist('autores')
        
        # Obtener la editorial si se seleccionó una
        editorial = None
        if editorial_id:
            editorial = Editorial.objects.get(editorialid=editorial_id)
        
        # Crear el libro
        libro = Libro(
            titulo=titulo,
            isbn=isbn,
            genero=genero,
            fecha_publicacion=fecha_publicacion,
            precio=precio,
            stock=stock,
            descripcion=descripcion,
            editorial=editorial
        )
        libro.save()
        
        # Agregar autores (relación ManyToMany)
        for autor_id in autores_seleccionados:
            autor = Autor.objects.get(id=autor_id)
            libro.autores.add(autor)
        
        return redirect('ver_libros')
    
    return render(request, 'libro/agregar_libro.html', {
        'autores': autores,
        'editoriales': editoriales
    })

def actualizar_libro(request, libro_id):
    """Vista para mostrar formulario de actualización"""
    libro = get_object_or_404(Libro, id=libro_id)
    autores = Autor.objects.all()
    editoriales = Editorial.objects.all()
    autores_seleccionados = libro.autores.values_list('id', flat=True)
    
    return render(request, 'libro/actualizar_libro.html', {
        'libro': libro,
        'autores': autores,
        'editoriales': editoriales,
        'autores_seleccionados': list(autores_seleccionados)
    })

def realizar_actualizacion_libro(request, libro_id):
    """Vista para procesar la actualización del libro"""
    if request.method == 'POST':
        libro = get_object_or_404(Libro, id=libro_id)
        
        libro.titulo = request.POST.get('titulo')
        libro.isbn = request.POST.get('isbn')
        libro.genero = request.POST.get('genero')
        libro.fecha_publicacion = request.POST.get('fecha_publicacion')
        libro.precio = request.POST.get('precio')
        libro.stock = request.POST.get('stock')
        libro.descripcion = request.POST.get('descripcion')
        
        # Actualizar editorial
        editorial_id = request.POST.get('editorial')
        if editorial_id:
            libro.editorial = Editorial.objects.get(editorialid=editorial_id)
        else:
            libro.editorial = None
        
        libro.save()
        
        # Actualizar autores
        autores_seleccionados = request.POST.getlist('autores')
        libro.autores.clear()
        for autor_id in autores_seleccionados:
            autor = Autor.objects.get(id=autor_id)
            libro.autores.add(autor)
        
        return redirect('ver_libros')
    
    return redirect('ver_libros')

def borrar_libro(request, libro_id):
    """Vista para confirmar eliminación"""
    libro = get_object_or_404(Libro, id=libro_id)
    return render(request, 'libro/borrar_libro.html', {'libro': libro})

def confirmar_borrar_libro(request, libro_id):
    """Vista para procesar la eliminación"""
    if request.method == 'POST':
        libro = get_object_or_404(Libro, id=libro_id)
        libro.delete()
    return redirect('ver_libros')

# ==========================================
# VISTAS PARA CLIENTES
# ==========================================

def agregar_cliente(request):
    """Vista para agregar un nuevo cliente"""
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        preferenciasgenero = request.POST.get('preferenciasgenero')
        
        cliente = Cliente(
            nombre=nombre,
            apellido=apellido,
            email=email,
            telefono=telefono,
            direccion=direccion,
            preferenciasgenero=preferenciasgenero
        )
        cliente.save()
        
        return redirect('ver_clientes')
    
    return render(request, 'cliente/agregar_cliente.html')

def ver_clientes(request):
    """Vista para ver todos los clientes"""
    clientes = Cliente.objects.all()
    return render(request, 'cliente/ver_clientes.html', {'clientes': clientes})

def actualizar_cliente(request, cliente_id):
    """Vista para mostrar formulario de actualización"""
    cliente = get_object_or_404(Cliente, clienteid=cliente_id)
    return render(request, 'cliente/actualizar_cliente.html', {'cliente': cliente})

def realizar_actualizacion_cliente(request, cliente_id):
    """Vista para procesar la actualización de cliente"""
    if request.method == 'POST':
        cliente = get_object_or_404(Cliente, clienteid=cliente_id)
        
        cliente.nombre = request.POST.get('nombre')
        cliente.apellido = request.POST.get('apellido')
        cliente.email = request.POST.get('email')
        cliente.telefono = request.POST.get('telefono')
        cliente.direccion = request.POST.get('direccion')
        cliente.preferenciasgenero = request.POST.get('preferenciasgenero')
        
        cliente.save()
        return redirect('ver_clientes')
    
    return redirect('ver_clientes')

def borrar_cliente(request, cliente_id):
    """Vista para confirmar eliminación"""
    cliente = get_object_or_404(Cliente, clienteid=cliente_id)
    return render(request, 'cliente/borrar_cliente.html', {'cliente': cliente})

def confirmar_borrar_cliente(request, cliente_id):
    """Vista para procesar la eliminación"""
    if request.method == 'POST':
        cliente = get_object_or_404(Cliente, clienteid=cliente_id)
        cliente.delete()
    return redirect('ver_clientes')

# ==========================================
# VISTAS PARA VENTAS
# ==========================================

def agregar_venta(request):
    """Vista para agregar una nueva venta"""
    clientes = Cliente.objects.all()
    libros = Libro.objects.filter(stock__gt=0)
    
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        libro_id = request.POST.get('libro')
        cantidad = int(request.POST.get('cantidad'))
        estado = request.POST.get('estado')
        
        cliente = get_object_or_404(Cliente, clienteid=cliente_id)
        libro = get_object_or_404(Libro, id=libro_id)
        
        # Calcular total
        precio_unitario = libro.precio
        total = precio_unitario * cantidad
        
        venta = Venta(
            cantidad_total=cantidad,
            total=total,
            estado=estado,
            cliente_email=cliente.email,
            libro=libro,
            cliente=cliente
        )
        venta.save()
        
        # Crear detalle de venta
        detalle = DetalleVenta(
            precioUnitario=precio_unitario,
            iva=0.16,
            venta=venta,
            libro=libro,
            cantidad=cantidad,
            subtotal=total
        )
        detalle.save()
        
        # Actualizar stock del libro
        libro.stock -= cantidad
        libro.save()
        
        return redirect('ver_ventas')
    
    return render(request, 'venta/agregar_venta.html', {
        'clientes': clientes,
        'libros': libros
    })

def ver_ventas(request):
    """Vista para ver todas las ventas"""
    ventas = Venta.objects.all().select_related('cliente', 'libro')
    return render(request, 'venta/ver_ventas.html', {'ventas': ventas})

def actualizar_venta(request, venta_id):
    """Vista para mostrar formulario de actualización"""
    venta = get_object_or_404(Venta, id=venta_id)
    clientes = Cliente.objects.all()
    libros = Libro.objects.all()
    
    return render(request, 'venta/actualizar_venta.html', {
        'venta': venta,
        'clientes': clientes,
        'libros': libros
    })

def realizar_actualizacion_venta(request, venta_id):
    """Vista para procesar la actualización de venta"""
    if request.method == 'POST':
        venta = get_object_or_404(Venta, id=venta_id)
        
        cliente_id = request.POST.get('cliente')
        libro_id = request.POST.get('libro')
        cantidad = int(request.POST.get('cantidad'))
        estado = request.POST.get('estado')
        
        cliente = get_object_or_404(Cliente, clienteid=cliente_id)
        libro = get_object_or_404(Libro, id=libro_id)
        
        # Restaurar stock anterior
        libro_anterior = venta.libro
        libro_anterior.stock += venta.cantidad_total
        libro_anterior.save()
        
        # Actualizar venta
        venta.cliente = cliente
        venta.libro = libro
        venta.cantidad_total = cantidad
        venta.estado = estado
        venta.cliente_email = cliente.email
        
        # Recalcular total
        precio_unitario = libro.precio
        venta.total = precio_unitario * cantidad
        
        venta.save()
        
        # Actualizar stock nuevo
        libro.stock -= cantidad
        libro.save()
        
        # Actualizar detalle de venta
        detalle = venta.detalles.first()
        if detalle:
            detalle.precioUnitario = precio_unitario
            detalle.libro = libro
            detalle.cantidad = cantidad
            detalle.subtotal = venta.total
            detalle.save()
        
        return redirect('ver_ventas')
    
    return redirect('ver_ventas')

def borrar_venta(request, venta_id):
    """Vista para confirmar eliminación"""
    venta = get_object_or_404(Venta, id=venta_id)
    return render(request, 'venta/borrar_venta.html', {'venta': venta})

def confirmar_borrar_venta(request, venta_id):
    """Vista para procesar la eliminación"""
    if request.method == 'POST':
        venta = get_object_or_404(Venta, id=venta_id)
        
        # Restaurar stock
        libro = venta.libro
        libro.stock += venta.cantidad_total
        libro.save()
        
        venta.delete()
    
    return redirect('ver_ventas')

# ==========================================
# VISTAS PARA DETALLES DE VENTA
# ==========================================

def ver_detalles_venta(request, venta_id):
    """Vista para ver los detalles de una venta específica"""
    venta = get_object_or_404(Venta, id=venta_id)
    detalles = DetalleVenta.objects.filter(venta=venta).select_related('libro')
    
    return render(request, 'detalle_venta/ver_detalles_venta.html', {
        'venta': venta,
        'detalles': detalles
    })

def agregar_detalle_venta(request, venta_id):
    """Vista para agregar un detalle a una venta existente"""
    venta = get_object_or_404(Venta, id=venta_id)
    libros = Libro.objects.filter(stock__gt=0)
    
    if request.method == 'POST':
        libro_id = request.POST.get('libro')
        cantidad = int(request.POST.get('cantidad'))
        
        libro = get_object_or_404(Libro, id=libro_id)
        precio_unitario = libro.precio
        subtotal = precio_unitario * cantidad
        
        detalle = DetalleVenta(
            precioUnitario=precio_unitario,
            iva=0.16,
            venta=venta,
            libro=libro,
            cantidad=cantidad,
            subtotal=subtotal
        )
        detalle.save()
        
        # Actualizar stock y total de la venta
        libro.stock -= cantidad
        libro.save()
        
        venta.cantidad_total += cantidad
        venta.total += subtotal
        venta.save()
        
        return redirect('ver_detalles_venta', venta_id=venta.id)
    
    return render(request, 'detalle_venta/agregar_detalle_venta.html', {
        'venta': venta,
        'libros': libros
    })