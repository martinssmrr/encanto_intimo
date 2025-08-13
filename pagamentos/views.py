from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Pagamento


class ProcessarPagamentoView(LoginRequiredMixin, TemplateView):
    template_name = 'pagamentos/processar.html'


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(View):
    def post(self, request):
        # Implementar webhook do Stripe
        return HttpResponse(status=200)


@method_decorator(csrf_exempt, name='dispatch')
class MercadoPagoWebhookView(View):
    def post(self, request):
        # Implementar webhook do Mercado Pago
        return HttpResponse(status=200)


class PagamentoSucessoView(LoginRequiredMixin, TemplateView):
    template_name = 'pagamentos/sucesso.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pagamento = get_object_or_404(Pagamento, id_pagamento=kwargs['pagamento_id'], usuario=self.request.user)
        context['pagamento'] = pagamento
        return context


class PagamentoCanceladoView(LoginRequiredMixin, TemplateView):
    template_name = 'pagamentos/cancelado.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pagamento = get_object_or_404(Pagamento, id_pagamento=kwargs['pagamento_id'], usuario=self.request.user)
        context['pagamento'] = pagamento
        return context
