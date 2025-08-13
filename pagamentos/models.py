from django.db import models
from django.contrib.auth.models import User
from pedidos.models import Pedido
import uuid


class Pagamento(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('processando', 'Processando'),
        ('aprovado', 'Aprovado'),
        ('rejeitado', 'Rejeitado'),
        ('cancelado', 'Cancelado'),
        ('estornado', 'Estornado'),
    ]

    GATEWAY_CHOICES = [
        ('stripe', 'Stripe'),
        ('mercadopago', 'Mercado Pago'),
        ('pix', 'PIX'),
        ('boleto', 'Boleto'),
    ]

    # Identificação
    id_pagamento = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, related_name='pagamento')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pagamentos')
    
    # Detalhes do pagamento
    gateway = models.CharField(max_length=20, choices=GATEWAY_CHOICES, verbose_name="Gateway de Pagamento")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente', verbose_name="Status")
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor")
    
    # IDs externos
    transaction_id = models.CharField(max_length=200, blank=True, verbose_name="ID da Transação")
    payment_intent_id = models.CharField(max_length=200, blank=True, verbose_name="Payment Intent ID (Stripe)")
    preference_id = models.CharField(max_length=200, blank=True, verbose_name="Preference ID (Mercado Pago)")
    
    # Dados do cartão (apenas últimos 4 dígitos)
    cartao_ultimos_digitos = models.CharField(max_length=4, blank=True, verbose_name="Últimos 4 Dígitos")
    cartao_bandeira = models.CharField(max_length=20, blank=True, verbose_name="Bandeira do Cartão")
    
    # Metadados
    metadata = models.JSONField(default=dict, blank=True, verbose_name="Metadados")
    
    # Timestamps
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    data_processamento = models.DateTimeField(null=True, blank=True, verbose_name="Data de Processamento")
    data_confirmacao = models.DateTimeField(null=True, blank=True, verbose_name="Data de Confirmação")

    class Meta:
        verbose_name = "Pagamento"
        verbose_name_plural = "Pagamentos"
        ordering = ['-data_criacao']

    def __str__(self):
        return f'Pagamento {str(self.id_pagamento)[:8]} - {self.get_status_display()}'

    @property
    def esta_aprovado(self):
        return self.status == 'aprovado'

    @property
    def pode_cancelar(self):
        return self.status in ['pendente', 'processando']


class LogPagamento(models.Model):
    pagamento = models.ForeignKey(Pagamento, on_delete=models.CASCADE, related_name='logs')
    evento = models.CharField(max_length=100, verbose_name="Evento")
    dados = models.JSONField(default=dict, verbose_name="Dados do Evento")
    data_evento = models.DateTimeField(auto_now_add=True, verbose_name="Data do Evento")

    class Meta:
        verbose_name = "Log de Pagamento"
        verbose_name_plural = "Logs de Pagamento"
        ordering = ['-data_evento']

    def __str__(self):
        return f'{self.pagamento} - {self.evento}'
