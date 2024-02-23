from django.shortcuts import render
from applications.Perfiles.models import Producto 
from PIL import Image
import random
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
import os
from applications.Perfiles.models import ImagenProducto
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
###########Logica para mostrar los  productos agregados recientemente###############################################
@login_required
def home_view(request):
    productos = Producto.objects.order_by('-fecha_publicacion')[:8]

    for producto in productos:
        imagenes_producto = ImagenProducto.objects.filter(producto=producto)
        for imagen in imagenes_producto:
            if os.path.exists(imagen.imagen.path):
                img = Image.open(imagen.imagen.path)
                img = img.resize((300, 200), Image.BOX)
                img.save(imagen.imagen.path)

    producto_aleatorio = None
    if productos:
        producto_aleatorio = random.choice(productos)

    return render(request, 'home.html', {'productos': productos, 'producto_aleatorio': producto_aleatorio})



###########################################################################################################################
@login_required
def tienda_view(request):
    # Obtén todos los productos disponibles
    productos = Producto.objects.all()

    ciudad = request.GET.get('ciudad')
    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')

    # Verifica si se proporciona un parámetro para mostrar todos los productos
    mostrar_todos = request.GET.get('mostrar_todos')

    if not mostrar_todos:
        # Verifica si se proporciona precio, independientemente de la ciudad
        if not ciudad and not precio_min and not precio_max:
            pass  # No se aplica filtro de ciudad si solo se busca por precio
        else:
            if ciudad:
                productos = productos.filter(ciudad=ciudad)

        if precio_min:
            productos = productos.filter(precio__gte=precio_min)

        if precio_max:
            productos = productos.filter(precio__lte=precio_max)

    # Lógica para ordenar los productos
    ordenar_por = request.GET.get('order_by')

    if ordenar_por:
        if ordenar_por == 'fecha_asc':
            productos = productos.order_by('fecha_publicacion')
        elif ordenar_por == 'fecha_desc':
            productos = productos.order_by('-fecha_publicacion')

    ciudades_huila = ["Acevedo", "Aipe", "Algeciras", "Altamira", "Baraya", "Campoalegre", "Colombia", "Elías", "El Agrado", "Garzón", "Gigante",
                     "Guadalupe", "Hobo", "Íquira", "Isnos", "La Argentina", "La Plata", "Nátaga", "Neiva", "Oporapa", "Paicol", "Palermo", "Palestina",
                     "Pital", "Rivera", "Saladoblanco", "Santa María", "San Agustín", "Suaza", "Tarqui", "Tello", "Teruel", "Tesalia", "Timana", "Villavieja", "Yaguara"]

    query = request.GET.get("q")

    if query:
        productos = productos.filter(nombre__icontains=query)


    # Paginación
    page = request.GET.get('page')
    paginator = Paginator(productos, 5)  # 5 productos por página

    try:
        productos = paginator.page(page)
    except PageNotAnInteger:
        productos = paginator.page(1)
    except EmptyPage:
        productos = paginator.page(paginator.num_pages)


    context = {
        "productos": productos,
        "ciudades_huila": ciudades_huila,
        "ciudad_seleccionada": ciudad, 
    }

    return render(request, 'tienda.html', context)

####################################################################################################################################
@login_required

def info_productos(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    imagenes_producto = producto.imagenes.all() 
    return render(request, 'info_productos.html', {'producto': producto, 'imagenes_producto': imagenes_producto})

###################################################################################################################################
@login_required

def tienda_dos_view(request):
    productos = Producto.objects.all()

    # Lógica para ordenar los productos
    ordenar_por = request.GET.get('order_by')

    if ordenar_por:
        if ordenar_por == 'fecha_asc':
            productos = productos.order_by('fecha_publicacion')
        elif ordenar_por == 'fecha_desc':
            productos = productos.order_by('-fecha_publicacion')

    query = request.GET.get("q")

    if query:
        productos = productos.filter(nombre__icontains=query)

    
    return render(request, 'tienda2.html', {'productos': productos})