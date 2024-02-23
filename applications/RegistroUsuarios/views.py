from .models import Perfil
from django.shortcuts import render, redirect, get_object_or_404
from .forms import EmpresaRegistroForm, PNaturalRegistroForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import user_passes_test
        

###########################################################################################################################

def registro_view(request):
    return render(request, 'registro.html')

#############################################################################################################################

def registro_usuario_normal(request):
    if request.method == 'POST':
        form = PNaturalRegistroForm(request.POST)
        if form.is_valid():
            user = form.save()  # Guarda el usuario
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('home')
        else:
            print(form.errors)  # Agrega este debug
            messages.error(request, 'Formulario no válido. Revise los datos.')
    else:
        form = PNaturalRegistroForm()

    return render(request, 'registroNatural.html', {'form': form})

##################################################################################################################################
def registro_empresa(request):
    if request.method == 'POST':
        form = EmpresaRegistroForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            # Crea un usuario 
            user = form.save(commit=False)  # No guardar aún para asignar valores
            # Asigna los datos del formulario a los campos del modelo
            user.email = form.cleaned_data['email']
            user.nombre_comercial = form.cleaned_data['nombre_comercial']
            user.nit_rut = form.cleaned_data['nit_rut']
            user.documento = form.cleaned_data['documento'] 
            user.cell = form.cleaned_data['cell']
            user.departamento = form.cleaned_data['departamento']
            user.municipio = form.cleaned_data['municipio']
            user.direccion = form.cleaned_data['direccion']
            user.documento = request.FILES.get('documento')
            print(request.FILES)
            # Establece la contraseña correctamente
            user.set_password(form.cleaned_data['password1'])
            # Guarda el usuario
            user.save()
            return redirect('home')  # Redirige a la página de inicio
    else:
        form = EmpresaRegistroForm()
    return render(request, 'registroEmpresa.html', {'form': form})


#####################################################################################################################################

def crear_usuario_administrador(request):
    if request.method == 'POST':
        form = PNaturalRegistroForm(request.POST)
        if form.is_valid():
            # Crea un superusuario sin guardarlo aún
            User = get_user_model()  # Obtén el modelo de usuario personalizado
            user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                cell=form.cleaned_data['cell']
            )
            # Establece la contraseña correctamente
            user.set_password(form.cleaned_data['password'])
            user.usuario_administrador = True  # Marca como administrador
            user.usuario_activo = True
            # Guarda el superusuario
            user.save()
            messages.success(request, 'Superusuario creado correctamente.')
            return redirect('home')
    else:
        form = PNaturalRegistroForm()
    return render(request, 'crear_usuario_administrador.html', {'form': form})


##################################################################################################################################
def es_administrador(user):
     return user.is_authenticated and user.is_active and user.usuario_administrador
@login_required
@user_passes_test(es_administrador)
def mostrar_solicitudes(request):

    solicitudes_pendientes = Perfil.objects.filter(usuario_activo=0).count()
    solicitudes_aceptadas = Perfil.objects.filter(usuario_activo=1).count()
    # Obtener todas las solicitudes de creación de usuarios
    solicitudes = Perfil.objects.filter(usuario_activo=0)
    return render(request, 'mostrar_solicitudes.html', {
        'solicitudes': solicitudes,
        'solicitudes_pendientes': solicitudes_pendientes,
        'solicitudes_aceptadas': solicitudes_aceptadas})

@login_required
@user_passes_test(es_administrador)
def aceptar_solicitud(request, solicitud_id):
    # Lógica para aceptar la solicitud
    solicitud = get_object_or_404(Perfil, pk=solicitud_id)
    solicitud.usuario_activo = True
    solicitud.save()
    return redirect('mostrar_solicitudes')

@login_required
@user_passes_test(es_administrador)
def eliminar_solicitud(request, solicitud_id):
    # Lógica para eliminar la solicitud
    solicitud = get_object_or_404(Perfil, pk=solicitud_id)
    solicitud.delete()
    return redirect('mostrar_solicitudes')

################################################################################################################################

def login_view(request):
    mensaje_advertencia = "" 

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)

                # Verificar el tipo de usuario y redirigir en consecuencia
                if user.usuario_administrador:
                    return redirect('mostrar_solicitudes')
                elif user.usuario_activo:
                    return redirect('blog:home')
                else:
                    mensaje_advertencia = "El administrador no ha aprobado tu solicitud"
            else:
                mensaje_advertencia = "Usuario Inválido"
        else:
            mensaje_advertencia = "Información Inválida"
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form, 'mensaje_advertencia': mensaje_advertencia})


def logout_view(request):
    logout(request)
    return redirect(login_view)

###############################Formulario Pnatural secuencial####################################################################
from django.shortcuts import render, redirect
from .models import Perfil
from django.views import View
from .forms import RegistroPasoUnoForm
from .forms import RegistroPasoDosForm
from .forms import RegistroPasoTresForm
from .forms import RegistroPasoCuatroForm
from django import forms 


class RegistroPasoUnoForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico')

class RegistroPasoUnoView(View):
    def get(self, request):
         # Captura los datos de la URL
        email = request.GET.get('email')
        # Prellena el formulario con los datos capturados de la URL
        form = RegistroPasoUnoForm(initial={'email': email})
        return render(request, 'formulario_paso1.html', {'form': form})

    def post(self, request):
        form = RegistroPasoUnoForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Realiza la validación del correo en la base de datos
            if Perfil.objects.filter(email=email).exists():
                form.add_error('email', "Este correo electrónico ya está en uso.")
                return render(request, 'formulario_paso1.html', {'form': form})
            # Si el correo no existe en la base de datos, almacénalo en la sesión y redirige al siguiente paso.
            request.session['email'] = email
            return redirect('paso2')
        return render(request, 'formulario_paso1.html', {'form': form})
    

class RegistroPasoDosForm(forms.Form):
    username = forms.CharField(max_length=30, label='Nombre de usuario')

class RegistroPasoDosView(View):
    def get(self, request):
         # Captura los datos de la URL
        username = request.GET.get('username')

        # Prellena el formulario con los datos capturados de la URL
        form = RegistroPasoDosForm(initial={'username': username})
        return render(request, 'formulario_paso2.html', {'form': form})

    def post(self, request):
        form = RegistroPasoDosForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            # Realiza la validación del correo en la base de datos
            if Perfil.objects.filter(username=username).exists():
                form.add_error('username', "Este nombre ya está en uso.")
                return render(request, 'formulario_paso2.html', {'form': form})
            # Si el correo no existe en la base de datos, almacénalo en la sesión y redirige al siguiente paso.
            request.session['username'] = username
            return redirect('paso3')
        return render(request, 'formulario_paso2.html', {'form': form})
    

class RegistroPasoTresForm(forms.Form):
    cell = forms.CharField(max_length=13, label='Número de teléfono')

def clean_cell(self):
        cell = self.cleaned_data['cell']

        # Verifica que el campo solo contenga números
        if not cell.isdigit():
            raise forms.ValidationError("Este campo debe contener solo números.")

class RegistroPasoTresView(View):
    def get(self, request):
         # Captura los datos de la URL
        cell = request.GET.get('cell')

        # Prellena el formulario con los datos capturados de la URL
        form = RegistroPasoTresForm(initial={'cell': cell})
        return render(request, 'formulario_paso3.html', {'form': form})

    def post(self, request):
        form = RegistroPasoTresForm(request.POST)
        if form.is_valid():
            cell = form.cleaned_data['cell']
            # Realiza la validación del correo en la base de datos
            if Perfil.objects.filter(cell=cell).exists():
                form.add_error('cell', "Este telefono ya está en uso.")
                return render(request, 'formulario_paso3.html', {'form': form})
            # Si el correo no existe en la base de datos, almacénalo en la sesión y redirige al siguiente paso.
            request.session['cell'] = cell
            return redirect('paso4')
        return render(request, 'formulario_paso3.html', {'form': form})
    


class RegistroPasoCuatroView(View):
    def get(self, request):
        email = request.session.get('email')
        username = request.session.get('username')
        cell = request.session.get('cell')

        # Se pasan los datos de la sesión al formulario a través de initial
        form = RegistroPasoCuatroForm(initial={'email': email, 'username': username, 'cell': cell})
        return render(request, 'formulario_paso4.html', {'form': form})

    def post(self, request):
        form = RegistroPasoCuatroForm(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            # Realiza las validaciones necesarias para las contraseñas
            if password1 != password2:
                form.add_error('password2', "Las contraseñas no coinciden.")
                return render(request, 'formulario_paso4.html', {'form': form})
            # Si las contraseñas coinciden, almacena la contraseña en la sesión
            request.session['password'] = password1
            # Creación del usuario y guardado en la base de datos
            email = request.session['email']
            username = request.session['username']
            cell = request.session['cell']
            # Se utiliza make_password para generar la contraseña con el algoritmo de hash predeterminado
            password_hash = make_password(password1)

            # Crea una instancia de Perfil y asignar los valores
            user = Perfil(email=email, username=username, cell=cell, password=password_hash)
            user.save()  # Guarda el usuario en la base de datos

            # Redirige a la página de confirmación
            return redirect('creacion_exitosa')

        return render(request, 'formulario_paso4.html', {'form': form})



################################Formulario Empresa################################################################################
class RegistroEmpPasoUnoForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico')

class RegistroEmpPasoUnoView(View):
    def get(self, request):
         # Captura los datos de la URL
        email = request.GET.get('email')
        # Prellena el formulario con los datos capturados de la URL
        form = RegistroEmpPasoUnoForm(initial={'email': email})
        return render(request, 'formularioEm_paso1.html', {'form': form})

    def post(self, request):
        form = RegistroEmpPasoUnoForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Realiza la validación del correo en la base de datos
            if Perfil.objects.filter(email=email).exists():
                form.add_error('email', "Este correo electrónico ya está en uso.")
                return render(request, 'formularioEm_paso1.html', {'form': form})
            # Si el correo no existe en la base de datos, almacénalo en la sesión y redirige al siguiente paso.
            request.session['email'] = email
            return redirect('pasoEm2')
        return render(request, 'formularioEm_paso1.html', {'form': form})
    

#####################################################PASO 1########################################################################
from django import forms
from django.shortcuts import render, redirect
from django.views import View
from .models import Perfil
from django.core.validators import FileExtensionValidator
import base64

class RegistroEmpPasoDosForm(forms.Form):
    nombre_comercial = forms.CharField(max_length=100, label='Nombre Comercial')
    nit_rut = forms.CharField(max_length=30, label='Número de Identificación Tributaria (NIT) o (RUT)')
    documento = forms.FileField(
        label='Documento (PDF, JPG, PNG)',
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'png']),
        ],
        widget=forms.ClearableFileInput(attrs={'accept': '.pdf,.jpg,.png'}),
        required=False
    )
    departamento = forms.CharField(max_length=100, label='Departamento')
    municipio = forms.CharField(max_length=100, label='Municipio')
    direccion = forms.CharField(max_length=100, label='Dirección')
    nombre_propietario = forms.CharField(max_length=100, label='Nombre del Propietario')

class RegistroEmpPasoDosView(View):
    def get(self, request):
        # Captura los datos de la URL
        nombre_comercial = request.GET.get('nombre_comercial')
        nit_rut = request.GET.get('nit_rut')
        departamento = request.GET.get('departamento')
        municipio = request.GET.get('municipio')
        direccion = request.GET.get('direccion')
        nombre_propietario = request.GET.get('nombre_propietario')

        # Prellena el formulario con los datos capturados de la URL
        form = RegistroEmpPasoDosForm(initial={'nombre_comercial': nombre_comercial, 'nit_rut': nit_rut, 'departamento': departamento,
                        'municipio': municipio, 'direccion': direccion, 'nombre_propietario': nombre_propietario})
        return render(request, 'formularioEm_paso2.html', {'form': form})

    def post(self, request):
        form = RegistroEmpPasoDosForm(request.POST, request.FILES)
        if form.is_valid():
            nit_rut = form.cleaned_data['nit_rut']

            # Realiza la validación del NIT/RUT en la base de datos
            if Perfil.objects.filter(nit_rut=nit_rut).exists():
                form.add_error('nit_rut', "Este NIT/RUT ya está en uso.")
                return render(request, 'formularioEm_paso2.html', {'form': form})
            
            # Si el NIT/RUT no existe en la base de datos, almacénalo en la sesión y redirige al siguiente paso.
            request.session['nit_rut'] = nit_rut

            # Almacena los otros valores directamente en la sesión
            request.session['nombre_comercial'] = form.cleaned_data['nombre_comercial']
            request.session['departamento'] = form.cleaned_data['departamento']
            request.session['municipio'] = form.cleaned_data['municipio']
            request.session['direccion'] = form.cleaned_data['direccion']
            request.session['nombre_propietario'] = form.cleaned_data['nombre_propietario']

            # Almacena el contenido del archivo en la sesión, codificándolo en Base64
            if 'documento' in request.FILES:
                documento_content = base64.b64encode(request.FILES['documento'].read()).decode('utf-8')
                request.session['documento'] = documento_content

            return redirect('pasoEm3')

        return render(request, 'formularioEm_paso2.html', {'form': form})

#####################################################################################################################################
class RegistroEmpPasoTresView(View):
    def get(self, request):
         # Captura los datos de la URL
        cell = request.GET.get('cell')

        # Prellena el formulario con los datos capturados de la URL
        form = RegistroPasoTresForm(initial={'cell': cell})
        return render(request, 'formulario_paso3.html', {'form': form})

    def post(self, request):
        form = RegistroPasoTresForm(request.POST)
        if form.is_valid():
            cell = form.cleaned_data['cell']
            # Realiza la validación del correo en la base de datos
            if Perfil.objects.filter(cell=cell).exists():
                form.add_error('cell', "Este telefono ya está en uso.")
                return render(request, 'formulario_paso3.html', {'form': form})
            # Si el correo no existe en la base de datos, almacénalo en la sesión y redirige al siguiente paso.
            request.session['cell'] = cell
            return redirect('pasoEm4')
        return render(request, 'formulario_paso3.html', {'form': form})
    

###########################################################################################################################################3
from .forms import RegistroEmpPasoCuatroForm  
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from django.views import View
from .forms import RegistroEmpPasoCuatroForm
from .models import Perfil  # Asegúrate de importar el modelo Perfil

class RegistroEmpPasoCuatroView(View):
    def get(self, request):
        email = request.session.get('email')
        nombre_comercial = request.session.get('nombre_comercial')
        nit_rut = request.session.get('nit_rut')
        departamento = request.session.get('departamento')
        municipio = request.session.get('municipio')
        direccion = request.session.get('direccion')
        nombre_propietario = request.session.get('nombre_propietario')

        form = RegistroEmpPasoCuatroForm(initial={
            'email': email,
            'nombre_comercial': nombre_comercial,
            'nit_rut': nit_rut,
            'departamento': departamento,
            'municipio': municipio,
            'direccion': direccion,
            'nombre_propietario': nombre_propietario,
        })

        return render(request, 'formularioEm_paso4.html', {'form': form})

    def post(self, request):
        form = RegistroEmpPasoCuatroForm(request.POST, request.FILES)
        if form.is_valid():
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            if password1 != password2:
                form.add_error('password2', "Las contraseñas no coinciden.")
                return render(request, 'formularioEm_paso4.html', {'form': form})

            documento_content = request.session.get('documento')
            if documento_content:
                # Decodificar el contenido del archivo desde Base64 para obtener los bytes originales
                documento_bytes = base64.b64decode(documento_content.encode('utf-8'))
                # Generar un nombre de archivo único basado en el NIT/RUT
                nit_rut = request.session.get('nit_rut')
                file_name = f'documentos/{nit_rut}.pdf'
                # Verificar si el archivo ya existe y eliminarlo
                if default_storage.exists(file_name):
                    default_storage.delete(file_name)
                # Almacenar el archivo en la carpeta de medios
                file_content = ContentFile(documento_bytes)
                default_storage.save(file_name, file_content)

                # Crear el usuario y asignar el archivo
                user = Perfil()
                user.email = request.session.get('email')
                user.nombre_comercial = request.session.get('nombre_comercial')
                user.nit_rut = nit_rut
                user.cell = request.session.get('cell')
                user.departamento = request.session.get('departamento')
                user.municipio = request.session.get('municipio')
                user.direccion = request.session.get('direccion')
                user.nombre_propietario = request.session.get('nombre_propietario')
                user.documento.name = file_name
                user.set_password(password1)
                user.save()
                # Limpia la variable de sesión después de guardar el usuario
                del request.session['documento']
                return redirect('creacion_exitosa')
        return render(request, 'formularioEm_paso4.html', {'form': form})
    


def creacionUsuarioExitosa(request):
    
    return render(request, 'creacion_exitosa.html')
