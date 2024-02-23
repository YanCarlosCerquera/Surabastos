from django import forms
from .models import Producto
from django.forms import formset_factory
from .models import ImagenProducto

#class ProductoForm(forms.ModelForm):
    #class Meta:
       # model = Producto
       # fields = ['nombre', 'categoria', 'descripcion', 'precio', 'ciudad', 'imagenes']

###########################Formulario secuencial##############################################################

ciudades_huila = ["Acevedo", "Aipe", "Algeciras", "Altamira", "Baraya", "Campoalegre", "Colombia", "Elías", "El Agrado", "Garzón", "Gigante",
                     "Guadalupe", "Hobo", "Íquira", "Isnos", "La Argentina", "La Plata", "Nátaga", "Neiva", "Oporapa", "Paicol", "Palermo", "Palestina",
                     "Pital", "Rivera", "Saladoblanco", "Santa María", "San Agustín", "Suaza", "Tarqui", "Tello", "Teruel", "Tesalia", "Timana", "Villavieja", "Yaguara"]


class PasoUnoForm(forms.Form):
    
    nombre = forms.CharField(max_length=100)
    descripcion = forms.CharField(widget=forms.Textarea)
    precio = forms.DecimalField()
    ciudad = forms.ChoiceField(
        choices=[('', 'Seleccionar ciudad')] + [(ciudad, ciudad) for ciudad in ciudades_huila]
    )

class PasoDosForm(forms.Form):
    OPCIONES_CATEGORIA = {
        'frutas.jpg': 1,
        'verduras.jpg': 0
    }
    categoria = forms.ChoiceField(choices=OPCIONES_CATEGORIA, widget=forms.RadioSelect)

class PasoTresForm(forms.ModelForm):
    class Meta:
        model = ImagenProducto
        fields = ['imagen']
        widgets = {
            'imagen': forms.FileInput(attrs={'class': 'custom-class'}),
        }
ImagenFormSet = formset_factory(PasoTresForm, extra=10, max_num=10, validate_max=True)





