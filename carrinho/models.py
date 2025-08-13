from django.db import models
from django.contrib.auth.models import User
from produtos.models import Produto
from decimal import Decimal


class Carrinho(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='carrinho', null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    cep_frete = models.CharField(max_length=9, blank=True, verbose_name="CEP para Frete")
    valor_frete = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Valor do Frete")

    class Meta:
        verbose_name = "Carrinho"
        verbose_name_plural = "Carrinhos"

    def __str__(self):
        if self.usuario:
            return f'Carrinho de {self.usuario.username}'
        return f'Carrinho anônimo {self.session_key}'

    @property
    def total_itens(self):
        return sum(item.quantidade for item in self.itens.all())

    @property
    def subtotal(self):
        return sum(item.total for item in self.itens.all())

    @property
    def total(self):
        return self.subtotal + self.valor_frete

    def limpar(self):
        self.itens.all().delete()
        self.valor_frete = 0
        self.cep_frete = ''
        self.save()

    def calcular_frete(self, cep):
        """Calcula o frete baseado no CEP - versão simulada"""
        self.cep_frete = cep
        # Simulação de cálculo de frete
        peso_total = sum(item.produto.peso or 0.5 for item in self.itens.all())
        if self.subtotal >= 199:
            self.valor_frete = 0  # Frete grátis acima de R$ 199
        elif peso_total <= 1:
            self.valor_frete = Decimal('15.90')
        elif peso_total <= 3:
            self.valor_frete = Decimal('25.90')
        else:
            self.valor_frete = Decimal('35.90')
        self.save()
        return self.valor_frete


class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    tamanho = models.CharField(max_length=10, blank=True)
    cor = models.CharField(max_length=50, blank=True)
    data_adicao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Item do Carrinho"
        verbose_name_plural = "Itens do Carrinho"
        unique_together = ('carrinho', 'produto', 'tamanho', 'cor')

    def __str__(self):
        return f'{self.produto.nome} x{self.quantidade}'

    @property
    def preco_unitario(self):
        return self.produto.preco_final

    @property
    def total(self):
        return self.preco_unitario * self.quantidade

    def verificar_estoque(self):
        """Verifica se há estoque suficiente"""
        return self.produto.estoque_disponivel() >= self.quantidade
