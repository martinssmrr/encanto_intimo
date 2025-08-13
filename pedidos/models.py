from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from produtos.models import Produto
import uuid


class Pedido(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('processando', 'Em Processamento'),
        ('enviado', 'Enviado'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
        ('devolvido', 'Devolvido'),
    ]

    FORMA_PAGAMENTO_CHOICES = [
        ('stripe', 'Cartão de Crédito (Stripe)'),
        ('mercadopago', 'Mercado Pago'),
        ('pix', 'PIX'),
        ('boleto', 'Boleto'),
    ]

    # Identificação
    numero_pedido = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos', verbose_name="Usuário")
    
    # Status e datas
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente', verbose_name="Status")
    data_pedido = models.DateTimeField(auto_now_add=True, verbose_name="Data do Pedido")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")
    data_envio = models.DateTimeField(blank=True, null=True, verbose_name="Data de Envio")
    data_entrega = models.DateTimeField(blank=True, null=True, verbose_name="Data de Entrega")
    
    # Dados do cliente
    nome_cliente = models.CharField(max_length=200, verbose_name="Nome do Cliente")
    email_cliente = models.EmailField(verbose_name="E-mail do Cliente")
    telefone_cliente = models.CharField(max_length=20, verbose_name="Telefone do Cliente")
    
    # Endereço de entrega
    cep = models.CharField(max_length=9, verbose_name="CEP")
    endereco = models.CharField(max_length=200, verbose_name="Endereço")
    numero = models.CharField(max_length=10, verbose_name="Número")
    complemento = models.CharField(max_length=100, blank=True, verbose_name="Complemento")
    bairro = models.CharField(max_length=100, verbose_name="Bairro")
    cidade = models.CharField(max_length=100, verbose_name="Cidade")
    estado = models.CharField(max_length=2, verbose_name="Estado")
    
    # Valores
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Subtotal")
    valor_frete = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Valor do Frete")
    desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Desconto")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total")
    
    # Pagamento
    forma_pagamento = models.CharField(max_length=20, choices=FORMA_PAGAMENTO_CHOICES, verbose_name="Forma de Pagamento")
    pagamento_confirmado = models.BooleanField(default=False, verbose_name="Pagamento Confirmado")
    transaction_id = models.CharField(max_length=200, blank=True, verbose_name="ID da Transação")
    
    # Observações
    observacoes = models.TextField(blank=True, verbose_name="Observações")
    codigo_rastreamento = models.CharField(max_length=100, blank=True, verbose_name="Código de Rastreamento")

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-data_pedido']

    def __str__(self):
        return f'Pedido #{str(self.numero_pedido)[:8]}'

    def get_absolute_url(self):
        return reverse('pedidos:pedido_detail', kwargs={'numero_pedido': self.numero_pedido})

    @property
    def endereco_completo(self):
        endereco_parts = [self.endereco]
        if self.numero:
            endereco_parts.append(self.numero)
        if self.complemento:
            endereco_parts.append(f'- {self.complemento}')
        if self.bairro:
            endereco_parts.append(f'{self.bairro}')
        if self.cidade and self.estado:
            endereco_parts.append(f'{self.cidade}/{self.estado}')
        if self.cep:
            endereco_parts.append(f'CEP: {self.cep}')
            
        return ', '.join(endereco_parts)

    def pode_cancelar(self):
        return self.status in ['pendente', 'confirmado']

    def total_itens(self):
        return sum(item.quantidade for item in self.itens.all())


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens', verbose_name="Pedido")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, verbose_name="Produto")
    
    # Dados do produto no momento da compra
    nome_produto = models.CharField(max_length=200, verbose_name="Nome do Produto")
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço Unitário")
    quantidade = models.PositiveIntegerField(verbose_name="Quantidade")
    
    # Variações escolhidas
    tamanho = models.CharField(max_length=10, blank=True, verbose_name="Tamanho")
    cor = models.CharField(max_length=50, blank=True, verbose_name="Cor")
    
    # Dados do fornecedor
    fornecedor_nome = models.CharField(max_length=200, verbose_name="Nome do Fornecedor")
    fornecedor_email = models.EmailField(verbose_name="E-mail do Fornecedor")

    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens dos Pedidos"

    def __str__(self):
        return f'{self.nome_produto} x{self.quantidade}'

    @property
    def total_item(self):
        return self.preco_unitario * self.quantidade


class StatusPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='historico_status', verbose_name="Pedido")
    status = models.CharField(max_length=20, choices=Pedido.STATUS_CHOICES, verbose_name="Status")
    data_alteracao = models.DateTimeField(auto_now_add=True, verbose_name="Data da Alteração")
    observacao = models.TextField(blank=True, verbose_name="Observação")
    usuario_alteracao = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Usuário que Alterou")

    class Meta:
        verbose_name = "Histórico de Status"
        verbose_name_plural = "Histórico de Status"
        ordering = ['-data_alteracao']

    def __str__(self):
        return f'{self.pedido} - {self.get_status_display()}'
