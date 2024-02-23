# Generated by Django 4.2.2 on 2024-02-09 16:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=100, unique=True, verbose_name='Correo Electrónico')),
                ('username', models.CharField(max_length=100, unique=True, verbose_name='Nombre de usuario')),
                ('cell', models.CharField(max_length=13, unique=True, verbose_name='Celular')),
                ('fecha_creacion', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha y Hora de Creación')),
                ('usuario_activo', models.BooleanField(default=False)),
                ('usuario_administrador', models.BooleanField(default=False)),
                ('nit_rut', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='NIT/RUT')),
                ('documento', models.FileField(blank=True, null=True, upload_to='documentos/', verbose_name='Documento (PDF/JPG)')),
                ('nombre_comercial', models.CharField(blank=True, max_length=255, verbose_name='Nombre Comercial')),
                ('departamento', models.CharField(blank=True, max_length=100, verbose_name='Departamento')),
                ('municipio', models.CharField(blank=True, max_length=100, verbose_name='Municipio')),
                ('direccion', models.CharField(blank=True, max_length=255, verbose_name='Dirección')),
                ('nombre_propietario', models.CharField(blank=True, max_length=255, verbose_name='Nombre Propietario')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
