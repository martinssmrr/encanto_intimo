from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    # Checkout e criação de pedido
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('finalizar/', views.finalizar_pedido, name='finalizar'),
    
    # Pagamento
    path('pagamento/<uuid:numero_pedido>/', views.PagamentoView.as_view(), name='pagamento'),
    path('confirmar-pagamento/', views.confirmar_pagamento, name='confirmar_pagamento'),
    path('confirmar-pagamento-manual/<uuid:numero_pedido>/', views.confirmar_pagamento_manual, name='confirmar_pagamento_manual'),
    
    # Visualização de pedidos
    path('meus-pedidos/', views.MeusPedidosView.as_view(), name='meus_pedidos'),
    path('confirmacao/<uuid:numero_pedido>/', views.ConfirmacaoView.as_view(), name='confirmacao'),
    path('pedido/<uuid:numero_pedido>/', views.PedidoDetailView.as_view(), name='detalhe'),
    path('rastrear/<uuid:numero_pedido>/', views.RastrearPedidoView.as_view(), name='rastrear'),
    
    # Ações do pedido
    path('cancelar/<uuid:numero_pedido>/', views.cancelar_pedido, name='cancelar'),
]
