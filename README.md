# SantaClaraPapelaria


# Guia de Configuração do Projeto Django

## 1. Instalar as Dependências

Com o ambiente virtual ativado, a próxima etapa é instalar as dependências listadas no `requirements.txt`.

```bash
pip install -r requirements.txt
```

Esse comando irá instalar o Django, o Django REST Framework, o drf-yasg (para o Swagger) e outras dependências que você especificou.

## 2. Criar o Arquivo .env

A pessoa também precisará configurar as variáveis de ambiente para conectar ao banco de dados PostgreSQL. Para isso, deve criar um arquivo `.env` no diretório raiz do projeto, com o conteúdo a seguir:

```env
# .env
```

## 3. Criar uma Nova View, Model e Serializer

Agora, vamos criar um novo modelo, view e serializer para um novo recurso, digamos, tabela.

### 3.1. Criar o Modelo (tabela.py)

Dentro do diretório `cadastro/models/`, crie um novo arquivo `tabela.py`:

```python
from django.db import models

class Tabela(models.Model):
    atributo = models.CharField(max_length=8, primary_key=True)

    class Meta:
        db_table = '"schema"."tabela"'  # Especificando que a tabela ficará no esquema 'cadastro'

    def __str__(self):
        return self.nome
```

### 3.2. Adicionar ao admin.py

No arquivo `cadastro/admin.py`, registre o modelo `Tabela` para que ele apareça na interface administrativa do Django.

```python
from django.contrib import admin

# Register your models here.
from .models.tabela import Tabela

admin.site.register(Tabela)
```

### 3.3. Criar o Serializer (tabela_serializer.py)

Agora, crie o arquivo `cadastro/serializers/tabela_serializer.py` para o serializer do modelo `Tabela`:

```python
from rest_framework import serializers
from cadastro.models.tabela import Tabela

class TabelaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tabela
        fields = '__all__'  # Inclui todos os campos do modelo Tabela
```

### 3.4. Criar a View (tabela_view.py)

Crie o arquivo `cadastro/views/tabela_view.py` para a view que lida com as operações CRUD do modelo `Tabela`:

```python
from rest_framework import viewsets
from cadastro.models.tabela import Tabela
from cadastro.serializers.tabela_serializer import TabelaSerializer

class TabelaViewSet(viewsets.ModelViewSet):
    queryset = Tabela.objects.all()  # Obtém todos os registros de Tabela
    serializer_class = TabelaSerializer  # Define o serializer para este viewset
```

### 3.5. Registrar as URLs (cadastro/urls.py)

Agora, registre as URLs para a view `Tabela` no arquivo `cadastro/urls.py`:

```python
from cadastro.views.tabela_view import TabelaViewSet  # Importando o ViewSet de Tabela
from rest_framework.routers import DefaultRouter

# Criando o roteador e registrando as views
router = DefaultRouter()
router.register(r'tabelas', TabelaViewSet)
```

## 4. Testar a API

Agora, você pode rodar o servidor Django e testar a API:

```bash
python manage.py runserver
```

No navegador, acesse a URL do Swagger para testar as rotas criadas para `Tabela`:

**Swagger UI:** [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)
