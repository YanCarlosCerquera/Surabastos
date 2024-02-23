from django import forms
from .models import Perfil
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.contrib.auth.password_validation import validate_password

########################################################Formulario Usuario persona natural#####################################################

class PNaturalRegistroForm(UserCreationForm):
    class Meta:
        model = Perfil
        fields = ['email', 'username', 'cell','password1', 'password2']
        widgets = {
            'password1': forms.PasswordInput(attrs={'placeholder': 'Contraseña'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirmar contraseña'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return password2
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Verificar si ya existe un usuario con este username
        if Perfil.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Verificar si ya existe un usuario con este email
        if Perfil.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está en uso.")
        
        return email

    def clean_cell(self):
        cell = self.cleaned_data.get('cell')

        # Verificar si ya existe un usuario con este número de celular
        if Perfil.objects.filter(cell=cell).exists():
            raise forms.ValidationError("Este número de celular ya está en uso.")
        
        return cell

###############################Formulario usuario tipo empresa##################################################################################

class EmpresaRegistroForm(UserCreationForm):
    nombre_comercial = forms.CharField(max_length=100, label='Nombre Comercial')
    departamento = forms.CharField(max_length=100, label='Departamento')
    municipio = forms.CharField(max_length=100, label='Municipio')
    direccion = forms.CharField(max_length=100, label='Dirección')
    nombre_propietario = forms.CharField(max_length=100, label='Nombre del Propietario')
    


    documento = forms.FileField(
        label='Documento (PDF, JPG, PNG)',
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'png']),
        ],
        widget=forms.ClearableFileInput(attrs={'accept': '.pdf,.jpg,.png'}),
        required=False
    )

    class Meta:
        model = Perfil
        fields = ['email', 'cell', 'password1', 'password2', 
                  'nit_rut', 'nombre_comercial', 'departamento', 'municipio', 
                  'direccion', 'nombre_propietario']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': 'Contraseña'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': 'Confirmar contraseña'})

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return password2
    
    def clean_documento(self):
        documento = self.cleaned_data.get('documento')
        if documento:
            # Validar el tamaño del archivo
            if documento.size > 10 * 1024 * 1024:  # 10 MB
                raise forms.ValidationError("El archivo es demasiado grande (máximo 10 MB).")
        return documento
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Perfil.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está en uso.")
        
        return email

    def clean_cell(self):
        cell = self.cleaned_data.get('cell')
        if Perfil.objects.filter(cell=cell).exists():
            raise forms.ValidationError("Este número de celular ya está en uso.")
        
        return cell
    
    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Guardar documento si está presente
        documento = self.cleaned_data.get('documento')
        if documento:
            user.documento = documento

        if commit:
            user.save()
        return user

Perfil = get_user_model()

class UsuarioAdministradorForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Perfil
        fields = ['username', 'email', 'cell', 'password']

    def save(self, commit=True):
        # Guarda la contraseña de forma segura
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.usuario_administrador = True
        

        if commit:
            user.save()
        return user
    

############################formulario empresa por pasos##########################################################################
class RegistroPasoUnoForm(forms.Form):
    class Meta:
        model = Perfil
        fields = ['email']

class RegistroPasoDosForm(forms.Form):
    class Meta:
        model = Perfil
        fields = ['username']

class RegistroPasoTresForm(forms.Form):
    class Meta:
        model = Perfil
        fields = ['cell']



class RegistroPasoCuatroForm(UserCreationForm):
    class Meta:
        model = Perfil
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None  

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        try:
            validate_password(password1, self.instance)
        except forms.ValidationError as error:
            self.add_error('password1', error)
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return password2

#########################Formulario secuencial para empresa############################################################################
class RegistroEmpPasoUnoForm(forms.Form):
    class Meta:
        model = Perfil
        fields = ['email']

class RegistroEmpPasoDosForm(forms.Form):
    class Meta:
        model = Perfil
        fields = ['nombre_comercial', 'nit_rut', 'documento', 'departamento', 'municipio', 'direccion', 'nombre_propietario']

class RegistroEmpPasoTresForm(forms.Form):
    class Meta:
        model = Perfil
        fields = ['cell']



class RegistroEmpPasoCuatroForm(UserCreationForm):
    class Meta:
        model = Perfil
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None  

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        try:
            validate_password(password1, self.instance)
        except forms.ValidationError as error:
            self.add_error('password1', error)
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return password2
