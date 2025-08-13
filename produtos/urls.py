from django.urls import path
from . import views

app_name = 'produtos'

urlpatterns = [
    path('', views.ProdutoListView.as_view(), name='lista'),
    path('buscar/', views.ProdutoBuscarView.as_view(), name='buscar'),
    path('categoria/<slug:slug>/', views.CategoriaProdutosView.as_view(), name='categoria'),
    path('<slug:slug>/', views.ProdutoDetailView.as_view(), name='produto_detail'),
]
