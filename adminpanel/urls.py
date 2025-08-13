from django.urls import path
from . import views

app_name = 'adminpanel'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    # Produtos
    path('produtos/', views.ProdutoListView.as_view(), name='produto_list'),
    path('produtos/adicionar/', views.ProdutoCreateView.as_view(), name='produto_create'),
    path('produtos/<int:pk>/', views.ProdutoDetailView.as_view(), name='produto_detail'),
    path('produtos/<int:pk>/editar/', views.ProdutoUpdateView.as_view(), name='produto_update'),
    path('produtos/<int:pk>/deletar/', views.ProdutoDeleteView.as_view(), name='produto_delete'),
    
    # Fornecedores
    path('fornecedores/', views.FornecedorListView.as_view(), name='fornecedor_list'),
    path('fornecedores/adicionar/', views.FornecedorCreateView.as_view(), name='fornecedor_create'),
    path('fornecedores/<int:pk>/', views.FornecedorDetailView.as_view(), name='fornecedor_detail'),
    path('fornecedores/<int:pk>/editar/', views.FornecedorUpdateView.as_view(), name='fornecedor_update'),
    path('fornecedores/<int:pk>/deletar/', views.FornecedorDeleteView.as_view(), name='fornecedor_delete'),
    
    # Pedidos
    path('pedidos/', views.PedidoListView.as_view(), name='pedido_list'),
    path('pedidos/<uuid:numero_pedido>/', views.PedidoDetailView.as_view(), name='pedido_detail'),
    path('pedidos/<uuid:numero_pedido>/status/', views.AtualizarStatusView.as_view(), name='atualizar_status'),
    
    # Relatórios
    path('relatorios/', views.RelatoriosView.as_view(), name='relatorios'),
]
