from django.urls import path
from .import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('registro/', views.registro_view, name='registro'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('paso1/', views.RegistroPasoUnoView.as_view(), name='paso1'),
    path('paso2/', views.RegistroPasoDosView.as_view(), name='paso2'),
    path('paso3/', views.RegistroPasoTresView.as_view(), name='paso3'),
    path('paso4/',  views.RegistroPasoCuatroView.as_view(), name='paso4'),
    path('pasoEm1/', views.RegistroEmpPasoUnoView.as_view(), name='pasoEm1'),
    path('pasoEm2/', views.RegistroEmpPasoDosView.as_view(), name='pasoEm2'),
    path('pasoEm3/', views.RegistroEmpPasoTresView.as_view(), name='pasoEm3'),
    path('pasoEm4/', views.RegistroEmpPasoCuatroView.as_view(), name='pasoEm4'),
    path('creacion_exitosa/', views.creacionUsuarioExitosa, name='creacion_exitosa'),
    path('crear-administrador/', views.crear_usuario_administrador, name='crear_usuario_administrador'),
    path('mostrar_solicitudes/', views.mostrar_solicitudes, name='mostrar_solicitudes'),
    path('aceptar_solicitud/<int:solicitud_id>/', views.aceptar_solicitud, name='aceptar_solicitud'),
    path('eliminar_solicitud/<int:solicitud_id>/', views.eliminar_solicitud, name='eliminar_solicitud'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)