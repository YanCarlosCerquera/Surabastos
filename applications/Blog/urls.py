from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'blog'  

urlpatterns = [
    path('', views.home_view, name='home'), 
    path('tienda',views.tienda_view, name='tienda'),
    path('shop',views.tienda_dos_view, name='shop'),
    path('info',views.info_productos, name='info'),
    path('info_productos/<int:producto_id>/', views.info_productos, name='info_productos'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
