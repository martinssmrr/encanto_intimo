from django.urls import path
from . import views

app_name = 'pagamentos'

urlpatterns = [
    path('processar/', views.ProcessarPagamentoView.as_view(), name='processar'),
    path('stripe/webhook/', views.StripeWebhookView.as_view(), name='stripe_webhook'),
    path('mercadopago/webhook/', views.MercadoPagoWebhookView.as_view(), name='mercadopago_webhook'),
    path('sucesso/<uuid:pagamento_id>/', views.PagamentoSucessoView.as_view(), name='sucesso'),
    path('cancelado/<uuid:pagamento_id>/', views.PagamentoCanceladoView.as_view(), name='cancelado'),
]
