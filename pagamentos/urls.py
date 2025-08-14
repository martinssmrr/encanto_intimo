from django.urls import path
from . import views

app_name = 'pagamentos'

urlpatterns = [
    # Processar pagamento
    path('processar/', views.ProcessarPagamentoView.as_view(), name='processar'),
    
    # Retornos do Mercado Pago
    path('sucesso/', views.PagamentoSucessoView.as_view(), name='sucesso'),
    path('falha/', views.PagamentoFalhaView.as_view(), name='falha'),
    path('pendente/', views.PagamentoPendenteView.as_view(), name='pendente'),
    
    # Webhooks
    path('webhook/', views.MercadoPagoWebhookView.as_view(), name='webhook'),
    path('mercadopago/webhook/', views.MercadoPagoWebhookView.as_view(), name='mercadopago_webhook'),
]
