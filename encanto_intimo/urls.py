"""
URL configuration for encanto_intimo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from .test_views import teste_mensagens

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    
    # Apps do projeto
    path('produtos/', include('produtos.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('carrinho/', include('carrinho.urls')),
    path('pedidos/', include('pedidos.urls')),
    path('pagamentos/', include('pagamentos.urls')),
    path('painel/', include('adminpanel.urls')),
    
    # Django Allauth URLs
    path('accounts/', include('allauth.urls')),
    
    # Teste
    path('teste-mensagens/', teste_mensagens, name='teste_mensagens'),
]

# Servir arquivos de media em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
