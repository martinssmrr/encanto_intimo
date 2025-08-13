from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Pedido, ItemPedido, StatusPedido
from carrinho.models import Carrinho


class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = 'pedidos/checkout.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            carrinho = Carrinho.objects.get(usuario=self.request.user)
            context['carrinho'] = carrinho
            context['itens'] = carrinho.itens.all()
        except Carrinho.DoesNotExist:
            context['carrinho'] = None
            context['itens'] = []
        return context


class ConfirmacaoView(LoginRequiredMixin, DetailView):
    model = Pedido
    template_name = 'pedidos/confirmacao.html'
    context_object_name = 'pedido'
    slug_field = 'numero_pedido'
    slug_url_kwarg = 'numero_pedido'
    
    def get_queryset(self):
        return Pedido.objects.filter(usuario=self.request.user)


class PedidoDetailView(LoginRequiredMixin, DetailView):
    model = Pedido
    template_name = 'pedidos/detalhe.html'
    context_object_name = 'pedido'
    slug_field = 'numero_pedido'
    slug_url_kwarg = 'numero_pedido'
    
    def get_queryset(self):
        return Pedido.objects.filter(usuario=self.request.user).prefetch_related('itens')


class RastrearPedidoView(DetailView):
    model = Pedido
    template_name = 'pedidos/rastrear.html'
    context_object_name = 'pedido'
    slug_field = 'numero_pedido'
    slug_url_kwarg = 'numero_pedido'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['historico'] = self.object.historico_status.all()
        return context
