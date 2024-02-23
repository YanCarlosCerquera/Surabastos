
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('applications.Blog.urls')),
    path('perfil/', include('applications.Perfiles.urls')),
    path('', include('applications.RegistroUsuarios.urls')),
]
