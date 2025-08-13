from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from fornecedores.models import Fornecedor


class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    descricao = models.TextField(blank=True, verbose_name="Descrição")
    imagem = models.ImageField(upload_to='categorias/', blank=True, verbose_name="Imagem")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    ordem = models.PositiveIntegerField(default=0, verbose_name="Ordem de Exibição")

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['ordem', 'nome']

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('produtos:categoria', kwargs={'slug': self.slug})


class Tag(models.Model):
    nome = models.CharField(max_length=50, unique=True, verbose_name="Nome")
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    cor = models.CharField(max_length=7, default='#000000', verbose_name="Cor (Hex)")

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)


class Produto(models.Model):
    TAMANHOS_CHOICES = [
        ('PP', 'PP'),
        ('P', 'P'),
        ('M', 'M'),
        ('G', 'G'),
        ('GG', 'GG'),
        ('XG', 'XG'),
        ('XXG', 'XXG'),
        ('UNICO', 'Tamanho Único'),
    ]

    nome = models.CharField(max_length=200, verbose_name="Nome")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    descricao = models.TextField(verbose_name="Descrição")
    descricao_curta = models.CharField(max_length=300, blank=True, verbose_name="Descrição Curta")
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço")
    preco_promocional = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Preço Promocional")
    
    # Relacionamentos
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='produtos', verbose_name="Categoria")
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE, related_name='produtos', verbose_name="Fornecedor")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Tags")
    
    # Características do produto
    tamanhos_disponiveis = models.JSONField(default=list, verbose_name="Tamanhos Disponíveis")
    cores_disponiveis = models.JSONField(default=list, verbose_name="Cores Disponíveis")
    material = models.CharField(max_length=200, blank=True, verbose_name="Material")
    peso = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Peso (kg)")
    
    # Estoque virtual
    estoque_virtual = models.PositiveIntegerField(default=999, verbose_name="Estoque Virtual")
    vendas_simuladas = models.PositiveIntegerField(default=0, verbose_name="Vendas Simuladas")
    
    # SEO
    meta_title = models.CharField(max_length=60, blank=True, verbose_name="Meta Title")
    meta_description = models.CharField(max_length=160, blank=True, verbose_name="Meta Description")
    
    # Status
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    destaque = models.BooleanField(default=False, verbose_name="Produto em Destaque")
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['-data_cadastro']

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('produtos:produto_detail', kwargs={'slug': self.slug})

    @property
    def preco_final(self):
        if self.preco_promocional:
            return self.preco_promocional
        return self.preco

    @property
    def tem_promocao(self):
        return bool(self.preco_promocional and self.preco_promocional < self.preco)

    @property
    def percentual_desconto(self):
        if self.tem_promocao:
            return int(((self.preco - self.preco_promocional) / self.preco) * 100)
        return 0

    @property
    def imagem_principal(self):
        primeira_imagem = self.imagens.first()
        return primeira_imagem.imagem if primeira_imagem else None

    def estoque_disponivel(self):
        return max(0, self.estoque_virtual - self.vendas_simuladas)


class ImagemProduto(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='imagens', verbose_name="Produto")
    imagem = models.ImageField(upload_to='produtos/', verbose_name="Imagem")
    alt_text = models.CharField(max_length=200, blank=True, verbose_name="Texto Alternativo")
    ordem = models.PositiveIntegerField(default=0, verbose_name="Ordem")
    
    class Meta:
        verbose_name = "Imagem do Produto"
        verbose_name_plural = "Imagens dos Produtos"
        ordering = ['ordem']

    def __str__(self):
        return f'{self.produto.nome} - Imagem {self.ordem}'
