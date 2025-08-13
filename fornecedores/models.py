from django.db import models
from django.urls import reverse


class Fornecedor(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome")
    email = models.EmailField(verbose_name="E-mail")
    telefone = models.CharField(max_length=20, blank=True, verbose_name="Telefone")
    endereco = models.TextField(blank=True, verbose_name="Endereço")
    catalogo_url = models.URLField(blank=True, verbose_name="URL do Catálogo")
    api_endpoint = models.URLField(blank=True, verbose_name="Endpoint da API")
    observacoes = models.TextField(blank=True, verbose_name="Observações")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('adminpanel:fornecedor_detail', kwargs={'pk': self.pk})

    def produtos_count(self):
        return self.produtos.count()
    produtos_count.short_description = "Qtd. Produtos"
