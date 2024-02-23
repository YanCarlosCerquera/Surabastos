from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Producto
from django.contrib import messages



###########Vistas panel de usuario##################################################
@login_required
def panel_usuario(request):
    return render(request, 'Perfiles/panel_usuario.html')

@login_required
def mi_perfil(request):
    try:
        # Intenta recuperar el primer objeto relacionado con el usuario actual
        producto = Producto.objects.filter(autor_persona_natural=request.user).first()
        ciudad = producto.ciudad if producto else "Ciudad no especificada"
    except Producto.DoesNotExist:
        ciudad = "Ciudad no especificada"
    return render(request, 'mi_perfil.html', {'ciudad': ciudad})


###############################################################################################################################
from .forms import PasoUnoForm, PasoDosForm, PasoTresForm, ImagenFormSet
from django.views import View
from django import forms
from .models import Producto
from decimal import Decimal
from .models import ImagenProducto

class PasoUnoView(View):
    def get(self, request):
        nombre = request.GET.get('nombre')
        descripcion = request.GET.get('descripcion')
        precio = request.GET.get('precio')
        ciudad = request.GET.get('ciudad')
        form = PasoUnoForm(initial={'nombre': nombre, 'descripcion': descripcion, 'precio': precio, 'ciudad': ciudad})
        return render(request, 'Perfiles/paso_uno.html', {'form': form})

    def post(self, request):
        form = PasoUnoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data['descripcion']
            precio = form.cleaned_data['precio']
            ciudad = form.cleaned_data['ciudad']

            request.session['nombre'] = nombre
            request.session['descripcion'] = descripcion
            request.session['precio'] = str(precio) 
            request.session['ciudad'] = ciudad
            return redirect('paso_dos')
        return render(request, 'Perfiles/paso_uno.html', {'form': form})



class PasoDosForm(forms.Form):
    OPCIONES_CATEGORIA = {
        'frutas.jpg': 1,
        'verduras.jpg': 0,
    }
    categoria = forms.ChoiceField(choices=OPCIONES_CATEGORIA, widget=forms.RadioSelect)

from django.shortcuts import redirect


class PasoDosView(View):
    def get(self, request):
        form = PasoDosForm()
        return render(request, 'Perfiles/paso_dos.html', {'form': form})

    def post(self, request):
        categoria = request.POST.get('categoria') 
        if categoria in ('0', '1'): 
            request.session['categoria'] = int(categoria)
            return redirect('paso_tres')
        form = PasoDosForm(request.POST)
        return render(request, 'Perfiles/paso_dos.html', {'form': form})


class PasoTresView(View):
    def get(self, request):
        formset = ImagenFormSet()
        return render(request, 'Perfiles/paso_tres.html', {'formset': formset})

    def post(self, request):
        formset = ImagenFormSet(request.POST, request.FILES)
        if formset.is_valid():
            nombre = request.session['nombre']
            descripcion = request.session['descripcion']
            ciudad = request.session['ciudad']
            categoria = request.session.get('categoria')
            precio = Decimal(request.session['precio'])

            producto = Producto(nombre=nombre, precio=precio, descripcion=descripcion, ciudad=ciudad, categoria=categoria)
            if request.user.nit_rut:
                
                producto.autor_empresa = request.user
            else:
                
                producto.autor_persona_natural = request.user
            
            producto.save()  

            for form in formset:
                if 'imagen' in form.cleaned_data and form.cleaned_data['imagen']:
                    imagen = form.cleaned_data['imagen']
                    img = ImagenProducto(producto=producto, imagen=imagen)
                    img.save()
            
            return redirect('publicacion_exitosa')
        return render(request, 'Perfiles/paso_tres.html', {'formset': formset})


@login_required
def publicacionexitosa(request):
    
    return render(request, 'Perfiles/publicacion_correcta.html')