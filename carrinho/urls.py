from django.urls import path
from . import views

app_name = 'carrinho'

urlpatterns = [
    path('', views.CarrinhoView.as_view(), name='visualizar'),
    path('carrinho/', views.CarrinhoView.as_view(), name='carrinho'),
    path('adicionar/<int:produto_id>/', views.AdicionarItemView.as_view(), name='adicionar'),
    path('remover/<int:item_id>/', views.RemoverItemView.as_view(), name='remover'),
    path('atualizar/<int:item_id>/', views.AtualizarItemView.as_view(), name='atualizar'),
    path('limpar/', views.LimparCarrinhoView.as_view(), name='limpar'),
    path('calcular-frete/', views.CalcularFreteView.as_view(), name='calcular_frete'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('finalizar/', views.FinalizarCompraView.as_view(), name='finalizar'),
]
