from django.urls import path
from . import views
from .test_views import logout_view

app_name = 'usuarios'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('cadastro/', views.RegisterView.as_view(), name='register'),
    path('perfil/', views.PerfilView.as_view(), name='perfil'),
    path('perfil/editar/', views.EditarPerfilView.as_view(), name='editar_perfil'),
    path('pedidos/', views.MeusPedidosView.as_view(), name='meus_pedidos'),
]
