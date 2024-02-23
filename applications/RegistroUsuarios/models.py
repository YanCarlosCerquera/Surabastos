from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

#Manager
class PerfilManager(BaseUserManager):
    def create_user(self, email, username, cell, password=None, **extra_fields):
        if not email:
            raise ValueError("El usuario debe tener un correo electrónico")
        
        user = self.model(
            username=username,
            cell=cell,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user
    
#######Superuser##################################################################################
    def create_superuser(self, email, username, cell, password, **extra_fields):
        extra_fields.setdefault('usuario_administrador', True)
        extra_fields.setdefault('usuario_activo', True)

        if extra_fields.get('usuario_administrador') is not True:
            raise ValueError("Superuser must have usuario_administrador=True.")

        return self.create_user(username, email, cell, password, **extra_fields)

#################Modelo Perfil (PERSONA NATURAL/PERSONA JURIDICA)#####################################
class Perfil(AbstractBaseUser):
    email = models.EmailField('Correo Electrónico', unique=True, max_length=100, blank=False)
    username = models.CharField('Nombre de usuario', unique=True, max_length=100, blank=False)
    cell = models.CharField('Celular', unique=True, max_length=13)
    fecha_creacion = models.DateTimeField('Fecha y Hora de Creación', default=timezone.now)
    usuario_activo = models.BooleanField(default=False)
    usuario_administrador = models.BooleanField(default=False)
    nit_rut = models.CharField('NIT/RUT', unique=True, max_length=100, blank=True, null=True)
    documento = models.FileField('Documento (PDF/JPG)', upload_to='documentos/', blank=True, null=True)
    nombre_comercial = models.CharField('Nombre Comercial', max_length=255, blank=True)
    departamento = models.CharField('Departamento', max_length=100, blank=True)
    municipio = models.CharField('Municipio', max_length=100, blank=True)
    direccion = models.CharField('Dirección', max_length=255, blank=True)
    nombre_propietario = models.CharField('Nombre Propietario', max_length=255, blank=True)
    
    objects = PerfilManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'cell']

    def save(self, *args, **kwargs):
        # Si se proporciona un NIT/RUT, el usuario se considera como usuario de empresa
        if self.nit_rut:
            self.username = self.nit_rut

        super().save(*args, **kwargs)

    
    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.usuario_administrador
