from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuração do Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="API Santa Clara",
        default_version="v1",
        description="API para gestão de cadastro e vendas",
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),  # Rota para o painel admin
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger'),  # Rota para o Swagger
    path('', include('cadastro.urls')),  # Incluindo as URLs do módulo de cadastro
]
