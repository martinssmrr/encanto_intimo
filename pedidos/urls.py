from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('confirmacao/<uuid:numero_pedido>/', views.ConfirmacaoView.as_view(), name='confirmacao'),
    path('pedido/<uuid:numero_pedido>/', views.PedidoDetailView.as_view(), name='pedido_detail'),
    path('rastrear/<uuid:numero_pedido>/', views.RastrearPedidoView.as_view(), name='rastrear'),
]
