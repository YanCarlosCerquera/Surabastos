from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import PasoUnoView, PasoDosView, PasoTresView


urlpatterns = [
    path('panel/', views.panel_usuario, name='panel_usuario'),
    #path('panel/publicar/', views.publicar_producto, name='publicar_producto'),
    path('mi_perfil/', views.mi_perfil, name='mi_perfil'),
    path('paso_uno/', PasoUnoView.as_view(), name='paso_uno'),
    path('paso_dos/', PasoDosView.as_view(), name='paso_dos'),
    path('paso_tres/', PasoTresView.as_view(), name='paso_tres'),
    path('publicacion_exitosa/', views.publicacionexitosa, name='publicacion_exitosa'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
