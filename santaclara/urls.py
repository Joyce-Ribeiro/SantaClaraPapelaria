from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/cadastro/', include('cadastro.urls')),  # Prefixo para as rotas da app 'cadastro'
    path('api/comercial/', include('comercial.urls')),  # Prefixo para as rotas da app 'comercial'
]
